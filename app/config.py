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


class RedisSettings(BaseModel):
    host: str = "localhost"
    port: int = 6379
    password: Optional[str] = None


class ElasticsearchSettings(BaseModel):
    host: str = "localhost" 
    port: int = 9200
    username: Optional[str] = None
    password: Optional[str] = None


class Settings(BaseSettings):
    """应用配置"""
    mongodb: MongoDBSettings = MongoDBSettings()
    redis: RedisSettings = RedisSettings()
    elasticsearch: ElasticsearchSettings = ElasticsearchSettings()

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        env_nested_delimiter="_",
    )


@lru_cache
def get_settings() -> Settings:
    """获取应用配置（使用缓存）"""
    return Settings()


if __name__ == "__main__":
    settings = get_settings()
    print(f"MongoDB 配置:")
    print(f"- password: {settings.mongodb.password}")
    print(f"- host: {settings.mongodb.host}")
    print(f"- database: {settings.mongodb.database}")
    print(f"Redis 配置:")
    print(f"- password: {settings.redis.password}")
    print(f"Elasticsearch 配置:")
    print(f"- password: {settings.elasticsearch.password}")
