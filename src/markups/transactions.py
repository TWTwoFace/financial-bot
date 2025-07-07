from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from src.config import config


transactions_markup = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text=config.markups.transactions.cancel)]
    ],
    resize_keyboard=True,
)

expense_category_markup = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text=config.markups.transactions.expenses.shops)],
        [KeyboardButton(text=config.markups.transactions.expenses.credit)],
        [KeyboardButton(text=config.markups.transactions.expenses.housing)],
        [KeyboardButton(text=config.markups.transactions.expenses.products)],
        [KeyboardButton(text=config.markups.transactions.expenses.transport)],
        [KeyboardButton(text=config.markups.transactions.cancel)]
    ],
    resize_keyboard=True,
)

income_category_markup = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text=config.markups.transactions.incomes.payment)],
        [KeyboardButton(text=config.markups.transactions.incomes.remittance)],
        [KeyboardButton(text=config.markups.transactions.incomes.business)],
        [KeyboardButton(text=config.markups.transactions.incomes.passive)],
        [KeyboardButton(text=config.markups.transactions.cancel)]
    ],
    resize_keyboard=True,
)