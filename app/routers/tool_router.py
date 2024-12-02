from fastapi import APIRouter, HTTPException, Path

from app.models.tool import Tool
from app.utils.api_response import ResponseModel

router = APIRouter()


@router.get("", response_model=ResponseModel)
async def list_tools():
    """获取所有工具"""
    tools = await Tool.list(skip=0, limit=100)
    return ResponseModel(
        success=True,
        data=[
            tool.model_dump(
                by_alias=False,
            )
            for tool in tools
        ],
        message="Tools retrieved successfully",
    )


@router.get("/{tool_id}", response_model=ResponseModel)
async def get_tool(tool_id: str):
    """获取单个工具"""
    tool = await Tool.get_by_id(tool_id)
    if not tool:
        raise HTTPException(status_code=404, detail="Tool not found")
    return ResponseModel(
        success=True,
        data=tool.model_dump(
            by_alias=False,
        ),
        message="Tool retrieved successfully",
    )


@router.post("")
async def create_tool(payload: Tool):
    """创建工具"""
    return HTTPException(status_code=403, detail="Tool creation is disabled")


@router.post("/{tool_id}/run")
async def call_tool(tool_id: str, payload: Tool):
    """调用工具"""
    return {}


@router.put("/{tool_id}")
async def update_tool(tool_id: str, payload: Tool):
    """更新工具"""
    return HTTPException(status_code=403, detail="Tool update is disabled")


@router.delete("/{tool_id}")
async def delete_tool(tool_id: str):
    """删除工具"""
    return HTTPException(status_code=403, detail="Tool deletion is disabled")
