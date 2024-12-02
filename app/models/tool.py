from typing import Optional

from pydantic import Field

from app.models.base import MongoBaseModel
from app.utils.logger import get_logger

logger = get_logger(__name__)


class Tool(MongoBaseModel):
    name: str = Field(..., description="工具名称")
    description: Optional[str] = Field(None, description="工具描述")
    content: Optional[str] = Field(None, description="工具内容")

    class Config:
        json_schema_extra = {
            "example": {
                "id": "1234567890",
                "name": "记事本",
                "description": "一个简单的记事本",
                "content": "这是一个记事本内容",
                "created_at": "2022-01-01T00:00:00",
                "updated_at": "2022-01-01T00:00:00",
                "is_deleted": False,
            }
        }


if __name__ == "__main__":
    import asyncio

    asyncio.run(
        Tool.create(
            name="记事本",
            description="一个简单的记事本",
            content="这是一个记事本内容",
        )
    )
