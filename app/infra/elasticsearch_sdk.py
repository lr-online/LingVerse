from elasticsearch import AsyncElasticsearch

from app.utils.logger import get_logger

logger = get_logger(__name__)


class ElasticsearchSDK:
    def __init__(self, hosts: list[str], **kwargs):
        """
        初始化 Elasticsearch 客户端

        Args:
            hosts: Elasticsearch 服务器地址列表
            **kwargs: 其他 Elasticsearch 客户端参数
        """
        self.client = AsyncElasticsearch(hosts=hosts, **kwargs)

    async def connect(self):
        """建立连接"""
        try:
            await self.client.info()
            logger.info("Successfully connected to Elasticsearch")
        except Exception as e:
            logger.error(f"Failed to connect to Elasticsearch: {e}")
            raise

    async def close(self):
        """关闭连接"""
        await self.client.close()
        logger.info("Elasticsearch connection closed")

    async def create_index(self, index: str, body: dict = None):
        """
        创建索引

        Args:
            index: 索引名称
            body: 索引配置
        """
        try:
            await self.client.indices.create(index=index, body=body)
            logger.info(f"Index {index} created successfully")
        except Exception as e:
            logger.error(f"Failed to create index {index}: {e}")
            raise

    async def index_document(self, index: str, document: dict, id: str = None):
        """
        索引文档

        Args:
            index: 索引名称
            document: 文档内容
            id: 文档ID（可选）
        """
        try:
            result = await self.client.index(index=index, body=document, id=id)
            logger.debug(f"Document indexed successfully: {result}")
            return result
        except Exception as e:
            logger.error(f"Failed to index document: {e}")
            raise

    async def search(self, index: str, query: dict):
        """
        搜索文档

        Args:
            index: 索引名称
            query: 查询条件
        """
        try:
            result = await self.client.search(index=index, body=query)
            return result
        except Exception as e:
            logger.error(f"Search failed: {e}")
            raise
