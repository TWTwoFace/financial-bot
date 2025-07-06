from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from src.config import config


stats_markup = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(
            text=config.markups.statistics.monthly_analytics,
            callback_data=config.callbacks.monthly_analytics
        )]
    ]
)
