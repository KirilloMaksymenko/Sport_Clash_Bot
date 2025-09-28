#!/usr/bin/env python3
"""
Головний файл Telegram Fitness Bot
Автор: Ukrainian Fitness Bot Developer
"""

import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from config import config
from bot.handlers import setup_routers
from database.database import init_db
from utils.logger import setup_logger

# Налаштування логування
logger = setup_logger()

async def main():
    """Головна функція запуску бота"""
    logger.info("🚀 Запуск Telegram Fitness Bot...")

    # Ініціалізація бота
    bot = Bot(token=config.BOT_TOKEN)
    dp = Dispatcher(storage=MemoryStorage())

    # Ініціалізація бази даних
    await init_db()
    logger.info("✅ База даних ініціалізована")

    # Налаштування роутерів
    setup_routers(dp)
    logger.info("✅ Обробники команд налаштовані")

    # Запуск поллінгу
    try:
        await dp.start_polling(bot, allowed_updates=["message", "callback_query", "location"])
    except Exception as e:
        logger.error(f"❌ Помилка при запуску бота: {e}")
    finally:
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run(main())
