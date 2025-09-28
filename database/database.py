"""
Підключення та ініціалізація бази даних SQLite
"""

import aiosqlite
import os
from config import config
from utils.logger import setup_logger

logger = setup_logger()

async def init_db():
    """Ініціалізація бази даних"""
    try:
        async with aiosqlite.connect(config.DATABASE_PATH) as db:
            # Створення таблиці користувачів
            await db.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    telegram_id INTEGER UNIQUE NOT NULL,
                    username TEXT,
                    first_name TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    total_distance REAL DEFAULT 0.0,
                    total_steps INTEGER DEFAULT 0,
                    is_active BOOLEAN DEFAULT 1
                )
            """)

            # Створення таблиці груп
            await db.execute("""
                CREATE TABLE IF NOT EXISTS groups (
                    group_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    telegram_group_id INTEGER UNIQUE NOT NULL,
                    group_name TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    is_active BOOLEAN DEFAULT 1
                )
            """)

            # Створення таблиці рейтингів
            await db.execute("""
                CREATE TABLE IF NOT EXISTS rankings (
                    ranking_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    group_id INTEGER,
                    points INTEGER DEFAULT 0,
                    rank_level TEXT DEFAULT 'bronze',
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(user_id),
                    FOREIGN KEY (group_id) REFERENCES groups(group_id)
                )
            """)

            # Створення таблиці змагань
            await db.execute("""
                CREATE TABLE IF NOT EXISTS competitions (
                    competition_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    group_id INTEGER,
                    comp_type TEXT NOT NULL,
                    route_data TEXT,
                    start_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    duration_minutes INTEGER DEFAULT 60,
                    is_active BOOLEAN DEFAULT 1,
                    FOREIGN KEY (group_id) REFERENCES groups(group_id)
                )
            """)

            # Створення таблиці GPS треків
            await db.execute("""
                CREATE TABLE IF NOT EXISTS gps_tracks (
                    track_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    competition_id INTEGER,
                    latitude REAL NOT NULL,
                    longitude REAL NOT NULL,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    distance_km REAL DEFAULT 0.0,
                    speed_kmh REAL DEFAULT 0.0,
                    is_valid BOOLEAN DEFAULT 1,
                    FOREIGN KEY (user_id) REFERENCES users(user_id),
                    FOREIGN KEY (competition_id) REFERENCES competitions(competition_id)
                )
            """)

            # Створення індексів для швидкості запитів
            await db.execute("CREATE INDEX IF NOT EXISTS idx_users_telegram_id ON users(telegram_id)")
            await db.execute("CREATE INDEX IF NOT EXISTS idx_rankings_user_id ON rankings(user_id)")
            await db.execute("CREATE INDEX IF NOT EXISTS idx_gps_tracks_user_id ON gps_tracks(user_id)")

            await db.commit()
            logger.info("✅ База даних успішно ініціалізована")

    except Exception as e:
        logger.error(f"❌ Помилка ініціалізації БД: {e}")
        raise

async def get_db_connection():
    """Отримати підключення до БД"""
    return await aiosqlite.connect(config.DATABASE_PATH)
