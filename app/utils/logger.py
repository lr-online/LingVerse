import sys
from pathlib import Path

from loguru import logger

# 创建logs目录（如果不存在）
log_dir = Path("logs")
log_dir.mkdir(exist_ok=True)

# 移除默认的控制台处理器
logger.remove()

# 添加控制台处理器，设置日志级别为INFO
logger.add(
    sys.stdout,
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
    level="INFO",
)

# 添加文件处理器，设置日志级别为DEBUG
# 日志文件将按天进行切割，保留7天的历史记录
logger.add(
    "logs/app_{time:YYYY-MM-DD}.log",
    rotation="00:00",  # 每天午夜切割
    retention="7 days",  # 保留7天的日志
    format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
    level="DEBUG",
    encoding="utf-8",
)


def get_logger(name: str = "app"):
    """
    获取logger实例

    Args:
        name: 日志记录器的名称，默认为'app'

    Returns:
        loguru.logger 实例
    """
    return logger.bind(name=name)


# 导出logger实例，可以直接使用
app_logger = get_logger()


if __name__ == "__main__":
    app_logger.info("This is a test log")
