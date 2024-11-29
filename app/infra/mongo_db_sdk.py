from typing import Any, List, Optional, Union

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

from app.utils.config import get_settings
from app.utils.logger import get_logger

logger = get_logger(__name__)


class MongoDBSDK:
    _instance = None
    client: Optional[AsyncIOMotorClient] = None
    db: Optional[AsyncIOMotorDatabase] = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            settings = get_settings()
            mongo_config = settings.mongodb

            # 构建连接 URI
            uri = cls._build_uri(
                host=mongo_config.host,
                port=mongo_config.port,
                username=mongo_config.username,
                password=mongo_config.password,
            )

            # 初始化客户端
            cls.client = AsyncIOMotorClient(uri)
            cls.db = cls.client[mongo_config.database]

            logger.info("MongoDB client initialized")

        return cls._instance

    @staticmethod
    def _build_uri(
        host: str, port: int, username: Optional[str], password: Optional[str]
    ) -> str:
        """构建 MongoDB 连接 URI"""
        if username and password:
            return f"mongodb://{username}:{password}@{host}:{port}"
        return f"mongodb://{host}:{port}"

    async def ping(self) -> bool:
        """测试连接是否正常"""
        try:
            await self.client.admin.command("ping")
            logger.info("Successfully connected to MongoDB")
            return True
        except Exception as e:
            logger.error(f"Failed to connect to MongoDB: {e}")
            return False

    async def close(self):
        """关闭连接"""
        if self.client:
            self.client.close()
            logger.info("MongoDB connection closed")

    async def insert_one(self, collection: str, document: dict) -> str:
        """插入单个文档"""
        try:
            result = await self.db[collection].insert_one(document)
            logger.debug(f"Document inserted successfully: {result.inserted_id}")
            return str(result.inserted_id)
        except Exception as e:
            logger.error(f"Failed to insert document: {e}")
            raise

    async def find_one(
        self, collection: str, filter: dict, projection: dict = None
    ) -> Optional[dict]:
        """查找单个文档"""
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
        """查找多个文档"""
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
        """更新单个文档"""
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

    async def delete_one(self, collection: str, filter: dict) -> int:
        """删除单个文档"""
        try:
            result = await self.db[collection].delete_one(filter)
            return result.deleted_count
        except Exception as e:
            logger.error(f"Failed to delete document: {e}")
            raise

    async def count_documents(self, collection: str, filter: dict) -> int:
        """统计文档数量"""
        try:
            return await self.db[collection].count_documents(filter)
        except Exception as e:
            logger.error(f"Failed to count documents: {e}")
            raise
