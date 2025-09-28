"""
Обробник змагань
"""

from aiogram import Router, types, F
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from datetime import datetime, timedelta

from database.database import get_db_connection
from services.competition_service import CompetitionService
from utils.logger import setup_logger

router = Router()
logger = setup_logger()
competition_service = CompetitionService()

@router.callback_query(F.data.startswith("competition_"))
async def handle_competition_callback(callback: types.CallbackQuery):
    """Обробник колбеків змагань"""

    action = callback.data.split("_")[1]
    user_id = callback.from_user.id

    if action == "sprint":
        await start_sprint_competition(callback, user_id)
    elif action == "endurance":
        await start_endurance_competition(callback, user_id)
    elif action == "join":
        comp_id = callback.data.split("_")[2]
        await join_competition(callback, user_id, comp_id)

    await callback.answer()

async def start_sprint_competition(callback: types.CallbackQuery, user_id: int):
    """Запуск Sprint змагання"""
    try:
        # Створення змагання в БД
        competition_id = await competition_service.create_competition(
            group_id=None,
            comp_type="sprint",
            duration_minutes=30
        )

        text = f"""
⚡ **Sprint змагання запущено!**

🏃‍♂️ Тривалість: 30 хвилин
🎯 Мета: Максимальна швидкість
📍 Використовуйте Mini App для відстеження

Удачі! 🚀
        """

        await callback.message.edit_text(text, parse_mode="Markdown")

    except Exception as e:
        logger.error(f"❌ Помилка запуску Sprint змагання: {e}")
        await callback.message.edit_text("❌ Помилка запуску змагання")

async def start_endurance_competition(callback: types.CallbackQuery, user_id: int):
    """Запуск Endurance змагання"""
    try:
        # Створення змагання в БД
        competition_id = await competition_service.create_competition(
            group_id=None,
            comp_type="endurance", 
            duration_minutes=90
        )

        text = f"""
🏃‍♂️ **Endurance змагання запущено!**

⏱️ Тривалість: 90 хвилин
🎯 Мета: Максимальна відстань
📍 Використовуйте Mini App для відстеження

Удачі! 💪
        """

        await callback.message.edit_text(text, parse_mode="Markdown")

    except Exception as e:
        logger.error(f"❌ Помилка запуску Endurance змагання: {e}")
        await callback.message.edit_text("❌ Помилка запуску змагання")
