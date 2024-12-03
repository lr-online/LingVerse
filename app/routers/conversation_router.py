from fastapi import APIRouter, HTTPException

from app.dependencies.auth import CurrentUser
from app.models.conversation import Conversation
from app.models.message import Message
from app.utils.api_response import ResponseModel

router = APIRouter()


@router.get("", response_model=ResponseModel)
async def list_conversations(page: int = 1, limit: int = 100):
    """获取所有会话"""
    conversations = await Conversation.list(
        filter_dict={}, skip=(page - 1) * limit, limit=limit
    )
    return ResponseModel(
        success=True,
        data=[
            conversation.model_dump(by_alias=False) for conversation in conversations
        ],
        message="Conversations retrieved successfully",
    )


@router.get("/{conversation_id}", response_model=ResponseModel)
async def get_conversation(conversation_id: str):
    """获取单个会话及其消息"""
    conversation = await Conversation.get_by_id(conversation_id)
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")

    # 获取会话相关的消息
    messages = await Message.list({"conversation_id": conversation_id}, limit=100)

    return ResponseModel(
        success=True,
        data={
            "conversation": conversation.model_dump(by_alias=False),
            "messages": [message.model_dump(by_alias=False) for message in messages],
        },
        message="Conversation retrieved successfully",
    )


@router.post("", response_model=ResponseModel)
async def create_conversation(payload: Conversation, current_user: CurrentUser):
    """创建会话"""
    payload.creator_id = current_user.id
    new_conversation = await Conversation.create(**payload.model_dump())
    return ResponseModel(
        success=True,
        data=new_conversation.model_dump(by_alias=False),
        message="Conversation created successfully",
    )


@router.put("/{conversation_id}", response_model=ResponseModel)
async def update_conversation(conversation_id: str, payload: Conversation):
    """更新会话信息"""
    try:
        success = await Conversation.update_by_id(
            id=conversation_id,
            data=payload.model_dump(
                exclude={"id", "created_at", "updated_at", "is_deleted"}
            ),
        )
        message = "Conversation updated successfully"
    except Exception as e:
        success = False
        message = str(e)
    return ResponseModel(success=success, data={}, message=message)


@router.delete("/{conversation_id}", response_model=ResponseModel)
async def delete_conversation(conversation_id: str):
    """删除会话"""
    success = await Conversation.delete_by_id(conversation_id)
    return ResponseModel(
        success=success,
        data={"id": conversation_id},
        message="Conversation deleted successfully",
    )
