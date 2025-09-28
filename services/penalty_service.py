"""
Сервіс штрафної системи
"""

from database.database import get_db_connection
from services.gps_service import GpsService
from config import config
from utils.logger import setup_logger

logger = setup_logger()

class PenaltyService:
    """Сервіс штрафної системи"""

    def __init__(self):
        self.gps_service = GpsService()
        self.deviation_threshold = 0.05  # 50 метрів
        self.penalty_seconds = config.ROUTE_DEVIATION_PENALTY

    async def check_route_deviation(
        self, 
        user_id: int, 
        competition_id: int,
        user_location: tuple,
        route_points: list
    ) -> bool:
        """Перевірка відхилення від маршруту"""

        if not route_points:
            return False

        deviation_km = await self.gps_service.calculate_route_deviation(
            user_location, route_points
        )

        # Якщо відхилення більше порогу
        if deviation_km > self.deviation_threshold:
            await self.apply_penalty(user_id, competition_id, self.penalty_seconds)
            return True

        return False

    async def apply_penalty(self, user_id: int, competition_id: int, penalty_seconds: int):
        """Застосування штрафу"""

        try:
            # Тут можна зберегти штраф в БД або просто логувати
            logger.warning(f"⚠️ Штраф {penalty_seconds}с для користувача {user_id} в змаганні {competition_id}")

            # Можна додати логіку штрафних балів

        except Exception as e:
            logger.error(f"❌ Помилка застосування штрафу: {e}")
