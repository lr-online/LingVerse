from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List, Optional, Union

from bson import ObjectId
from pydantic import BaseModel as PydanticBaseModel
from pydantic import Field

from app.infra.mongo_db_sdk import MongoDBSDK
from app.utils.datetime_utils import get_china_now
from app.utils.logger import get_logger

logger = get_logger(__name__)


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
    async def create(
        cls, mongo_client: MongoDBSDK, data: Dict[str, Any]
    ) -> "MongoBaseModel":
        """
        创建新文档

        Args:
            mongo_client: MongoDB客户端
            data: 文档数据

        Returns:
            MongoBaseModel: 创建的文档对象
        """
        collection = mongo_client.db[cls.__name__.lower()]
        try:
            # 确保更新时间戳
            data["created_at"] = get_china_now()
            data["updated_at"] = get_china_now()

            result = await collection.insert_one(data)
            data["_id"] = str(result.inserted_id)

            logger.debug(f"Created document in {cls.__name__}: {result.inserted_id}")
            return cls(**data)
        except Exception as e:
            logger.error(f"Failed to create document in {cls.__name__}: {e}")
            raise

    @classmethod
    async def get(cls, mongo_client: MongoDBSDK, id: str) -> Optional["MongoBaseModel"]:
        """
        获取单个文档

        Args:
            mongo_client: MongoDB客户端
            id: 文档ID

        Returns:
            Optional[MongoBaseModel]: 文档对象,不存在则返回None
        """
        collection = mongo_client.db[cls.__name__.lower()]
        try:
            doc = await collection.find_one({"_id": ObjectId(id), "is_deleted": False})
            if doc:
                doc["_id"] = str(doc["_id"])
                return cls(**doc)
            return None
        except Exception as e:
            logger.error(f"Failed to get document from {cls.__name__}: {e}")
            raise

    async def update(self, mongo_client: MongoDBSDK, data: Dict[str, Any]) -> bool:
        """
        更新文档

        Args:
            mongo_client: MongoDB客户端
            data: 更新的数据

        Returns:
            bool: 更新是否成功
        """
        if not self.id:
            raise ValueError("Document ID is required for update")

        collection = mongo_client.db[self.__class__.__name__.lower()]
        try:
            # 更新时间戳
            data["updated_at"] = get_china_now()

            result = await collection.update_one(
                {"_id": ObjectId(self.id), "is_deleted": False}, {"$set": data}
            )
            success = result.modified_count > 0
            if success:
                # 更新实例属性
                for key, value in data.items():
                    setattr(self, key, value)
                logger.debug(
                    f"Updated document in {self.__class__.__name__}: {self.id}"
                )
            return success
        except Exception as e:
            logger.error(f"Failed to update document in {self.__class__.__name__}: {e}")
            raise

    async def delete(self, mongo_client: MongoDBSDK) -> bool:
        """
        软删除文档

        Args:
            mongo_client: MongoDB客户端

        Returns:
            bool: 删除是否成功
        """
        if not self.id:
            raise ValueError("Document ID is required for delete")

        collection = mongo_client.db[self.__class__.__name__.lower()]
        try:
            result = await collection.update_one(
                {"_id": ObjectId(self.id), "is_deleted": False},
                {"$set": {"is_deleted": True, "updated_at": get_china_now()}},
            )
            success = result.modified_count > 0
            if success:
                self.is_deleted = True
                self.updated_at = get_china_now()
                logger.debug(
                    f"Soft deleted document from {self.__class__.__name__}: {self.id}"
                )
            return success
        except Exception as e:
            logger.error(
                f"Failed to delete document from {self.__class__.__name__}: {e}"
            )
            raise

    @classmethod
    async def list(
        cls,
        mongo_client: MongoDBSDK,
        filter_dict: Dict[str, Any] = None,
        skip: int = 0,
        limit: int = 100,
    ) -> List["MongoBaseModel"]:
        """
        列出符合条件的文档

        Args:
            mongo_client: MongoDB客户端
            filter_dict: 过滤条件
            skip: 跳过的文档数
            limit: 返回的最大文档数

        Returns:
            List[MongoBaseModel]: 文档对象列表
        """
        collection = mongo_client.db[cls.__name__.lower()]
        try:
            # 添加未删除过滤条件
            filter_dict = filter_dict or {}
            filter_dict["is_deleted"] = False

            cursor = collection.find(filter_dict).skip(skip).limit(limit)
            documents = await cursor.to_list(length=None)

            # 转换ID为字符串
            for doc in documents:
                doc["_id"] = str(doc["_id"])

            return [cls(**doc) for doc in documents]
        except Exception as e:
            logger.error(f"Failed to list documents from {cls.__name__}: {e}")
            raise
