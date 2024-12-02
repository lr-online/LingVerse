from typing import Any, Dict

from pydantic import Field

from app.models.base import MongoBaseModel
from app.utils.logger import get_logger

logger = get_logger(__name__)


class LLM(MongoBaseModel):
    """大语言模型数据模型"""

    model_name: str = Field(..., description="模型名称,如 gpt-4/claude-2")
    provider: str = Field(..., description="模型提供商,如 OpenAI")
    api_key: str = Field(..., description="API Key")
    base_url: str = Field(..., description="API Base URL")

    class Config:
        json_schema_extra = {
            "example": {
                "id": "1234567890",
                "model_name": "gpt-4",
                "provider": "openai",
                "created_at": "2024-01-01 00:00:00",
                "updated_at": "2024-01-01 00:00:00",
                "is_deleted": False,
            }
        }

    @classmethod
    async def create(cls, model_name: str, provider: str, api_key: str, base_url: str) -> "LLM":
        # 检查模型是否存在
        record = await cls.get_by_multi_field(
            {
                "model_name": model_name,
                "provider": provider,
                "api_key": api_key,
                "base_url": base_url
            }
        )
        if record:
            logger.warning(f"模型 {model_name} 已存在")
            return record

        return await super().create(model_name=model_name, provider=provider, api_key=api_key, base_url=base_url)

    @classmethod
    async def update_by_id(cls, id: str, **kwargs) -> bool:
        raise NotImplementedError("LLM 不支持更新")

    @classmethod
    async def update_by_field(
        cls, filter_dict: Dict[str, Any], data: Dict[str, Any]
    ) -> bool:
        if {"is_deleted"} == set(data.keys()):
            return await super().update_by_field(filter_dict, data)
        else:
            logger.warning("LLM 不支持更新字段, 屏蔽此次更新")
            return False

