import pytest
from fastapi.testclient import TestClient


@pytest.mark.asyncio
async def test_list_conversations(client: TestClient, user_token: str):
    """测试获取会话列表"""
    response = client.get(
        "/api/conversations",
        headers={"Authorization": user_token},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert isinstance(data["data"], list)


@pytest.mark.asyncio
async def test_create_conversation(client: TestClient, user_token: str):
    """测试创建会话"""
    response = client.post(
        "/api/conversations",
        headers={"Authorization": user_token},
        json={"name": "test conversation"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["data"]["name"] == "test conversation"
    return data["data"]["id"]


async def test_get_conversation(client: TestClient, user_token: str):
    """测试获取单个会话"""
    # 先创建一个会话
    conversation_id = await test_create_conversation(client, user_token)
    
    response = client.get(
        f"/api/conversations/{conversation_id}",
        headers={"Authorization": user_token},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["data"]["conversation"]["id"] == conversation_id


async def test_update_conversation(client: TestClient, user_token: str):
    """测试更新会话"""
    # 先创建一个会话
    conversation_id = await test_create_conversation(client, user_token)
    
    response = client.put(
        f"/api/conversations/{conversation_id}",
        headers={"Authorization": user_token},
        json={"name": "updated conversation"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True


async def test_delete_conversation(client: TestClient, user_token: str):
    """测试删除会话"""
    # 先创建一个会话
    conversation_id = await test_create_conversation(client, user_token)
    
    response = client.delete(
        f"/api/conversations/{conversation_id}",
        headers={"Authorization": user_token},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True 