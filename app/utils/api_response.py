from pydantic import BaseModel


class ResponseModel(BaseModel):
    success: bool
    message: str | None = None
    data: dict | list | None = None
