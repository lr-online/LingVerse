import time

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

from app.utils.logger import get_logger

logger = get_logger(__name__)


class RequestTimerMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # 记录请求开始时间
        start_time = time.time()

        # 记录请求信息
        logger.info(f"Request started: {request.method} {request.url.path}")

        try:
            # 处理请求
            response = await call_next(request)

            # 计算耗时
            process_time = (time.time() - start_time) * 1000  # 转换为毫秒

            # 记录请求完成信息
            logger.info(
                f"Request completed: {request.method} {request.url.path} {response.status_code} {process_time:.2f}ms"
            )

            # 在响应头中添加处理时间
            response.headers["X-Process-Time"] = f"{process_time:.2f}ms"
            return response

        except Exception as e:
            # 记录请求失败信息
            process_time = (time.time() - start_time) * 1000
            logger.error(
                f"Request failed: {request.method} {request.url.path} "
                f"- Error: {str(e)} "
                f"- Duration: {process_time:.2f}ms"
            )
            raise
