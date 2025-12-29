from pydantic import BaseModel, Field, HttpUrl
from typing import Optional, Dict, List
from datetime import datetime
import uuid


class Customization(BaseModel):
    primary_color: str = "#7c3aed"
    secondary_color: str = "#2563eb"
    bot_name: str = "Assistant"
    welcome_message: str = "Hi! How can I help you today?"
    position: str = "bottom-right"  # bottom-right, bottom-left
    size: str = "medium"  # small, medium, large


class ChatbotStats(BaseModel):
    total_conversations: int = 0
    total_views: int = 0
    completion_rate: float = 0.0


class Chatbot(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    chatbot_id: str = Field(default_factory=lambda: f"bot_{uuid.uuid4().hex[:12]}")
    google_form_url: str
    name: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    customization: Customization = Field(default_factory=Customization)
    stats: ChatbotStats = Field(default_factory=ChatbotStats)
    embed_type: str = "popup"  # popup, iframe
    is_active: bool = True

    class Config:
        json_schema_extra = {
            "example": {
                "google_form_url": "https://docs.google.com/forms/d/e/1FAIpQLSc...",
                "name": "Contact Form Chatbot",
                "embed_type": "popup"
            }
        }


class ChatbotCreate(BaseModel):
    google_form_url: str
    name: str
    customization: Optional[Customization] = None
    embed_type: str = "popup"


class ChatbotUpdate(BaseModel):
    name: Optional[str] = None
    google_form_url: Optional[str] = None
    customization: Optional[Customization] = None
    embed_type: Optional[str] = None
    is_active: Optional[bool] = None