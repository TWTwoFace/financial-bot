from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from src.config import config

main_menu_markup = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text=config.markups.main_menu.add_expense),
            KeyboardButton(text=config.markups.main_menu.add_income)
        ],
        [
            KeyboardButton(text=config.markups.main_menu.statistics),
            KeyboardButton(text=config.markups.main_menu.goals)
        ],
        [
            KeyboardButton(text=config.markups.main_menu.notifications)
        ],
        [
            KeyboardButton(text=config.markups.main_menu.help)
        ]
    ],
    resize_keyboard=True,
    input_field_placeholder=config.markups.main_menu.placeholder
)
