from pydantic import Field

from app.models.base import MongoBaseModel
from app.models.person import Person
from app.utils.logger import get_logger

logger = get_logger(__name__)


class Memory(MongoBaseModel):
    """Memory data model"""

    owner_id: str = Field(..., description="所有者ID")
    title: str = Field(..., description="记忆标题")
    content: str = Field(..., description="记忆内容")
    creator_id: str = Field(..., description="创建者ID")
    tags: list[str] = Field(None, description="标签列表")

    class Config:
        json_schema_extra = {
            "example": {
                "id": "1234567890",
                "owner_id": "1234567890",
                "title": "旅游",
                "content": "张三周六要去西藏旅游",
                "creator_id": "1234567890",
                "tags": ["旅游", "出行"],
                "created_at": "2022-01-01T00:00:00",
                "updated_at": "2022-01-01T00:00:00",
                "is_deleted": False,
            }
        }


if __name__ == "__main__":
    import asyncio

    asyncio.run(
        Memory.create(
            owner_id="674d4e7e1ec6ae081672debe",
            title="旅游",
            content="李四周六要去云南旅游",
            creator_id="674d4e7e1ec6ae081672debe",
            tags=["旅游", "出行"],
        )
    )
