"""
Інлайн клавіатури
"""

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_competition_keyboard() -> InlineKeyboardMarkup:
    """Клавіатура змагань"""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="⚡ Sprint", callback_data="competition_sprint"),
                InlineKeyboardButton(text="🏃‍♂️ Endurance", callback_data="competition_endurance")
            ]
        ]
    )
