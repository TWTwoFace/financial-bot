from datetime import datetime

from aiogram import Router, F, types
from aiogram.types import Message

from src.config import *
from src.markups.statistics import stats_markup
from src.markups.transactions import month_statistics_markup
from src.repositories.statistics import StatsRepository
from src.repositories.transactions import TransactionsRepository
from src.repositories.users import UsersRepository
from src.schemas.users import UserSchema

router = Router()


@router.message(F.text == config.markups.main_menu.statistics)
async def show_balance_and_stats(message: types.Message):
    user = UserSchema(telegram_id=str(message.from_user.id))
    balance = await StatsRepository.get_balance(user)
    monthly_balance = await StatsRepository.get_balance_by_month(user)
    await message.answer(
        f"Ваш текущий баланс: **{balance:.2f}**\n\n"
        f"Баланс за месяц: **{monthly_balance:.2f}**\n\n"
        "Выберите опцию для получения детальной статистики.",
        reply_markup=stats_markup,
        parse_mode="Markdown"
    )


@router.callback_query(F.data == config.callbacks.monthly_analytics)
async def show_monthly_analytics(callback: types.CallbackQuery):
    await callback.message.answer("Выберите интересующий пункт в меню", reply_markup=month_statistics_markup)
    await callback.answer()


@router.message(F.text == config.markups.month_statistics.expenses)
async def show_expenses(message: Message):
    user = await UsersRepository.get_user_by_telegram(str(message.from_user.id))
    date = datetime.today().replace(day=1).replace(hour=0).replace(minute=0).replace(second=0)
    expenses = await TransactionsRepository.get_user_expenses(user, str(date))

    expenses_text = ''

    for exp in expenses:
        expenses_text += f'{exp.value}р.\t\t{exp.category}\n'

    if len(expenses) == 0:
        expenses_text = 'Нет расходов'

    await message.answer(text=f"Расходы:\n\n{expenses_text}")


@router.message(F.text == config.markups.month_statistics.incomes)
async def show_incomes(message: Message):
    user = await UsersRepository.get_user_by_telegram(str(message.from_user.id))
    date = datetime.today().replace(day=1).replace(hour=0).replace(minute=0).replace(second=0)
    incomes = await TransactionsRepository.get_user_incomes(user, str(date))

    incomes_text = ''

    for inc in incomes:
        incomes_text += f'{inc.value}р.\t\t{inc.category}\n'

    if len(incomes) == 0:
        incomes_text = 'Нет расходов'

    await message.answer(text=f"Доходы:\n\n{incomes_text}")


@router.message(F.text == config.markups.month_statistics.categories)
async def show_top_categories(message: Message):
    user = await UsersRepository.get_user_by_telegram(str(message.from_user.id))
    date = datetime.today().replace(day=1).replace(hour=0).replace(minute=0).replace(second=0)

    expenses = await StatsRepository.get_expenses_top_categories(user, str(date), 5)
    incomes = await StatsRepository.get_incomes_top_categories(user, str(date), 5)

    expenses_text = ''
    for i in range(len(expenses)):
        expenses_text += f"{i + 1}: {expenses[i].category} | {expenses[i].total}р.\n"

    incomes_text = ''
    for i in range(len(incomes)):
        incomes_text += f"{i + 1}: {incomes[i].category} | {incomes[i].total}р.\n"

    await message.answer(
        text=f'<b>Статистика по категориям</b>\n\nРасходы:\n{expenses_text}\n\nДоходы:\n{incomes_text}',
        parse_mode='HTML'
    )
