from datetime import datetime
from typing import Literal, Optional

from bson import ObjectId
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
    message_type: Literal["text", "image", "video", "file"] = Field(
        ..., description="消息类型"
    )
    content: Optional[str] = Field(None, description="消息内容")
    media_url: Optional[str] = Field(None, description="媒体链接")
    metadata: Optional[dict] = Field(None, description="元数据")


@router.put("/{conversation_id}/messages", response_model=ResponseModel)
async def create_message(
    conversation_id: str, payload: CreateMessagePayload, current_user: CurrentUser
):
    """向会话发送新消息"""
    # 验证会话是否存在
    conversation = await Conversation.get_by_id(conversation_id)
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")

    # 验证发送者是否在会话成员中
    if current_user.id not in conversation.members:
        raise HTTPException(
            status_code=403, detail="You are not a member of this conversation"
        )

    # 验证接收者是否存在且在会话成员中
    if current_user.id == payload.receiver_id:
        raise HTTPException(
            status_code=400, detail="You cannot send message to yourself"
        )
    if not await Person.get_by_id(payload.receiver_id):
        raise HTTPException(status_code=404, detail="Receiver not found")
    if payload.receiver_id not in conversation.members:
        raise HTTPException(
            status_code=400, detail="Receiver is not a member of this conversation"
        )

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
            message="Message sent successfully",
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to send message: {str(e)}")


class GetMessagesQuery(BaseModel):
    before: Optional[datetime] = Field(None, description="获取此时间之前的消息")
    after: Optional[datetime] = Field(None, description="获取此时间之后的消息")
    page: int = Field(1, ge=1, description="页码")
    limit: int = Field(20, ge=1, le=100, description="每页消息数量")


@router.get("/{conversation_id}/messages", response_model=ResponseModel)
async def list_conversation_messages(
    conversation_id: str,
    current_user: CurrentUser,
    before: Optional[datetime] = None,
    after: Optional[datetime] = None,
    page: int = 1,
    limit: int = 20,
):
    """获取会话消息列表

    Args:
        conversation_id: 会话ID
        before: 获取此时间之前的消息
        after: 获取此时间之后的消息
        page: 页码，从1开始
        limit: 每页消息数量，默认20，最大100
    """
    # 验证会话是否存在
    conversation = await Conversation.get_by_id(conversation_id)
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")

    # 验证用户是否在会话中
    if current_user.id not in conversation.members:
        raise HTTPException(
            status_code=403, detail="You are not a member of this conversation"
        )

    # 构建查询条件
    filter_dict = {"conversation_id": conversation_id, "is_deleted": False}

    # 添加时间范围条件
    if before or after:
        filter_dict["created_at"] = {}
        if before:
            filter_dict["created_at"]["$lt"] = before
        if after:
            filter_dict["created_at"]["$gt"] = after

    try:
        # 获取消息总数
        total = await Message.collection().count_documents(filter_dict)

        # 获取分页消息列表
        messages = await Message.list(
            filter_dict=filter_dict, skip=(page - 1) * limit, limit=limit
        )

        return ResponseModel(
            success=True,
            data={
                "messages": [
                    message.model_dump(by_alias=False) for message in messages
                ],
                "pagination": {
                    "total": total,
                    "page": page,
                    "limit": limit,
                    "pages": (total + limit - 1) // limit,
                },
            },
            message="Messages retrieved successfully",
        )
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to retrieve messages: {str(e)}"
        )


class MarkMessagesReadPayload(BaseModel):
    before: Optional[datetime] = Field(
        None, description="标记此时间之前的所有消息为已读"
    )
    message_ids: Optional[list[str]] = Field(
        None, description="要标记为已读的消息ID列表"
    )

    @validator("message_ids", "before")
    def validate_at_least_one_field(cls, v, values):
        if not v and "before" not in values:
            raise ValueError("Either before or message_ids must be provided")
        return v


@router.put("/{conversation_id}/messages/read", response_model=ResponseModel)
async def mark_messages_read(
    conversation_id: str,
    payload: MarkMessagesReadPayload,
    current_user: CurrentUser,
):
    """标记消息为已读

    支持两种模式：
    1. 通过 before 参数批量标记某个时间点之前的所有消息为已读
    2. 通过 message_ids 参数标记指定消息为已读
    """
    # 验证会话是否存在且用户是否在会话中
    conversation = await Conversation.get_by_id(conversation_id)
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")

    if current_user.id not in conversation.members:
        raise HTTPException(
            status_code=403, detail="You are not a member of this conversation"
        )

    try:
        # 构建基础查询条件
        base_filter = {
            "conversation_id": conversation_id,
            "receiver_id": current_user.id,  # 只标记发给自己的消息
            "is_read": False,  # 只更新未读消息
            "is_deleted": False,
        }

        update_data = {"is_read": True, "updated_at": datetime.now()}

        # 根据不同模式构建查询条件
        if payload.before:
            # 模式1: 标记时间点之前的所有消息
            filter_dict = {**base_filter, "created_at": {"$lt": payload.before}}
            result = await Message.collection().update_many(
                filter_dict, {"$set": update_data}
            )
            modified_count = result.modified_count

        else:
            # 模式2: 标记指定消息
            filter_dict = {
                **base_filter,
                "_id": {"$in": [ObjectId(mid) for mid in payload.message_ids]},
            }
            result = await Message.collection().update_many(
                filter_dict, {"$set": update_data}
            )
            modified_count = result.modified_count

        return ResponseModel(
            success=True,
            data={"modified_count": modified_count},
            message=f"Marked {modified_count} messages as read",
        )

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to mark messages as read: {str(e)}"
        )
