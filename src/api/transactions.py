from aiogram import Router, F, types
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext

from src.config import *
from src.markups.main_menu import main_menu_markup
from src.markups.transactions import transactions_markup, expense_category_markup, income_category_markup
from src.repositories.transactions import TransactionsRepository
from src.repositories.users import UsersRepository
from src.schemas.transactions import TransactionSchema
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
        data = await state.get_data()
        if data['type'] == 'expense':
            await message.answer("Отлично! Теперь Выберите категорию расхода\n\n"
                                 "Или напишите в чат свою категорию:",
                                 reply_markup=expense_category_markup)
        else:
            await message.answer("Отлично! Теперь Выберите категорию дохода\n\n"
                                 "Или напишите в чат свою категорию:",
                                 reply_markup=income_category_markup)
    except ValueError:
        await message.answer("Неверный формат. Пожалуйста, введите положительное число (например, 1500 или 99.90).",
                             reply_markup=transactions_markup)


@router.message(AddTransaction.category)
async def process_category(message: types.Message, state: FSMContext):
    data = await state.get_data()

    user = await UsersRepository.get_user_by_telegram(str(message.from_user.id))

    transaction = TransactionSchema(
        user_id=str(user.id),
        value=data['amount'],
        category=message.text
    )

    if data['type'] == 'expense':
        result = await TransactionsRepository.add_expense(transaction)
    else:
        result = await TransactionsRepository.add_income(transaction)

    if result:
        await message.answer(
            f"✅ Транзакция успешно добавлена: **{data['amount']}** в категории '{message.text}'.",
            reply_markup=main_menu_markup,
            parse_mode="Markdown"
        )
    else:
        await message.answer(
            "❌ Не удалось создать транзакцию",
            reply_markup=main_menu_markup,
            parse_mode="Markdown"
        )
    await state.clear()
