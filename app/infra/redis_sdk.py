from typing import Any, Optional, Union

import aioredis

from app.utils.logger import get_logger

logger = get_logger(__name__)


class RedisSDK:
    def __init__(self, url: str):
        """
        初始化 Redis 客户端

        Args:
            url: Redis 连接 URL，格式如: "redis://localhost:6379/0"
        """
        self.url = url
        self.client: Optional[aioredis.Redis] = None

    async def connect(self):
        """建立连接"""
        try:
            self.client = await aioredis.from_url(
                self.url, encoding="utf-8", decode_responses=True
            )
            await self.client.ping()
            logger.info("Successfully connected to Redis")
        except Exception as e:
            logger.error(f"Failed to connect to Redis: {e}")
            raise

    async def close(self):
        """关闭连接"""
        if self.client:
            await self.client.close()
            logger.info("Redis connection closed")

    async def set(
        self,
        key: str,
        value: Any,
        ex: Optional[int] = None,
        nx: bool = False,
        xx: bool = False,
    ):
        """
        设置键值对

        Args:
            key: 键
            value: 值
            ex: 过期时间（秒）
            nx: 如果设置为True，则只有键不存在时才进行设置
            xx: 如果设置为True，则只有键已经存在时才进行设置
        """
        try:
            await self.client.set(key, value, ex=ex, nx=nx, xx=xx)
            logger.debug(f"Successfully set key: {key}")
        except Exception as e:
            logger.error(f"Failed to set key {key}: {e}")
            raise

    async def get(self, key: str) -> Any:
        """
        获取键值

        Args:
            key: 键

        Returns:
            键对应的值，如果键不存在则返回None
        """
        try:
            value = await self.client.get(key)
            return value
        except Exception as e:
            logger.error(f"Failed to get key {key}: {e}")
            raise

    async def delete(self, key: Union[str, list[str]]):
        """
        删除键

        Args:
            key: 单个键或键列表
        """
        try:
            await self.client.delete(key)
            logger.debug(f"Successfully deleted key(s): {key}")
        except Exception as e:
            logger.error(f"Failed to delete key(s) {key}: {e}")
            raise

    async def exists(self, key: str) -> bool:
        """
        检查键是否存在

        Args:
            key: 键

        Returns:
            布尔值，表示键是否存在
        """
        try:
            return await self.client.exists(key) > 0
        except Exception as e:
            logger.error(f"Failed to check existence of key {key}: {e}")
            raise
