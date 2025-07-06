from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from src.config import config


transactions_markup = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text=config.markups.transactions.cancel)]
    ],
    resize_keyboard=True,
)
