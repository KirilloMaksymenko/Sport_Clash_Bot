"""
Сервіс змагань
"""

import json
from datetime import datetime, timedelta
from typing import Optional, List
from database.database import get_db_connection
from utils.logger import setup_logger

logger = setup_logger()

class CompetitionService:
    """Сервіс для роботи зі змаганнями"""

    async def create_competition(
        self, 
        group_id: Optional[int], 
        comp_type: str,
        duration_minutes: int = 60,
        route_points: Optional[List] = None
    ) -> int:
        """Створення нового змагання"""

        try:
            route_data = json.dumps(route_points) if route_points else ""

            async with await get_db_connection() as db:
                cursor = await db.execute("""
                    INSERT INTO competitions (group_id, comp_type, route_data, duration_minutes)
                    VALUES (?, ?, ?, ?)
                """, (group_id, comp_type, route_data, duration_minutes))

                competition_id = cursor.lastrowid
                await db.commit()

                logger.info(f"✅ Створено змагання {comp_type} з ID {competition_id}")
                return competition_id

        except Exception as e:
            logger.error(f"❌ Помилка створення змагання: {e}")
            raise

    async def join_competition(self, user_id: int, competition_id: int):
        """Приєднання користувача до змагання"""

        try:
            async with await get_db_connection() as db:
                # Перевірка чи змагання активне
                cursor = await db.execute("""
                    SELECT comp_type, start_time, duration_minutes 
                    FROM competitions 
                    WHERE competition_id = ? AND is_active = 1
                """, (competition_id,))

                competition = await cursor.fetchone()

                if not competition:
                    return False

                # Логіка приєднання (можна розширити)
                logger.info(f"👤 Користувач {user_id} приєднався до змагання {competition_id}")
                return True

        except Exception as e:
            logger.error(f"❌ Помилка приєднання до змагання: {e}")
            return False

    async def end_competition(self, competition_id: int):
        """Завершення змагання"""

        try:
            async with await get_db_connection() as db:
                await db.execute("""
                    UPDATE competitions 
                    SET is_active = 0 
                    WHERE competition_id = ?
                """, (competition_id,))

                await db.commit()
                logger.info(f"🏁 Змагання {competition_id} завершено")

        except Exception as e:
            logger.error(f"❌ Помилка завершення змагання: {e}")
