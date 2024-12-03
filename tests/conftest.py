import asyncio
import pytest
from fastapi.testclient import TestClient
from typing import AsyncGenerator, Generator

from app.main import app
from app.models.person import Person


@pytest.fixture(scope="session")
def event_loop() -> Generator:
    """创建事件循环"""
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="function")
def client() -> Generator:
    """创建测试客户端"""
    with TestClient(app) as client:
        yield client


@pytest.fixture(scope="function")
async def admin_token() -> AsyncGenerator[str, None]:
    """创建管理员用户并返回 token"""
    admin = await Person.create(
        name="test_admin",
        role="admin",
        access_token="admin_test_token",
    )
    yield admin.access_token
    await Person.delete_by_id(admin.id)


@pytest.fixture(scope="function")
async def user_token() -> AsyncGenerator[str, None]:
    """创建普通用户并返回 token"""
    user = await Person.create(
        name="test_user",
        role="human",
        access_token="user_test_token",
    )
    yield user.access_token
    await Person.delete_by_id(user.id) 