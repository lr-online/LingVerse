from fastapi import APIRouter, HTTPException, Path

from app.models.llm_model import LLM
from app.utils.api_response import ResponseModel

router = APIRouter()


@router.get("", response_model=ResponseModel)
async def list_llm():
    """获取所有大语言模型"""
    all_llm = await LLM.list(skip=0, limit=100)
    return ResponseModel(
        success=True,
        data=[
            model.model_dump(
                exclude={"api_key", "base_url"},
                by_alias=False,
            )
            for model in all_llm
        ],
        message="LLMs retrieved successfully",
    )


@router.get("/{llm_name}", response_model=ResponseModel)
async def get_llm(llm_name: str = Path(..., description="大语言模型名称")):
    """获取单个大语言模型"""
    llm = await LLM.get_by_single_field("model_name", llm_name)
    if not llm:
        raise HTTPException(status_code=404, detail="LLM not found")
    return ResponseModel(
        success=True,
        data=llm.model_dump(
            exclude={"api_key", "base_url"},
            by_alias=False,
        ),
        message="LLMs retrieved successfully",
    )


@router.post("")
async def create_llm(llm: LLM):
    """创建大语言模型"""
    return HTTPException(status_code=403, detail="LLM creation is disabled")


@router.put("/{llm_name}")
async def update_llm(llm_name: str = Path(..., description="大语言模型名称")):
    """更新大语言模型"""
    return HTTPException(status_code=403, detail="LLM creation is disabled")


@router.delete("/{llm_name}")
async def delete_llm(llm_name: str = Path(..., description="大语言模型名称")):
    """删除大语言模型"""
    return HTTPException(status_code=403, detail="LLM creation is disabled")
