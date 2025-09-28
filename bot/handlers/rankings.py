"""
Обробник рейтингів та статистики
"""

from aiogram import Router, types, F

from database.database import get_db_connection
from utils.logger import setup_logger

router = Router()
logger = setup_logger()

# Цей модуль може містити додаткові команди для рейтингів
