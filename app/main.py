from fastapi import FastAPI

from app.middlewares.request_id import RequestIDMiddleware
from app.middlewares.request_timer import RequestTimerMiddleware
from app.routers import conversation_router
from app.routers.llm_router import router as llm_router
from app.routers.memory_router import router as memory_router
from app.routers.person_router import router as person_router
from app.routers.tool_router import router as tool_router

app = FastAPI()
app.add_middleware(RequestIDMiddleware)
app.add_middleware(RequestTimerMiddleware)

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
