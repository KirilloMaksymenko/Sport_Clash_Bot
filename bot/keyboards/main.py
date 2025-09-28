"""
Основні клавіатури
"""

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, WebAppInfo
from config import config

def get_main_keyboard() -> ReplyKeyboardMarkup:
    """Головна клавіатура"""
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="🏃 Відкрити Fitness App", 
                              web_app=WebAppInfo(url=config.MINI_APP_URL))
            ],
            [
                KeyboardButton(text="📊 Мій рейтинг"),
                KeyboardButton(text="🏆 Топ гравців")
            ],
            [
                KeyboardButton(text="📍 Поділитися локацією", 
                              request_location=True)
            ]
        ],
        resize_keyboard=True
    )
