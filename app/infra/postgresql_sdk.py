from typing import Any, List, Optional, Union

import asyncpg
from asyncpg import Connection, Pool

from app.utils.logger import get_logger

logger = get_logger(__name__)


class PostgreSQLSDK:
    def __init__(
        self,
        host: str,
        port: int,
        user: str,
        password: str,
        database: str,
        min_size: int = 10,
        max_size: int = 10,
    ):
        """
        初始化 PostgreSQL 连接池

        Args:
            host: 数据库主机
            port: 数据库端口
            user: 用户名
            password: 密码
            database: 数据库名
            min_size: 连接池最小连接数
            max_size: 连接池最大连接数
        """
        self.dsn = f"postgresql://{user}:{password}@{host}:{port}/{database}"
        self.pool: Optional[Pool] = None
        self.min_size = min_size
        self.max_size = max_size

    async def connect(self) -> None:
        """建立连接池"""
        try:
            self.pool = await asyncpg.create_pool(
                dsn=self.dsn,
                min_size=self.min_size,
                max_size=self.max_size,
            )
            logger.info("Successfully connected to PostgreSQL")
        except Exception as e:
            logger.error(f"Failed to connect to PostgreSQL: {e}")
            raise

    async def close(self) -> None:
        """关闭连接池"""
        if self.pool:
            await self.pool.close()
            logger.info("PostgreSQL connection pool closed")

    async def execute(self, query: str, *args, timeout: Optional[float] = None) -> str:
        """
        执行SQL语句

        Args:
            query: SQL查询语句
            *args: 查询参数
            timeout: 超时时间（秒）

        Returns:
            执行结果
        """
        try:
            async with self.pool.acquire() as conn:
                return await conn.execute(query, *args, timeout=timeout)
        except Exception as e:
            logger.error(f"Failed to execute query: {e}\nQuery: {query}\nArgs: {args}")
            raise

    async def fetch(
        self, query: str, *args, timeout: Optional[float] = None
    ) -> List[asyncpg.Record]:
        """
        执行查询并返回所有结果

        Args:
            query: SQL查询语句
            *args: 查询参数
            timeout: 超时时间（秒）

        Returns:
            查询结果列表
        """
        try:
            async with self.pool.acquire() as conn:
                return await conn.fetch(query, *args, timeout=timeout)
        except Exception as e:
            logger.error(f"Failed to fetch: {e}\nQuery: {query}\nArgs: {args}")
            raise

    async def fetchrow(
        self, query: str, *args, timeout: Optional[float] = None
    ) -> Optional[asyncpg.Record]:
        """
        执行查询并返回第一行结果

        Args:
            query: SQL查询语句
            *args: 查询参数
            timeout: 超时时间（秒）

        Returns:
            查询结果的第一行，如果没有结果则返回None
        """
        try:
            async with self.pool.acquire() as conn:
                return await conn.fetchrow(query, *args, timeout=timeout)
        except Exception as e:
            logger.error(f"Failed to fetchrow: {e}\nQuery: {query}\nArgs: {args}")
            raise

    async def fetchval(
        self, query: str, *args, column: int = 0, timeout: Optional[float] = None
    ) -> Any:
        """
        执行查询并返回第一个值

        Args:
            query: SQL查询语句
            *args: 查询参数
            column: 要返回的列索引
            timeout: 超时时间（秒）

        Returns:
            查询结果的第一个值
        """
        try:
            async with self.pool.acquire() as conn:
                return await conn.fetchval(query, *args, column=column, timeout=timeout)
        except Exception as e:
            logger.error(f"Failed to fetchval: {e}\nQuery: {query}\nArgs: {args}")
            raise

    async def transaction(self) -> Connection:
        """
        获取事务上下文管理器

        Returns:
            异步上下文管理器，用于事务操作
        """
        return self.pool.acquire()

    async def execute_many(
        self, query: str, args: List[tuple], timeout: Optional[float] = None
    ) -> None:
        """
        批量执行SQL语句

        Args:
            query: SQL查询语句
            args: 参数列表，每个元素是一个元组
            timeout: 超时时间（秒）
        """
        try:
            async with self.pool.acquire() as conn:
                await conn.executemany(query, args, timeout=timeout)
        except Exception as e:
            logger.error(f"Failed to execute many: {e}\nQuery: {query}\nArgs: {args}")
            raise
