"""
GPS Service для обробки локації та розрахунків
"""

import math
import asyncio
from datetime import datetime, timedelta
from typing import Optional, List, Tuple
from database.database import get_db_connection
from utils.logger import setup_logger

logger = setup_logger()

class GpsService:
    """Сервіс для роботи з GPS даними"""

    def __init__(self):
        self.accuracy_threshold = 50  # метрів
        self.min_distance_threshold = 0.01  # 10 метрів мінімальна відстань

    async def calculate_distance_from_last_point(
        self, 
        user_id: int, 
        location
    ) -> float:
        """Розрахунок відстані від останньої збереженої точки"""

        try:
            async with await get_db_connection() as db:
                # Отримання останньої GPS точки користувача
                cursor = await db.execute("""
                    SELECT latitude, longitude, timestamp 
                    FROM gps_tracks 
                    WHERE user_id = ? AND is_valid = 1
                    ORDER BY timestamp DESC 
                    LIMIT 1
                """, (user_id,))

                last_point = await cursor.fetchone()

                if not last_point:
                    return 0.0

                # Розрахунок відстані
                distance_km = self.haversine_distance(
                    (last_point[0], last_point[1]),
                    (location.latitude, location.longitude)
                )

                # Перевірка на мінімальну відстань та час
                last_timestamp = datetime.fromisoformat(last_point[2])
                time_diff = (datetime.now() - last_timestamp).total_seconds()

                # Ігнорування якщо відстань дуже мала або час дуже малий
                if distance_km < self.min_distance_threshold or time_diff < 10:
                    return 0.0

                return distance_km

        except Exception as e:
            logger.error(f"❌ Помилка розрахунку відстані: {e}")
            return 0.0

    def haversine_distance(
        self, 
        point1: Tuple[float, float], 
        point2: Tuple[float, float]
    ) -> float:
        """
        Розрахунок відстані між двома точками за формулою гаверсинуса
        """

        lat1, lon1 = point1
        lat2, lon2 = point2

        # Переведення градусів у радіани
        lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])

        # Різниці координат
        dlat = lat2 - lat1
        dlon = lon2 - lon1

        # Формула гаверсинуса
        a = (math.sin(dlat/2)**2 + 
             math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2)

        c = 2 * math.asin(math.sqrt(a))

        # Радіус Землі в кілометрах
        r = 6371

        return c * r

    async def calculate_speed(
        self, 
        user_id: int, 
        current_location
    ) -> float:
        """Розрахунок поточної швидкості"""

        try:
            async with await get_db_connection() as db:
                # Отримання останніх 2 точок для розрахунку швидкості
                cursor = await db.execute("""
                    SELECT latitude, longitude, timestamp 
                    FROM gps_tracks 
                    WHERE user_id = ? AND is_valid = 1
                    ORDER BY timestamp DESC 
                    LIMIT 2
                """, (user_id,))

                points = await cursor.fetchall()

                if len(points) < 1:
                    return 0.0

                last_point = points[0]

                # Розрахунок відстані
                distance_km = self.haversine_distance(
                    (last_point[0], last_point[1]),
                    (current_location.latitude, current_location.longitude)
                )

                # Розрахунок часу
                last_timestamp = datetime.fromisoformat(last_point[2])
                time_diff_hours = (datetime.now() - last_timestamp).total_seconds() / 3600

                if time_diff_hours == 0:
                    return 0.0

                # Швидкість в км/год
                speed_kmh = distance_km / time_diff_hours

                # Обмеження максимальної швидкості (100 км/год для фільтрації помилок)
                return min(speed_kmh, 100.0)

        except Exception as e:
            logger.error(f"❌ Помилка розрахунку швидкості: {e}")
            return 0.0

    def validate_location(self, location, previous_location=None) -> bool:
        """Валідація GPS локації"""

        # Перевірка базових параметрів
        if not (-90 <= location.latitude <= 90):
            return False

        if not (-180 <= location.longitude <= 180):
            return False

        # Перевірка точності (якщо доступна)
        if hasattr(location, 'accuracy') and location.accuracy:
            if location.accuracy > self.accuracy_threshold:
                logger.warning(f"⚠️ Низька точність GPS: {location.accuracy}м")
                return False

        # Перевірка на надто великий стрибок відстані
        if previous_location:
            distance_km = self.haversine_distance(
                (previous_location.latitude, previous_location.longitude),
                (location.latitude, location.longitude)
            )

            # Якщо відстань більше 1 км за раз - підозріло
            if distance_km > 1.0:
                logger.warning(f"⚠️ Великий стрибок відстані: {distance_km:.2f}км")
                return False

        return True

    async def calculate_route_deviation(
        self, 
        user_location: Tuple[float, float], 
        route_points: List[Tuple[float, float]]
    ) -> float:
        """Розрахунок відхилення від заданого маршруту"""

        if not route_points:
            return 0.0

        # Знаходження найближчої точки маршруту
        min_distance = float('inf')

        for point in route_points:
            distance = self.haversine_distance(user_location, point)
            min_distance = min(min_distance, distance)

        return min_distance
