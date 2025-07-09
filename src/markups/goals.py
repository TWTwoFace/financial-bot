from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from src.config import config

goals_markup = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text=config.markups.goals.get_goal),
            KeyboardButton(text=config.markups.goals.set_goal)
        ],
        [
            KeyboardButton(text=config.markups.back)
        ]
    ],
    resize_keyboard=True,
)