"""
Сервіс системи рейтингів
"""

from database.database import get_db_connection
from config import config
from utils.logger import setup_logger

logger = setup_logger()

class RankingService:
    """Сервіс для роботи з рейтингами"""

    def __init__(self):
        self.rank_thresholds = {
            "bronze": config.BRONZE_THRESHOLD,
            "silver": config.SILVER_THRESHOLD,
            "gold": config.GOLD_THRESHOLD,
            "platinum": 2500,
            "diamond": 5000
        }

    async def update_user_points(self, user_id: int, distance_km: float):
        """Оновлення балів користувача"""

        # Нарахування балів: 10 балів за км
        points_earned = int(distance_km * 10)

        if points_earned <= 0:
            return

        try:
            async with await get_db_connection() as db:
                # Перевірка чи існує запис рейтингу
                cursor = await db.execute("""
                    SELECT ranking_id, points FROM rankings WHERE user_id = ?
                """, (user_id,))
                existing_rank = await cursor.fetchone()

                if existing_rank:
                    # Оновлення існуючого рейтингу
                    new_points = existing_rank[1] + points_earned
                    new_rank_level = self.calculate_rank_level(new_points)

                    await db.execute("""
                        UPDATE rankings 
                        SET points = ?, rank_level = ?, updated_at = CURRENT_TIMESTAMP
                        WHERE user_id = ?
                    """, (new_points, new_rank_level, user_id))
                else:
                    # Створення нового рейтингу
                    rank_level = self.calculate_rank_level(points_earned)

                    await db.execute("""
                        INSERT INTO rankings (user_id, points, rank_level)
                        VALUES (?, ?, ?)
                    """, (user_id, points_earned, rank_level))

                await db.commit()
                logger.info(f"✅ Оновлено рейтинг користувача {user_id}: +{points_earned} балів")

        except Exception as e:
            logger.error(f"❌ Помилка оновлення рейтингу: {e}")

    def calculate_rank_level(self, points: int) -> str:
        """Розрахунок рівня рейтингу"""

        if points >= self.rank_thresholds["diamond"]:
            return "diamond"
        elif points >= self.rank_thresholds["platinum"]:
            return "platinum"
        elif points >= self.rank_thresholds["gold"]:
            return "gold"
        elif points >= self.rank_thresholds["silver"]:
            return "silver"
        else:
            return "bronze"

    async def get_user_ranking(self, user_id: int) -> dict:
        """Отримання рейтингу користувача"""

        try:
            async with await get_db_connection() as db:
                cursor = await db.execute("""
                    SELECT points, rank_level, 
                           (SELECT COUNT(*) + 1 FROM rankings r2 WHERE r2.points > r1.points) as position
                    FROM rankings r1
                    WHERE user_id = ?
                """, (user_id,))

                result = await cursor.fetchone()

                if result:
                    return {
                        "points": result[0],
                        "rank_level": result[1],
                        "position": result[2]
                    }
                else:
                    return {
                        "points": 0,
                        "rank_level": "bronze",
                        "position": None
                    }

        except Exception as e:
            logger.error(f"❌ Помилка отримання рейтингу: {e}")
            return {"points": 0, "rank_level": "bronze", "position": None}
