from datetime import datetime
from typing import Any, Dict, Optional

from pydantic import Field

from app.infra.mongo_db_sdk import MongoDBSDK
from app.models.base import MongoBaseModel


class LLMModel(MongoBaseModel):
    """大语言模型数据模型"""

    model_name: str = Field(..., description="模型名称,如 gpt-4/claude-2")

    class Config:
        schema_extra = {
            "example": {
                "id": "1234567890",
                "model_name": "gpt-4",
                "created_at": "2024-01-01 00:00:00",
                "updated_at": "2024-01-01 00:00:00",
                "is_deleted": False,
            }
        }

    @classmethod
    async def create(cls, model_name: str) -> "LLMModel":
        # 检查模型是否存在
        if await cls.get_by_field("model_name", model_name):
            raise ValueError(f"模型 {model_name} 已存在")

        return await super().create(model_name=model_name)

    @classmethod
    async def update_by_id(cls, id: str, **kwargs) -> bool:
        raise NotImplementedError("LLMModel 不支持更新")

    @classmethod
    async def update_by_field(
        cls, filter_dict: Dict[str, Any], data: Dict[str, Any]
    ) -> bool:
        raise NotImplementedError("LLMModel 不支持更新")
