from fastapi import APIRouter, HTTPException, Path
from openai import AsyncOpenAI

from app.models.llm_model import LLM
from app.utils.api_response import ResponseModel
from app.utils.logger import get_logger

logger = get_logger(__name__)

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


@router.post("/sync", response_model=ResponseModel)
async def sync_llm_models():
    """同步大语言模型列表"""
    logger.info("Starting LLM models synchronization")
    oai_client = AsyncOpenAI()

    try:
        model_list = await oai_client.models.list()
        logger.info(f"Retrieved {len(model_list.data)} models from OpenAI")

        for model in model_list.data:
            await LLM.create(
                model_name=model.id,
                provider=model.owned_by,
                api_key=oai_client.api_key,
                base_url=str(oai_client.base_url),
            )
            logger.debug(f"Created/Updated model: {model.id}")

        latest_model_list = [model.id for model in model_list.data]
        await LLM.update_by_field(
            {"model_name": {"$nin": latest_model_list}}, {"is_deleted": True}
        )
        logger.info("LLM models synchronization completed")

        return ResponseModel(
            success=True,
            data={},
            message="LLM models synchronized successfully",
        )
    except Exception as e:
        logger.error(f"Failed to sync LLM models: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
