"""
Валідатори даних
"""

import re
from typing import Optional

def validate_telegram_id(telegram_id: int) -> bool:
    """Валідація Telegram ID"""
    return isinstance(telegram_id, int) and telegram_id > 0

def validate_coordinates(latitude: float, longitude: float) -> bool:
    """Валідація GPS координат"""
    return (-90 <= latitude <= 90) and (-180 <= longitude <= 180)

def validate_username(username: Optional[str]) -> bool:
    """Валідація Telegram username"""
    if username is None:
        return True

    pattern = r"^[a-zA-Z0-9_]{5,32}$"
    return re.match(pattern, username) is not None

def validate_distance(distance: float) -> bool:
    """Валідація відстані"""
    return isinstance(distance, (int, float)) and 0 <= distance <= 1000  # максимум 1000 км

def validate_speed(speed: float) -> bool:
    """Валідація швидкості"""
    return isinstance(speed, (int, float)) and 0 <= speed <= 100  # максимум 100 км/год
