"""
日志模块，提供按天轮转的文件日志记录功能。

使用方法:
    from utils.logger import logger
    logger.info("日志信息")
    logger.error("错误信息")
"""

import logging
from logging.handlers import TimedRotatingFileHandler
import os
from datetime import datetime, timezone, timedelta


# 定义中国时区 (UTC+8)
CHINA_TZ = timezone(timedelta(hours=8))
#


class ChinaTimeFormatter(logging.Formatter):
    """使用中国时区的日志格式化器"""

    def formatTime(self, record, datefmt=None):
        ct = datetime.fromtimestamp(record.created, tz=CHINA_TZ)
        if datefmt:
            s = ct.strftime(datefmt)
        else:
            s = ct.strftime("%Y-%m-%d %H:%M:%S")
            s = f"{s},{int(record.msecs):03d}"
        return s


def get_logger(name: str = "app", log_dir: str = "logs") -> logging.Logger:
    """
    获取按天轮转的文件日志记录器。

    Args:
        name (str): 日志记录器名称，默认为 "app"。
        log_dir (str): 日志文件存放目录，默认为 "logs"。

    Returns:
        logging.Logger: 配置好的日志记录器实例。
    """
    os.makedirs(log_dir, exist_ok=True)

    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    if not logger.handlers:
        formatter = ChinaTimeFormatter(
            "%(asctime)s - %(levelname)s - %(funcName)s - %(message)s"
        )

        # 文件处理器：按天轮转
        log_file = os.path.join(log_dir, f"{name}.log")
        file_handler = TimedRotatingFileHandler(
            log_file, when="midnight", interval=1, backupCount=30, encoding="utf-8"
        )
        file_handler.suffix = "%Y-%m-%d"
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

        # 终端处理器：输出到控制台
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

    return logger


logger = get_logger()
