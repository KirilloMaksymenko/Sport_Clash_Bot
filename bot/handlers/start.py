"""
Обробник команди /start
"""

from aiogram import Router, types, F
from aiogram.filters import CommandStart
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, WebAppInfo

from config import config
from database.database import get_db_connection
from utils.logger import setup_logger

router = Router()
logger = setup_logger()

@router.message(CommandStart())
async def cmd_start(message: types.Message):
    """Обробник команди /start"""

    user = message.from_user
    logger.info(f"👤 Користувач {user.username} ({user.id}) запустив бота")

    # Реєстрація користувача в БД
    try:
        async with await get_db_connection() as db:
            await db.execute("""
                INSERT OR IGNORE INTO users (telegram_id, username, first_name)
                VALUES (?, ?, ?)
            """, (user.id, user.username, user.first_name))
            await db.commit()
    except Exception as e:
        logger.error(f"❌ Помилка реєстрації користувача: {e}")

    # Створення клавіатури
    keyboard = ReplyKeyboardMarkup(
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
        resize_keyboard=True,
        input_field_placeholder="Виберіть дію..."
    )

    welcome_text = f"""
🏃‍♂️ **Вітаю в Fitness Competition Bot!**

Привіт, {user.first_name}! 👋

Цей бот допоможе тобі:
🔹 Відстежувати щоденну активність
🔹 Брати участь у змаганнях з друзями  
🔹 Заробляти бали та підвищувати рейтинг
🔹 Змагатися в Sprint та Endurance забігах

**Твій поточний рівень:** 🥉 Бронза

📱 Натисни "Відкрити Fitness App" для повного функціоналу!
    """

    await message.answer(welcome_text, reply_markup=keyboard, parse_mode="Markdown")

@router.message(F.text == "📊 Мій рейтинг")
async def my_ranking(message: types.Message):
    """Показати рейтинг користувача"""
    user_id = message.from_user.id

    try:
        async with await get_db_connection() as db:
            cursor = await db.execute("""
                SELECT u.total_distance, u.total_steps, r.points, r.rank_level
                FROM users u
                LEFT JOIN rankings r ON u.user_id = r.user_id
                WHERE u.telegram_id = ?
            """, (user_id,))
            user_data = await cursor.fetchone()

            if user_data:
                distance, steps, points, rank = user_data
                rank_emoji = {"bronze": "🥉", "silver": "🥈", "gold": "🥇", "platinum": "💎", "diamond": "👑"}.get(rank, "🥉")

                ranking_text = f"""
📊 **Твоя статистика:**

🗺️ Загальна відстань: {distance or 0:.1f} км
👟 Загальні кроки: {steps or 0:,}
⭐ Очки: {points or 0}
{rank_emoji} Рівень: {rank or 'bronze'}

Продовжуй тренування для підвищення рейтингу! 💪
                """
            else:
                ranking_text = "📊 Статистика ще не доступна. Почни використовувати бота!"

        await message.answer(ranking_text, parse_mode="Markdown")

    except Exception as e:
        logger.error(f"❌ Помилка отримання рейтингу: {e}")
        await message.answer("❌ Помилка отримання статистики")

@router.message(F.text == "🏆 Топ гравців")  
async def top_players(message: types.Message):
    """Показати топ гравців"""
    try:
        async with await get_db_connection() as db:
            cursor = await db.execute("""
                SELECT u.first_name, r.points, r.rank_level
                FROM users u
                JOIN rankings r ON u.user_id = r.user_id
                ORDER BY r.points DESC
                LIMIT 10
            """, )
            top_users = await cursor.fetchall()

            if top_users:
                leaderboard_text = "🏆 **Топ 10 гравців:**\n\n"
                rank_emojis = {"bronze": "🥉", "silver": "🥈", "gold": "🥇", "platinum": "💎", "diamond": "👑"}

                for i, (name, points, rank_level) in enumerate(top_users, 1):
                    emoji = rank_emojis.get(rank_level, "🥉")
                    leaderboard_text += f"{i}. {emoji} {name} - {points} очок\n"
            else:
                leaderboard_text = "🏆 Рейтинг поки що порожній. Будь першим!"

        await message.answer(leaderboard_text, parse_mode="Markdown")

    except Exception as e:
        logger.error(f"❌ Помилка отримання топу: {e}")
        await message.answer("❌ Помилка отримання рейтингу")
