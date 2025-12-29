from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from models.chatbot import Chatbot, ChatbotCreate, ChatbotUpdate, Customization
from motor.motor_asyncio import AsyncIOMotorClient
import os
from datetime import datetime
import re

router = APIRouter(prefix="/api/chatbots", tags=["chatbots"])

# MongoDB connection
mongo_url = os.environ.get('MONGO_URL')
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ.get('DB_NAME', 'fobi_clone')]


def validate_google_form_url(url: str) -> bool:
    """Validate if the URL is a Google Form URL"""
    pattern = r'https://(docs\.google\.com/forms/|forms\.gle/)'
    return bool(re.match(pattern, url))


def generate_embed_code(chatbot_id: str, embed_type: str, customization: dict) -> dict:
    """Generate embed code for the chatbot"""
    base_url = os.environ.get('REACT_APP_BACKEND_URL', 'http://localhost:3000')
    
    popup_code = f'''<!-- Fobi Chatbot Popup -->
<script>
  (function() {{
    var chatbotId = '{chatbot_id}';
    var config = {{
      primaryColor: '{customization.get("primary_color", "#7c3aed")}',
      secondaryColor: '{customization.get("secondary_color", "#2563eb")}',
      botName: '{customization.get("bot_name", "Assistant")}',
      welcomeMessage: '{customization.get("welcome_message", "Hi! How can I help you?")}',
      position: '{customization.get("position", "bottom-right")}',
      size: '{customization.get("size", "medium")}'
    }};
    
    var script = document.createElement('script');
    script.src = '{base_url}/chatbot-widget.js';
    script.setAttribute('data-chatbot-id', chatbotId);
    script.setAttribute('data-config', JSON.stringify(config));
    document.body.appendChild(script);
  }})();
</script>'''
    
    iframe_code = f'''<!-- Fobi Chatbot IFrame -->
<iframe 
  src="{base_url}/embed/{chatbot_id}" 
  width="100%" 
  height="600px" 
  frameborder="0" 
  style="border: none; border-radius: 8px;"
></iframe>'''
    
    return {
        "popup": popup_code,
        "iframe": iframe_code
    }


@router.post("", response_model=dict)
async def create_chatbot(chatbot_data: ChatbotCreate):
    """Create a new chatbot from Google Form"""
    
    # Validate Google Form URL
    if not validate_google_form_url(chatbot_data.google_form_url):
        raise HTTPException(
            status_code=400,
            detail="Invalid Google Form URL. Please provide a valid Google Forms link."
        )
    
    # Create chatbot object
    chatbot = Chatbot(
        google_form_url=chatbot_data.google_form_url,
        name=chatbot_data.name,
        customization=chatbot_data.customization or Customization(),
        embed_type=chatbot_data.embed_type
    )
    
    # Insert into database
    chatbot_dict = chatbot.dict()
    await db.chatbots.insert_one(chatbot_dict)
    
    # Generate embed code
    embed_code = generate_embed_code(
        chatbot.chatbot_id,
        chatbot.embed_type,
        chatbot.customization.dict()
    )
    
    return {
        "success": True,
        "chatbot_id": chatbot.chatbot_id,
        "message": "Chatbot created successfully",
        "chatbot": chatbot_dict,
        "embed_code": embed_code
    }


@router.get("", response_model=dict)
async def get_chatbots(
    page: int = Query(1, ge=1),
    per_page: int = Query(10, ge=1, le=100),
    is_active: Optional[bool] = None
):
    """Get all chatbots with pagination"""
    
    # Build query
    query = {}
    if is_active is not None:
        query["is_active"] = is_active
    
    # Get total count
    total = await db.chatbots.count_documents(query)
    
    # Get paginated results
    skip = (page - 1) * per_page
    chatbots = await db.chatbots.find(query).skip(skip).limit(per_page).to_list(per_page)
    
    return {
        "success": True,
        "chatbots": chatbots,
        "total": total,
        "page": page,
        "per_page": per_page,
        "total_pages": (total + per_page - 1) // per_page
    }


@router.get("/{chatbot_id}", response_model=dict)
async def get_chatbot(chatbot_id: str):
    """Get specific chatbot details"""
    
    chatbot = await db.chatbots.find_one({"chatbot_id": chatbot_id})
    
    if not chatbot:
        raise HTTPException(status_code=404, detail="Chatbot not found")
    
    # Generate embed code
    embed_code = generate_embed_code(
        chatbot["chatbot_id"],
        chatbot["embed_type"],
        chatbot["customization"]
    )
    
    return {
        "success": True,
        "chatbot": chatbot,
        "embed_code": embed_code
    }


@router.put("/{chatbot_id}", response_model=dict)
async def update_chatbot(chatbot_id: str, update_data: ChatbotUpdate):
    """Update chatbot customization"""
    
    # Check if chatbot exists
    chatbot = await db.chatbots.find_one({"chatbot_id": chatbot_id})
    if not chatbot:
        raise HTTPException(status_code=404, detail="Chatbot not found")
    
    # Validate Google Form URL if provided
    if update_data.google_form_url and not validate_google_form_url(update_data.google_form_url):
        raise HTTPException(
            status_code=400,
            detail="Invalid Google Form URL"
        )
    
    # Prepare update data
    update_dict = {k: v for k, v in update_data.dict(exclude_unset=True).items() if v is not None}
    update_dict["updated_at"] = datetime.utcnow()
    
    # Update in database
    await db.chatbots.update_one(
        {"chatbot_id": chatbot_id},
        {"$set": update_dict}
    )
    
    return {
        "success": True,
        "message": "Chatbot updated successfully"
    }


@router.delete("/{chatbot_id}", response_model=dict)
async def delete_chatbot(chatbot_id: str):
    """Delete a chatbot"""
    
    result = await db.chatbots.delete_one({"chatbot_id": chatbot_id})
    
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Chatbot not found")
    
    # Also delete associated conversations
    await db.conversations.delete_many({"chatbot_id": chatbot_id})
    
    return {
        "success": True,
        "message": "Chatbot deleted successfully"
    }


@router.get("/{chatbot_id}/stats", response_model=dict)
async def get_chatbot_stats(chatbot_id: str):
    """Get specific chatbot statistics"""
    
    chatbot = await db.chatbots.find_one({"chatbot_id": chatbot_id})
    
    if not chatbot:
        raise HTTPException(status_code=404, detail="Chatbot not found")
    
    # Get conversation stats
    total_conversations = await db.conversations.count_documents({"chatbot_id": chatbot_id})
    completed_conversations = await db.conversations.count_documents({
        "chatbot_id": chatbot_id,
        "status": "completed"
    })
    
    completion_rate = (completed_conversations / total_conversations * 100) if total_conversations > 0 else 0
    
    return {
        "success": True,
        "stats": {
            "total_conversations": total_conversations,
            "completed_conversations": completed_conversations,
            "total_views": chatbot.get("stats", {}).get("total_views", 0),
            "completion_rate": round(completion_rate, 2)
        }
    }