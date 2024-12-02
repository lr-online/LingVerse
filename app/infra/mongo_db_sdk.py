from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

from app.utils.config import get_settings
from app.utils.logger import get_logger

logger = get_logger(__name__)


class MongoDBSDK:
    cfg = mongo_config = get_settings().mongodb

    uri = (
        f"mongodb://{cfg.username}:{cfg.password}@{cfg.host}:{cfg.port}"
        if cfg.username and cfg.password
        else f"mongodb://{cfg.host}:{cfg.port}"
    )
    client: AsyncIOMotorClient = AsyncIOMotorClient(uri)
    db: AsyncIOMotorDatabase = client[mongo_config.database]

    logger.info(f"Connected to MongoDB: {uri}")
