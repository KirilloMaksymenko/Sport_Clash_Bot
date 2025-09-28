"""
Налаштування логування
"""

import logging
import sys
from loguru import logger as loguru_logger
from config import config

def setup_logger():
    """Налаштування логера"""

    # Видалення стандартного обробника loguru
    loguru_logger.remove()

    # Додавання консольного виводу з кольоровим форматуванням
    loguru_logger.add(
        sys.stdout,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
        level=config.LOG_LEVEL,
        colorize=True
    )

    # Додавання файлового логування
    loguru_logger.add(
        "logs/bot.log",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
        level=config.LOG_LEVEL,
        rotation="10 MB",
        retention="7 days"
    )

    return loguru_logger
