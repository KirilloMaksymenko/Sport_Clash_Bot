"""
Налаштування роутерів для обробників
"""

from aiogram import Dispatcher
from . import start, location, competitions, rankings

def setup_routers(dp: Dispatcher):
    """Налаштування всіх роутерів"""
    dp.include_router(start.router)
    dp.include_router(location.router)
    dp.include_router(competitions.router)
    dp.include_router(rankings.router)
