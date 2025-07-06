from aiogram import Router, F, types
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardRemove

from src.config import *
from src.markups.main_menu import main_menu_markup
from src.markups.transactions import transactions_markup
from src.states.transactions import AddTransaction

router = Router()


@router.message(F.text == config.markups.main_menu.add_expense)
async def start_add_expense(message: types.Message, state: FSMContext):
    await state.set_state(AddTransaction.amount)
    await state.update_data(type='expense')
    await message.answer("Введите сумму расхода:", reply_markup=transactions_markup)


@router.message(F.text == config.markups.main_menu.add_income)
async def start_add_income(message: types.Message, state: FSMContext):
    await state.set_state(AddTransaction.amount)
    await state.update_data(type='income')
    await message.answer("Введите сумму дохода:", reply_markup=transactions_markup)


@router.message(StateFilter(AddTransaction), F.text == config.markups.transactions.cancel)
async def cancel_processing(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer("❌ Операция отменена", reply_markup=main_menu_markup)


@router.message(AddTransaction.amount)
async def process_amount(message: types.Message, state: FSMContext):
    try:
        amount = float(message.text.replace(',', '.'))

        if amount <= 0:
            raise ValueError

        await state.update_data(amount=amount)
        await state.set_state(AddTransaction.category)
        await message.answer("Отлично! Теперь введите категорию (например, 'Продукты', 'Зарплата', 'Транспорт').",
                             reply_markup=transactions_markup)
    except ValueError:
        await message.answer("Неверный формат. Пожалуйста, введите положительное число (например, 1500 или 99.90).",
                             reply_markup=transactions_markup)


@router.message(AddTransaction.category)
async def process_category(message: types.Message, state: FSMContext):
    data = await state.get_data()
    # TODO: Вызываем функцию для добавления транзакции в базу данных
    await message.answer(
        f"✅ Транзакция успешно добавлена: **{data['amount']}** в категории '{message.text}'.",
        reply_markup=main_menu_markup,
        parse_mode="Markdown"
    )
    await state.clear()
