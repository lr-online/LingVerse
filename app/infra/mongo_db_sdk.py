from typing import Any, List, Optional, Union

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

from app.utils.logger import get_logger

logger = get_logger(__name__)


class MongoDBSDK:
    def __init__(
        self,
        host: str = "localhost",
        port: int = 27017,
        username: Optional[str] = None,
        password: Optional[str] = None,
        database: str = "test",
    ):
        """
        初始化 MongoDB 客户端

        Args:
            host: MongoDB 主机地址
            port: MongoDB 端口
            username: 用户名（可选）
            password: 密码（可选）
            database: 数据库名
        """
        self.uri = self._build_uri(host, port, username, password)
        self.client: Optional[AsyncIOMotorClient] = None
        self.db: Optional[AsyncIOMotorDatabase] = None
        self.database_name = database

    def _build_uri(
        self, host: str, port: int, username: Optional[str], password: Optional[str]
    ) -> str:
        """构建 MongoDB 连接 URI"""
        if username and password:
            return f"mongodb://{username}:{password}@{host}:{port}"
        return f"mongodb://{host}:{port}"

    async def connect(self) -> None:
        """建立连接"""
        try:
            self.client = AsyncIOMotorClient(self.uri)
            self.db = self.client[self.database_name]
            # 验证连接
            await self.client.admin.command("ping")
            logger.info("Successfully connected to MongoDB")
        except Exception as e:
            logger.error(f"Failed to connect to MongoDB: {e}")
            raise

    async def close(self) -> None:
        """关闭连接"""
        if self.client:
            self.client.close()
            logger.info("MongoDB connection closed")

    async def insert_one(self, collection: str, document: dict) -> str:
        """
        插入单个文档

        Args:
            collection: 集合名称
            document: 要插入的文档

        Returns:
            插入文档的ID
        """
        try:
            result = await self.db[collection].insert_one(document)
            logger.debug(f"Document inserted successfully: {result.inserted_id}")
            return str(result.inserted_id)
        except Exception as e:
            logger.error(f"Failed to insert document: {e}")
            raise

    async def insert_many(self, collection: str, documents: List[dict]) -> List[str]:
        """
        插入多个文档

        Args:
            collection: 集合名称
            documents: 要插入的文档列表

        Returns:
            插入文档的ID列表
        """
        try:
            result = await self.db[collection].insert_many(documents)
            return [str(id) for id in result.inserted_ids]
        except Exception as e:
            logger.error(f"Failed to insert documents: {e}")
            raise

    async def find_one(
        self, collection: str, filter: dict, projection: dict = None
    ) -> Optional[dict]:
        """
        查找单个文档

        Args:
            collection: 集合名称
            filter: 查询条件
            projection: 投影条件

        Returns:
            查询结果文档，如果没有找到则返回None
        """
        try:
            result = await self.db[collection].find_one(filter, projection)
            return result
        except Exception as e:
            logger.error(f"Failed to find document: {e}")
            raise

    async def find_many(
        self,
        collection: str,
        filter: dict,
        projection: dict = None,
        sort: List[tuple] = None,
        limit: int = 0,
        skip: int = 0,
    ) -> List[dict]:
        """
        查找多个文档

        Args:
            collection: 集合名称
            filter: 查询条件
            projection: 投影条件
            sort: 排序条件，格式为 [(field_name, direction)]
            limit: 限制返回的文档数量
            skip: 跳过的文档数量

        Returns:
            查询结果文档列表
        """
        try:
            cursor = self.db[collection].find(filter, projection)

            if sort:
                cursor = cursor.sort(sort)
            if skip:
                cursor = cursor.skip(skip)
            if limit:
                cursor = cursor.limit(limit)

            return await cursor.to_list(length=None)
        except Exception as e:
            logger.error(f"Failed to find documents: {e}")
            raise

    async def update_one(
        self, collection: str, filter: dict, update: dict, upsert: bool = False
    ) -> dict:
        """
        更新单个文档

        Args:
            collection: 集合名称
            filter: 查询条件
            update: 更新操作
            upsert: 如果文档不存在是否插入

        Returns:
            更新结果
        """
        try:
            result = await self.db[collection].update_one(filter, update, upsert=upsert)
            return {
                "matched_count": result.matched_count,
                "modified_count": result.modified_count,
                "upserted_id": str(result.upserted_id) if result.upserted_id else None,
            }
        except Exception as e:
            logger.error(f"Failed to update document: {e}")
            raise

    async def update_many(
        self, collection: str, filter: dict, update: dict, upsert: bool = False
    ) -> dict:
        """
        更新多个文档

        Args:
            collection: 集合名称
            filter: 查询条件
            update: 更新操作
            upsert: 如果文档不存在是否插入

        Returns:
            更新结果
        """
        try:
            result = await self.db[collection].update_many(
                filter, update, upsert=upsert
            )
            return {
                "matched_count": result.matched_count,
                "modified_count": result.modified_count,
                "upserted_id": str(result.upserted_id) if result.upserted_id else None,
            }
        except Exception as e:
            logger.error(f"Failed to update documents: {e}")
            raise

    async def delete_one(self, collection: str, filter: dict) -> int:
        """
        删除单个文档

        Args:
            collection: 集合名称
            filter: 查询条件

        Returns:
            删除的文档数量
        """
        try:
            result = await self.db[collection].delete_one(filter)
            return result.deleted_count
        except Exception as e:
            logger.error(f"Failed to delete document: {e}")
            raise

    async def delete_many(self, collection: str, filter: dict) -> int:
        """
        删除多个文档

        Args:
            collection: 集合名称
            filter: 查询条件

        Returns:
            删除的文档数量
        """
        try:
            result = await self.db[collection].delete_many(filter)
            return result.deleted_count
        except Exception as e:
            logger.error(f"Failed to delete documents: {e}")
            raise

    async def count_documents(self, collection: str, filter: dict) -> int:
        """
        统计文档数量

        Args:
            collection: 集合名称
            filter: 查询条件

        Returns:
            符合条件的文档数量
        """
        try:
            return await self.db[collection].count_documents(filter)
        except Exception as e:
            logger.error(f"Failed to count documents: {e}")
            raise

    async def create_index(self, collection: str, keys: List[tuple], **kwargs) -> str:
        """
        创建索引

        Args:
            collection: 集合名称
            keys: 索引键列表，格式为 [(field_name, direction)]
            **kwargs: 其他索引选项

        Returns:
            创建的索引名称
        """
        try:
            return await self.db[collection].create_index(keys, **kwargs)
        except Exception as e:
            logger.error(f"Failed to create index: {e}")
            raise
