from fastapi import HTTPException, Request
from starlette.middleware.base import BaseHTTPMiddleware

from app.models.person import Person
from app.utils.logger import get_logger

logger = get_logger(__name__)


class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # 跳过根路径的认证
        if request.url.path == "/":
            return await call_next(request)

        # 获取 access_token
        access_token = request.headers.get("Authorization")
        if not access_token:
            logger.warning("Missing access token")
            raise HTTPException(status_code=401, detail="Missing access token")
        # 验证 access_token
        person = await Person.get_by_single_field("access_token", access_token)
        if not person or person.is_deleted or person.role not in ("admin", "human"):
            logger.warning(f"Invalid access token or unauthorized user: {access_token}")
            raise HTTPException(
                status_code=401, detail="Invalid access token or unauthorized user"
            )

        # 将验证通过的用户信息添加到请求状态中
        request.state.person = person

        return await call_next(request)
