import sys
from typing import Any, Dict

from loguru import logger

from app.utils.request_id import get_request_id

# 移除默认的处理器
logger.remove()


def request_id_filter(record: Dict[str, Any]) -> bool:
    """为每条日志记录添加请求ID"""
    record["extra"]["request_id"] = get_request_id()
    return True


# 添加自定义格式的处理器
logger.add(
    sys.stdout,
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
    "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | "
    "<blue>{level}</blue> | "
    "<magenta>{extra[request_id]}</magenta> | "
    "{message}",
    level="DEBUG",
    filter=request_id_filter,
)


def get_logger(name: str):
    """获取logger"""
    return logger.bind(name=name)
