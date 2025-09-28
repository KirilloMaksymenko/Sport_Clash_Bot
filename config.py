"""
Конфігурація Telegram Fitness Bot
"""

import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()

@dataclass
class Config:
    """Клас конфігурації"""

    # Telegram
    BOT_TOKEN: str = os.getenv("BOT_TOKEN")
    MINI_APP_URL: str = os.getenv("MINI_APP_URL", "https://yourapp.com/mini_app")

    # База даних
    DATABASE_PATH: str = os.getenv("DATABASE_PATH", "./bot_database.db")

    # Логування
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")

    # GPS налаштування
    GPS_ACCURACY_THRESHOLD: int = int(os.getenv("GPS_ACCURACY_THRESHOLD", "50"))
    ROUTE_DEVIATION_PENALTY: int = int(os.getenv("ROUTE_DEVIATION_PENALTY", "5"))

    # Рейтинги
    BRONZE_THRESHOLD: int = int(os.getenv("BRONZE_THRESHOLD", "100"))
    SILVER_THRESHOLD: int = int(os.getenv("SILVER_THRESHOLD", "500"))
    GOLD_THRESHOLD: int = int(os.getenv("GOLD_THRESHOLD", "1000"))

    def __post_init__(self):
        if not self.BOT_TOKEN:
            raise ValueError("BOT_TOKEN не встановлено в .env файлі")

config = Config()
