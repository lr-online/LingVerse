import pytest
from fastapi.testclient import TestClient


@pytest.mark.asyncio
async def test_list_llm(client: TestClient, user_token: str):
    """测试获取模型列表"""
    response = client.get(
        "/api/llms",
        headers={"Authorization": user_token},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert isinstance(data["data"], list)


@pytest.mark.asyncio
async def test_get_llm(client: TestClient, user_token: str):
    """测试获取单个模型"""
    response = client.get(
        "/api/llms/gpt-4",
        headers={"Authorization": user_token},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["data"]["model_name"] == "gpt-4"


@pytest.mark.asyncio
async def test_sync_llm_models(client: TestClient, admin_token: str, user_token: str):
    """测试同步模型列表"""
    # 测试普通用户无权限
    response = client.post(
        "/api/llms/sync",
        headers={"Authorization": user_token},
    )
    assert response.status_code == 403

    # 测试管理员可以同步
    response = client.post(
        "/api/llms/sync",
        headers={"Authorization": admin_token},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
