from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.responses import JSONResponse
from starlette.middleware.exceptions import ExceptionMiddleware

from app.middlewares.auth import AuthMiddleware
from app.middlewares.request_id import RequestIDMiddleware
from app.middlewares.request_timer import RequestTimerMiddleware
from app.routers import conversation_router
from app.routers.llm_router import router as llm_router
from app.routers.memory_router import router as memory_router
from app.routers.person_router import router as person_router
from app.routers.tool_router import router as tool_router

app = FastAPI()


# 异常处理器
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={"success": False, "message": exc.detail, "data": None},
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return JSONResponse(
        status_code=422,
        content={"success": False, "message": str(exc), "data": None},
    )


# 中间件注册（注意顺序：从内到外）
app.add_middleware(GZipMiddleware)  # 最内层，压缩响应
app.add_middleware(
    CORSMiddleware,  # 处理跨域
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(AuthMiddleware)  # 处理认证
app.add_middleware(RequestIDMiddleware)  # 添加请求ID
app.add_middleware(RequestTimerMiddleware)  # 记录所有请求
app.add_middleware(
    ExceptionMiddleware, handlers=app.exception_handlers
)  # 最外层，处理所有异常

app.include_router(llm_router, prefix="/api/llms", tags=["LLMs"])
app.include_router(memory_router, prefix="/api/memories", tags=["Memories"])
app.include_router(person_router, prefix="/api/persons", tags=["Persons"])
app.include_router(tool_router, prefix="/api/tools", tags=["Tools"])
app.include_router(
    conversation_router.router, prefix="/api/conversations", tags=["conversations"]
)


@app.get("/")
def read_root():
    return {"message": "Welcome to LingVerse!"}
