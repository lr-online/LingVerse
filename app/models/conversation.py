from typing import Optional

from pydantic import Field

from app.models.base import MongoBaseModel
from app.utils.logger import get_logger

logger = get_logger(__name__)


class Conversation(MongoBaseModel):
    """Conversation data model"""

    name: str = Field("新会话", description="对话名称")
    members: Optional[list[str]] = Field(None, description="对话成员的ID列表")

    class Config:
        json_schema_extra = {
            "example": {
                "id": "1234567890",
                "name": "吃瓜群",
                "members": ["123", "456"],
                "created_at": "2022-01-01T00:00:00",
                "updated_at": "2022-01-01T00:00:00",
                "is_deleted": False,
            }
        }
