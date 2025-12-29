from pydantic import BaseModel, Field
from datetime import datetime


class GlobalStats(BaseModel):
    id: str = "global_stats"
    total_chatbots: int = 50234
    total_conversations: int = 5123456
    total_websites: int = 50234
    avg_engagement_rate: float = 90.5
    last_updated: datetime = Field(default_factory=datetime.utcnow)