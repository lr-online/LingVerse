import uuid
from typing import Optional

from pydantic import Field
from pydantic.v1 import validator

from app.models.base import MongoBaseModel
from app.utils.config import get_settings
from app.utils.logger import get_logger

logger = get_logger(__name__)


class Person(MongoBaseModel):
    """Person data model"""

    name: Optional[str] = Field(None, description="人物姓名")
    gender: Optional[str] = Field(None, description="性别, 可选值: 男, 女")
    birthday: Optional[str] = Field(None, description="出生日期")
    email: Optional[str] = Field(None, description="邮箱")
    phone: Optional[str] = Field(None, description="电话号码")
    access_token: Optional[str] = Field(
        default_factory=lambda: uuid.uuid4().hex, description="访问令牌"
    )
    avatar_url: Optional[str] = Field(None, description="头像链接")
    role: Optional[str] = Field("human", description="角色, 可选值: admin, human，ai")
    address: Optional[str] = Field(None, description="用户所在地址")
    language_preference: Optional[str] = Field(
        "chinese", description="语言偏好, 可选值: chinese, english, japanese"
    )
    description: Optional[str] = Field(None, description="描述")

    class Config:
        json_schema_extra = {
            "example": {
                "id": "1234567890",
                "name": "张三",
                "gender": "男",
                "birthday": "1990-01-01",
                "email": "2233@gmail.com",
                "phone": "18888888888",
                "access_token": "abc123",
                "avatar_url": "https://www.example.com/avatar.jpg",
                "role": "admin",
                "address": "北京市朝阳区",
                "language_preference": "chinese",
                "description": "这是一个人物简介",
                "created_at": "2022-01-01T00:00:00",
                "updated_at": "2022-01-01T00:00:00",
                "is_deleted": False,
            }
        }

    @validator("role")
    def validate_role(cls, value):
        if value not in {"admin", "human", "ai"}:
            raise ValueError("角色必须是 'admin', 'human' 或 'ai'")
        return value

    @validator("language_preference")
    def validate_language_preference(cls, value):
        if value not in {"chinese", "english", "japanese"}:
            raise ValueError("语言偏好必须是 'chinese', 'english' 或 'japanese'")
        return value

    @validator("gender")
    def validate_gender(cls, value):
        if value not in {"男", "女"}:
            raise ValueError("性别必须是 '男' 或 '女'")
        return value

    @classmethod
    async def setup(cls):
        admin_cfg = get_settings().admin

        if await cls.get_by_single_field("role", "admin"):
            logger.warning("Admin user already exists, skip creating")
            return
        await cls.create(
            name=admin_cfg.user,
            email=admin_cfg.email,
            phone=admin_cfg.phone,
            access_token=admin_cfg.token,
            role="admin",
        )


if __name__ == "__main__":
    import asyncio

    asyncio.run(Person.setup())
