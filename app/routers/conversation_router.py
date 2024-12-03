from typing import Optional, Literal

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
async def list_conversations(
    current_user: CurrentUser, page: int = 1, limit: int = 100
):
    """获取所有会话"""
    conversations = await Conversation.list(
        filter_dict={
            "members": current_user.id,
            "is_deleted": False,
        },
        skip=(page - 1) * limit,
        limit=limit,
    )
    # TODO: 这里得按最后一条消息的时间降序排列
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
async def create_conversation(
    payload: CreateConversationPayload, current_user: CurrentUser
):
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


class RenameConversationPayload(BaseModel):
    name: str = Field(..., description="新的会话名称")


@router.put("/{conversation_id}/name", response_model=ResponseModel)
async def rename_conversation(conversation_id: str, payload: RenameConversationPayload):
    """重命名会话"""
    try:
        success = await Conversation.update_by_id(
            id=conversation_id, data={"name": payload.name}
        )
        message = "Conversation renamed successfully"
    except Exception as e:
        success = False
        message = str(e)
    return ResponseModel(success=success, data={}, message=message)


class UpdateMembersPayload(BaseModel):
    member_id: str = Field(..., description="成员ID")




@router.post("/{conversation_id}/members", response_model=ResponseModel)
async def add_conversation_member(conversation_id: str, payload: UpdateMembersPayload):
    """添加会话成员"""
    conversation = await Conversation.get_by_id(conversation_id)
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")

    # 检查成员是否存在
    if not await Person.get_by_id(payload.member_id):
        raise HTTPException(
            status_code=404, detail=f"Member {payload.member_id} not found"
        )

    members = set(conversation.members)
    members.add(payload.member_id)

    success = await Conversation.update_by_id(
        id=conversation_id, data={"members": list(members)}
    )
    return ResponseModel(success=success, data={}, message="Member added successfully")


@router.delete("/{conversation_id}/members/{member_id}", response_model=ResponseModel)
async def remove_conversation_member(conversation_id: str, member_id: str):
    """移除会话成员"""
    conversation = await Conversation.get_by_id(conversation_id)
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")

    members = set(conversation.members)
    if member_id not in members:
        raise HTTPException(status_code=404, detail="Member not in conversation")

    members.remove(member_id)
    if len(members) < 1:
        raise HTTPException(status_code=400, detail="Cannot remove last member")

    success = await Conversation.update_by_id(
        id=conversation_id, data={"members": list(members)}
    )
    return ResponseModel(
        success=success, data={}, message="Member removed successfully"
    )


@router.delete("/{conversation_id}", response_model=ResponseModel)
async def delete_conversation(conversation_id: str):
    """删除会话"""
    success = await Conversation.delete_by_id(conversation_id)
    return ResponseModel(
        success=success,
        data={"id": conversation_id},
        message="Conversation deleted successfully",
    )


class CreateMessagePayload(BaseModel):
    receiver_id: str = Field(..., description="接收者ID")
    message_type: Literal["text", "image", "video", "file"] = Field(..., description="消息类型")
    content: Optional[str] = Field(None, description="消息内容")
    media_url: Optional[str] = Field(None, description="媒体链接")
    metadata: Optional[dict] = Field(None, description="元数据")


@router.put("/{conversation_id}/messages", response_model=ResponseModel)
async def create_message(
    conversation_id: str,
    payload: CreateMessagePayload,
    current_user: CurrentUser
):
    """向会话发送新消息"""
    # 验证会话是否存在
    conversation = await Conversation.get_by_id(conversation_id)
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")
    
    # 验证发送者是否在会话成员中
    if current_user.id not in conversation.members:
        raise HTTPException(status_code=403, detail="You are not a member of this conversation")
    
    # 验证接收者是否存在且在会话成员中
    if current_user.id == payload.receiver_id:
        raise HTTPException(status_code=400, detail="You cannot send message to yourself")
    if not await Person.get_by_id(payload.receiver_id):
        raise HTTPException(status_code=404, detail="Receiver not found")
    if payload.receiver_id not in conversation.members:
        raise HTTPException(status_code=400, detail="Receiver is not a member of this conversation")
    
    # 创建新消息
    message_data = {
        "conversation_id": conversation_id,
        "sender_id": current_user.id,
        "receiver_id": payload.receiver_id,
        "message_type": payload.message_type,
        "content": payload.content,
        "media_url": payload.media_url,
        "metadata": payload.metadata,
    }
    
    try:
        new_message = await Message.create(**message_data)
        return ResponseModel(
            success=True,
            data=new_message.model_dump(by_alias=False),
            message="Message sent successfully"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to send message: {str(e)}")
