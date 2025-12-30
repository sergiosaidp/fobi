from pydantic import BaseModel, Field
from typing import Optional, List, Dict
from datetime import datetime
import uuid


class Conversation(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    conversation_id: str = Field(default_factory=lambda: f"conv_{uuid.uuid4().hex[:12]}")
    chatbot_id: str
    started_at: datetime = Field(default_factory=datetime.utcnow)
    completed_at: Optional[datetime] = None
    responses: List[Dict] = Field(default_factory=list)
    user_data: Dict = Field(default_factory=dict)
    status: str = "started"  # started, completed, abandoned


class ConversationCreate(BaseModel):
    chatbot_id: str
    user_data: Optional[Dict] = None


class ConversationUpdate(BaseModel):
    status: Optional[str] = None
    responses: Optional[List[Dict]] = None
    completed_at: Optional[datetime] = None