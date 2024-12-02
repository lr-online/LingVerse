from openai import AsyncOpenAI

from app.models.llm_model import LLM
from app.utils.logger import get_logger

logger = get_logger(__name__)


async def update_llm_model_collection():
    """
    更新大语言模型集合
    """
    oai_client = AsyncOpenAI()
    model_list = await oai_client.models.list()
    for model in model_list.data:
        await LLM.create(
            model_name=model.id,
            provider=model.owned_by,
            api_key=oai_client.api_key,
            base_url=str(oai_client.base_url),
        )

    latest_model_list = [model.id for model in model_list.data]
    await LLM.update_by_field(
        {
            "model_name": {"$nin": latest_model_list}
        },
        {"is_deleted": True}
    )
    logger.info("更新大语言模型集合成功")



async def dump_llm_model_collection():
    """
    导出大语言模型集合
    """
    model_list = await LLM.collection().find().to_list(None)
    logger.info(f"导出大语言模型集合成功: {model_list}")



if __name__ == '__main__':
    import asyncio

    loop = asyncio.new_event_loop()
    loop.run_until_complete(update_llm_model_collection())
