from typing import Optional

from pydantic import Field

from app.models.base import MongoBaseModel
from app.utils.logger import get_logger

logger = get_logger(__name__)


class Person(MongoBaseModel):
    """Person data model"""

    name: Optional[str] = Field(None, description="人物姓名")
    gender: Optional[str] = Field(None, description="性别, 可选值: 男, 女")
    birthday: Optional[str] = Field(None, description="出生日期")
    email: Optional[str] = Field(None, description="邮箱")
    phone: Optional[str] = Field(None, description="电话号码")
    access_token: Optional[str] = Field(None, description="访问令牌")
    avatar_url: Optional[str] = Field(None, description="头像链接")
    role: Optional[str] = Field("user", description="角色, 可选值: admin, user， ai")
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


if __name__ == "__main__":
    import asyncio

    async def create_person():
        # 创建一个人物实例
        await Person.create(
            name="女娲",
            gender="女",
            birthday="1990-01-01",
            email="",
            phone="18888888888",
            access_token="abc123",
            avatar_url="https://www.example.com/avatar.jpg",
            role="admin",
            address="北京市朝阳区",
            language_preference="chinese",
        )

        asyncio.run(create_person())
