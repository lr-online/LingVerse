from functools import lru_cache
from typing import Optional

from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


class MongoDBSettings(BaseModel):
    host: str = "localhost"
    port: int = 27017
    username: Optional[str] = None
    password: Optional[str] = None
    database: str = "lingverse"

    model_config = SettingsConfigDict(env_prefix="MONGODB_")


class RedisSettings(BaseModel):
    host: str = "localhost"
    port: int = 6379
    password: Optional[str] = None

    model_config = SettingsConfigDict(env_prefix="REDIS_")


class ElasticsearchSettings(BaseModel):
    host: str = "localhost"
    port: int = 9200
    username: Optional[str] = None
    password: Optional[str] = None

    model_config = SettingsConfigDict(env_prefix="ELASTICSEARCH_")


class Settings(BaseSettings):
    """应用配置"""

    # MongoDB 配置
    mongodb: MongoDBSettings = MongoDBSettings()

    # Redis 配置
    redis: RedisSettings = RedisSettings()

    # Elasticsearch 配置
    elasticsearch: ElasticsearchSettings = ElasticsearchSettings()

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_nested_delimiter="_",  # 修改分隔符为下划线
        case_sensitive=False,
    )


@lru_cache
def get_settings() -> Settings:
    """获取应用配置（使用缓存）"""
    return Settings()


if __name__ == "__main__":
    settings = get_settings()
    print(f"MongoDB settings: {settings.mongodb}")
    print(f"Redis settings: {settings.redis}")
    print(f"Elasticsearch settings: {settings.elasticsearch}")
