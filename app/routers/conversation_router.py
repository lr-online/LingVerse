from typing import Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from pydantic.v1 import validator

from app.dependencies.auth import CurrentUser
from app.models.conversation import Conversation
from app.models.message import Message
from app.models.person import Person
from app.utils.api_response import ResponseModel

router = APIRouter()


@router.get("", response_model=ResponseModel)
async def list_conversations(current_user: CurrentUser, page: int = 1, limit: int = 100):
    """获取所有会话"""
    conversations = await Conversation.list(
        filter_dict={
            "members": current_user.id,
            "is_deleted": False,
        },
        skip=(page - 1) * limit, limit=limit
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


class CreateConversationPayload(BaseModel):
    name: str = Field("新会话", description="对话名称")
    members: Optional[set[str]] = Field(None, description="对话成员的ID列表")

    @validator("members")
    def validate_members(cls, members):
        members = members or set()
        if len(members) < 1:
            raise ValueError("At least one member is required")
        return members


@router.post("", response_model=ResponseModel)
async def create_conversation(payload: CreateConversationPayload, current_user: CurrentUser):
    """创建会话"""
    payload.members.add(current_user.id)

    # 确保所有的member都存在
    for member_id in payload.members:
        if not await Person.get_by_id(member_id):
            raise HTTPException(status_code=404, detail=f"Member {member_id} not found")

    # 创建会话
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
