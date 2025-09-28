"""
Моделі даних для SQLite бази даних
"""

import aiosqlite
from datetime import datetime
from typing import Optional, List
from dataclasses import dataclass
from enum import Enum

class RankLevel(Enum):
    """Рівні рейтингу"""
    BRONZE = "bronze"
    SILVER = "silver"  
    GOLD = "gold"
    PLATINUM = "platinum"
    DIAMOND = "diamond"

class CompetitionType(Enum):
    """Типи змагань"""
    SPRINT = "sprint"
    ENDURANCE = "endurance"

@dataclass
class User:
    """Модель користувача"""
    user_id: Optional[int] = None
    telegram_id: int = 0
    username: Optional[str] = None
    first_name: str = ""
    created_at: Optional[datetime] = None
    total_distance: float = 0.0
    total_steps: int = 0
    is_active: bool = True

@dataclass  
class Group:
    """Модель групи"""
    group_id: Optional[int] = None
    telegram_group_id: int = 0
    group_name: str = ""
    created_at: Optional[datetime] = None
    is_active: bool = True

@dataclass
class Ranking:
    """Модель рейтингу"""
    ranking_id: Optional[int] = None
    user_id: int = 0
    group_id: Optional[int] = None
    points: int = 0
    rank_level: RankLevel = RankLevel.BRONZE
    updated_at: Optional[datetime] = None

@dataclass
class Competition:
    """Модель змагання"""
    competition_id: Optional[int] = None
    group_id: Optional[int] = None
    comp_type: CompetitionType = CompetitionType.SPRINT
    route_data: str = ""  # JSON з координатами маршруту
    start_time: Optional[datetime] = None
    duration_minutes: int = 60
    is_active: bool = True

@dataclass
class GpsTrack:
    """Модель GPS треку"""
    track_id: Optional[int] = None
    user_id: int = 0
    competition_id: Optional[int] = None
    latitude: float = 0.0
    longitude: float = 0.0
    timestamp: Optional[datetime] = None
    distance_km: float = 0.0
    speed_kmh: float = 0.0
    is_valid: bool = True
