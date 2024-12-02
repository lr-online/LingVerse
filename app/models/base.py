from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List, Optional, Type, TypeVar, Union

from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorCollection
from pydantic import BaseModel as PydanticBaseModel
from pydantic import Field

from app.infra.mongo_db_sdk import MongoDBSDK
from app.utils.datetime_utils import get_china_now
from app.utils.logger import get_logger

logger = get_logger(__name__)

T = TypeVar("T", bound="MongoBaseModel")


class MongoBaseModel(PydanticBaseModel):
    """MongoDB基础数据模型，提供通用的CRUD操作"""

    id: Optional[str] = Field(None, alias="_id")
    created_at: datetime = Field(default_factory=get_china_now)
    updated_at: datetime = Field(default_factory=get_china_now)
    is_deleted: bool = Field(default=False)

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        populate_by_name = True

    @classmethod
    def collection_name(cls) -> str:
        return cls.__name__.lower()

    @classmethod
    def collection(cls) -> AsyncIOMotorCollection:
        return MongoDBSDK.db[cls.collection_name()]

    # 自动创建表
    @classmethod
    async def create_indexes(cls):
        """创建索引"""
        await cls.collection().create_index("created_at")
        await cls.collection().create_index("updated_at")
        await cls.collection().create_index("is_deleted")

    @classmethod
    async def create(cls, **kwargs) -> "MongoBaseModel":
        """
        创建新文档

        Args:
            **kwargs: 文档数据字典

        Returns:
            MongoBaseModel: 创建的文档对象
        """
        try:
            # 确保更新时间戳
            new_record = cls(**kwargs)
            record_id = await cls.collection().insert_one(
                new_record.model_dump(exclude={"id"})
            )
            new_record.id = str(record_id.inserted_id)

            logger.debug(f"Created document in {cls.collection_name()}: {record_id}")
            return new_record
        except Exception as e:
            logger.error(f"Failed to create document in {cls.collection_name()}: {e}")
            raise

    @classmethod
    async def get_by_id(cls, id: str) -> Optional["MongoBaseModel"]:
        """
        获取单个文档

        Args:
            id: 文档ID

        Returns:
            Optional[MongoBaseModel]: 文档对象,不存在则返回None
        """
        try:
            doc = await cls.collection().find_one(
                {"_id": ObjectId(id), "is_deleted": False}
            )
            if doc:
                doc["_id"] = str(doc["_id"])
                return cls(**doc)
            return None
        except Exception as e:
            logger.error(f"Failed to get document from {cls.collection_name()}: {e}")
            raise

    @classmethod
    async def get_by_single_field(cls: Type[T], field: str, value: Any) -> Optional[T]:
        """
        通过指定字段获取文档

        Args:
            field: 字段名
            value: 字段值

        Returns:
            Optional[T]: 文档对象,不存在则返回None
        """
        try:
            doc = await cls.collection().find_one({field: value, "is_deleted": False})
            if doc:
                doc["_id"] = str(doc["_id"])
                return cls(**doc)
            return None
        except Exception as e:
            logger.error(
                f"Failed to get document by field from {cls.collection_name()}: {e}"
            )
            raise

    @classmethod
    async def get_by_multi_field(
        cls: Type[T], filter_dict: Dict[str, Any]
    ) -> Optional[T]:
        """
        通过多个字段获取文档

        Args:
            filter_dict: 字段名和字段值的字典

        Returns:
            Optional[T]: 文档对象,不存在则返回None
        """
        try:
            doc = await cls.collection().find_one(filter_dict)
            if doc:
                doc["_id"] = str(doc["_id"])
                return cls(**doc)
            return None
        except Exception as e:
            logger.error(
                f"Failed to get document by field from {cls.collection_name()}: {e}"
            )
            raise

    @classmethod
    async def update_by_id(cls, id: str, data: Dict[str, Any]) -> bool:
        """
        更新文档

        Args:
            id: 文档ID
            data: 更新的数据

        Returns:
            bool: 更新是否成功
        """

        try:
            # 更新时间戳
            data["updated_at"] = get_china_now()

            result = await cls.collection().update_one(
                {"_id": ObjectId(id), "is_deleted": False}, {"$set": data}
            )
            success = result.modified_count > 0
            logger.debug(f"Updated document in {cls.collection_name()}: {id}")
            return success
        except Exception as e:
            logger.error(f"Failed to update document in {cls.collection_name()}: {e}")
            raise

    @classmethod
    async def update_by_field(
        cls, filter_dict: Dict[str, Any], data: Dict[str, Any]
    ) -> bool:
        """
        通过指定条件更新文档

        Args:
            filter_dict: 过滤条件
            data: 更新的数据

        Returns:
            bool: 更新是否成功
        """
        try:
            filter_dict["is_deleted"] = False
            data["updated_at"] = get_china_now()
            result = await cls.collection().update_one(filter_dict, {"$set": data})
            logger.debug(
                f"Updated document by field in {cls.collection_name()}: {filter_dict}"
            )
            return result.modified_count > 0
        except Exception as e:
            logger.error(
                f"Failed to update document by field in {cls.collection_name()}: {e}"
            )
            raise

    async def delete(self) -> bool:
        """
        软删除文档

        Returns:
            bool: 删除是否成功
        """
        if not self.id:
            raise ValueError("Document ID is required for delete")

        try:
            result = await self.collection().update_one(
                {"_id": ObjectId(self.id), "is_deleted": False},
                {"$set": {"is_deleted": True, "updated_at": get_china_now()}},
            )
            success = result.modified_count > 0
            if success:
                self.is_deleted = True
                self.updated_at = get_china_now()
                logger.debug(
                    f"Soft deleted document from {self.collection_name()}: {self.id}"
                )
            return success
        except Exception as e:
            logger.error(
                f"Failed to delete document from {self.collection_name()}: {e}"
            )
            raise

    @classmethod
    async def list(
        cls: Type[T],
        filter_dict: Dict[str, Any] = None,
        skip: int = 0,
        limit: int = 100,
    ) -> List[T]:
        """列出符合条件的文档"""
        if skip < 0:
            raise ValueError("Skip must be non-negative")
        if limit <= 0:
            raise ValueError("Limit must be positive")
        if limit > 1000:
            raise ValueError("Limit cannot exceed 1000")

        try:
            # 添加未删除过滤条件
            filter_dict = filter_dict or {}
            filter_dict["is_deleted"] = False

            cursor = cls.collection().find(filter_dict).skip(skip).limit(limit)
            documents = await cursor.to_list(length=None)

            # 转换ID为字符串
            for doc in documents:
                doc["_id"] = str(doc["_id"])

            return [cls(**doc) for doc in documents]
        except Exception as e:
            logger.error(f"Failed to list documents from {cls.__name__}: {e}")
            raise
