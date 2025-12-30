from fastapi import APIRouter, HTTPException
from models.conversation import Conversation, ConversationCreate, ConversationUpdate
from services.chat_engine import chat_engine
from typing import Dict, Any
from motor.motor_asyncio import AsyncIOMotorClient
import os
from datetime import datetime

router = APIRouter(prefix="/api/conversations", tags=["conversations"])

# MongoDB connection
mongo_url = os.environ.get('MONGO_URL')
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ.get('DB_NAME', 'fobi_clone')]


@router.post("", response_model=dict)
async def create_conversation(conversation_data: ConversationCreate):
    """Create/start a new conversation"""
    
    # Check if chatbot exists
    chatbot = await db.chatbots.find_one({"chatbot_id": conversation_data.chatbot_id})
    if not chatbot:
        raise HTTPException(status_code=404, detail="Chatbot not found")
    
    # Create conversation
    conversation = Conversation(
        chatbot_id=conversation_data.chatbot_id,
        user_data=conversation_data.user_data or {}
    )
    
    # Insert into database
    conversation_dict = conversation.dict()
    await db.conversations.insert_one(conversation_dict)
    
    # Increment chatbot views
    await db.chatbots.update_one(
        {"chatbot_id": conversation_data.chatbot_id},
        {"$inc": {"stats.total_views": 1}}
    )
    
    # Get the first question
    next_question = chat_engine.get_next_question(chatbot.get("form_schema", {}), [])

    return {
        "success": True,
        "conversation_id": conversation.conversation_id,
        "message": "Conversation started",
        "next_question": next_question
    }


@router.put("/{conversation_id}", response_model=dict)
async def update_conversation(conversation_id: str, update_data: ConversationUpdate):
    """Update conversation (add responses, mark completed)"""
    
    # Check if conversation exists
    conversation = await db.conversations.find_one({"conversation_id": conversation_id})
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")
    
    # Prepare update data
    update_dict = {k: v for k, v in update_data.dict(exclude_unset=True).items() if v is not None}
    
    # If marking as completed, set completed_at
    if update_data.status == "completed" and not update_dict.get("completed_at"):
        update_dict["completed_at"] = datetime.utcnow()
    
    # Update in database
    await db.conversations.update_one(
        {"conversation_id": conversation_id},
        {"$set": update_dict}
    )
    
    # If completed, increment chatbot stats
    if update_data.status == "completed":
        await db.chatbots.update_one(
            {"chatbot_id": conversation["chatbot_id"]},
            {"$inc": {"stats.total_conversations": 1}}
        )
    
    
    # Get associated chatbot for schema
    chatbot = await db.chatbots.find_one({"chatbot_id": conversation["chatbot_id"]})
    if not chatbot:
        raise HTTPException(status_code=404, detail="Chatbot for conversation not found")

    # Get the current responses from update_dict or existing conversation
    current_responses = update_dict.get("responses") or conversation.get("responses", [])
    
    # Get next question
    next_question = chat_engine.get_next_question(chatbot.get("form_schema", {}), current_responses)
    
    # Determine if conversation is "internally" completed (no more questions)
    is_flow_completed = next_question is None
    
    if is_flow_completed and update_data.status != "completed":
        # Auto-complete if flow is done
        update_dict["status"] = "completed"
        update_dict["completed_at"] = datetime.utcnow()
        await db.conversations.update_one(
             {"conversation_id": conversation_id},
             {"$set": update_dict}
        )
        # Also increment stats if we auto-completed it just now
        await db.chatbots.update_one(
            {"chatbot_id": conversation["chatbot_id"]},
            {"$inc": {"stats.total_conversations": 1}}
        )

    return {
        "success": True,
        "message": "Conversation updated",
        "next_question": next_question
    }


@router.get("/{conversation_id}", response_model=dict)
async def get_conversation(conversation_id: str):
    """Get conversation details"""
    
    conversation = await db.conversations.find_one({"conversation_id": conversation_id})
    if conversation and "_id" in conversation:
        conversation["_id"] = str(conversation["_id"])
    
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")
    
    return {
        "success": True,
        "conversation": conversation
    }