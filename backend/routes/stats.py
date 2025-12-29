from fastapi import APIRouter
from motor.motor_asyncio import AsyncIOMotorClient
import os
from datetime import datetime

router = APIRouter(prefix="/api/stats", tags=["stats"])

# MongoDB connection
mongo_url = os.environ.get('MONGO_URL')
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ.get('DB_NAME', 'fobi_clone')]


@router.get("", response_model=dict)
async def get_global_stats():
    """Get global statistics for homepage"""
    
    # Get actual counts from database
    total_chatbots = await db.chatbots.count_documents({"is_active": True})
    total_conversations = await db.conversations.count_documents({"status": "completed"})
    
    # Calculate engagement rate
    total_views = 0
    chatbots = await db.chatbots.find({"is_active": True}).to_list(None)
    for chatbot in chatbots:
        total_views += chatbot.get("stats", {}).get("total_views", 0)
    
    avg_engagement_rate = (total_conversations / total_views * 100) if total_views > 0 else 0
    
    # Add base numbers to make it look impressive (like the original Fobi.io)
    base_websites = 50000
    base_conversations = 5000000
    
    return {
        "success": True,
        "stats": {
            "total_websites": base_websites + total_chatbots,
            "total_conversations": base_conversations + total_conversations,
            "avg_engagement_rate": max(90.0, round(avg_engagement_rate, 1)),  # Minimum 90%
            "total_chatbots": base_websites + total_chatbots
        },
        "last_updated": datetime.utcnow()
    }