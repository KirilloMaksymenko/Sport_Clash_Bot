"""
Middleware для автентифікації
"""

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from typing import Callable, Dict, Any, Awaitable

class AuthMiddleware(BaseMiddleware):
    """Middleware для автентифікації користувачів"""

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        # Тут можна додати логіку автентифікації
        return await handler(event, data)
