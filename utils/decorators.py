"""
Корисні декоратори
"""

import functools
import asyncio
from utils.logger import setup_logger

logger = setup_logger()

def async_retry(max_attempts: int = 3, delay: float = 1.0):
    """Декоратор для повтору асинхронних функцій"""

    def decorator(func):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            for attempt in range(max_attempts):
                try:
                    return await func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts - 1:
                        logger.error(f"❌ Функція {func.__name__} не виконалась після {max_attempts} спроб: {e}")
                        raise

                    logger.warning(f"⚠️ Спроба {attempt + 1} функції {func.__name__} не вдалась: {e}")
                    await asyncio.sleep(delay)

        return wrapper
    return decorator

def log_execution(func):
    """Декоратор для логування виконання функцій"""

    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        logger.info(f"🚀 Виконання {func.__name__}")
        try:
            result = await func(*args, **kwargs)
            logger.info(f"✅ {func.__name__} виконано успішно")
            return result
        except Exception as e:
            logger.error(f"❌ Помилка в {func.__name__}: {e}")
            raise

    return wrapper
