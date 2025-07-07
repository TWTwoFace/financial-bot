from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from src.config import config

notifications_markup = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text=config.markups.notifications.add_notification),
            KeyboardButton(text=config.markups.notifications.remove_notification)
        ],
        [
            KeyboardButton(text=config.markups.back)
        ]
    ],
    resize_keyboard=True,
)

cancel_processing_notifications_markup = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text=config.markups.back)
        ]
    ],
    resize_keyboard=True
)