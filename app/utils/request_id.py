import contextvars
import uuid
from typing import Optional

# 创建一个 contextvars 变量来存储请求 ID
REQUEST_ID = contextvars.ContextVar("request_id", default=None)


def get_request_id() -> str:
    """获取当前请求 ID，如果不存在则创建新的"""
    request_id = REQUEST_ID.get()
    if request_id is None:
        request_id = uuid.uuid4().hex
        REQUEST_ID.set(request_id)
    return request_id


def set_request_id(request_id: Optional[str] = None) -> None:
    """设置请求 ID"""
    REQUEST_ID.set(request_id or uuid.uuid4().hex)


def reset_request_id() -> None:
    """重置请求 ID"""
    REQUEST_ID.set(None)
