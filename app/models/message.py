from typing import Optional

from pydantic import Field

from app.models.base import MongoBaseModel
from app.utils.logger import get_logger

logger = get_logger(__name__)


class Message(MongoBaseModel):
    """Message data model"""

    conversation_id: str = Field(..., description="对话ID")
    sender_id: str = Field(..., description="发送者ID")
    receiver_id: str = Field(..., description="接收者ID")
    message_type: str = Field(..., description="消息类型")
    content: Optional[str] = Field(None, description="消息内容")
    media_url: Optional[str] = Field(None, description="媒体链接")
    metadata: Optional[dict] = Field(None, description="元数据")
    is_read: bool = Field(False, description="消息是否已读")
