import uuid

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

from app.utils.request_id import reset_request_id, set_request_id


class RequestIDMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # 从请求头中获取请求 ID，如果没有则生成新的
        request_id = request.headers.get("X-Request-ID") or uuid.uuid4().hex
        set_request_id(request_id)

        try:
            response = await call_next(request)
            # 将请求 ID 添加到响应头
            if request_id:  # 只在有 request_id 时设置响应头
                response.headers["X-Request-ID"] = request_id
            return response
        finally:
            # 请求结束后重置请求 ID
            reset_request_id()
