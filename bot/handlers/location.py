"""
Обробник GPS локації
"""

from aiogram import Router, types, F
from datetime import datetime
import math

from database.database import get_db_connection
from services.gps_service import GpsService  
from services.ranking_service import RankingService
from utils.logger import setup_logger

router = Router()
logger = setup_logger()
gps_service = GpsService()
ranking_service = RankingService()

@router.message(F.location)
async def handle_location(message: types.Message):
    """Обробник отримання GPS локації"""

    location = message.location
    user_id = message.from_user.id

    logger.info(f"📍 Отримана локація від користувача {user_id}: {location.latitude}, {location.longitude}")

    try:
        # Збереження локації в БД
        async with await get_db_connection() as db:
            # Отримання user_id з БД
            cursor = await db.execute("SELECT user_id FROM users WHERE telegram_id = ?", (user_id,))
            user_row = await cursor.fetchone()

            if user_row:
                internal_user_id = user_row[0]

                # Валідація локації
                if not gps_service.validate_location(location):
                    await message.answer("❌ Неточна GPS локація. Спробуйте ще раз.")
                    return

                # Збереження GPS треку
                speed = await gps_service.calculate_speed(internal_user_id, location)

                await db.execute("""
                    INSERT INTO gps_tracks (user_id, latitude, longitude, speed_kmh, timestamp)
                    VALUES (?, ?, ?, ?, ?)
                """, (internal_user_id, location.latitude, location.longitude, speed, datetime.now()))

                # Розрахунок пройденої відстані
                distance = await gps_service.calculate_distance_from_last_point(internal_user_id, location)

                # Оновлення загальної відстані користувача  
                if distance > 0:
                    await db.execute("""
                        UPDATE users SET total_distance = total_distance + ?, 
                                       total_steps = total_steps + ?
                        WHERE user_id = ?
                    """, (distance, int(distance * 1300), internal_user_id))  # ~1300 кроків на км

                    # Оновлення рейтингу
                    await ranking_service.update_user_points(internal_user_id, distance)

                await db.commit()

                # Відповідь користувачу
                response_text = f"""
📍 **Локація збережена!**

🗺️ Координати: `{location.latitude:.6f}, {location.longitude:.6f}`
🚶‍♂️ Відстань з останньої точки: {distance:.2f} км
🏃‍♂️ Швидкість: {speed:.1f} км/год
📊 Бали нараховані за активність!

*Продовжуй рухатись для збільшення рейтингу* 💪
                """

                await message.answer(response_text, parse_mode="Markdown")

        logger.info(f"✅ Локація користувача {user_id} збережена, відстань: {distance:.2f} км")

    except Exception as e:
        logger.error(f"❌ Помилка обробки локації: {e}")
        await message.answer("❌ Помилка при обробці локації. Спробуйте ще раз.")

@router.message(F.text == "📍 Поділитися локацією") 
async def request_location(message: types.Message):
    """Запит локації від користувача"""
    await message.answer(
        "📍 Поділіться своєю локацією для відстеження активності",
        reply_markup=types.ReplyKeyboardMarkup(
            keyboard=[[types.KeyboardButton(text="📍 Надіслати локацію", request_location=True)]],
            resize_keyboard=True,
            one_time_keyboard=True
        )
    )
