from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardRemove

from src.config import *
from src.markups.main_menu import main_menu_markup
from src.states.transactions import AddTransaction

router = Router()


@router.message(F.text == config.markups.main_menu.add_expense)
async def start_add_expense(message: types.Message, state: FSMContext):
    """Начинает процесс добавления расхода."""
    # Устанавливаем пользователю состояние 'amount' (ожидание ввода суммы)
    await state.set_state(AddTransaction.amount)
    # Сохраняем во временное хранилище FSM тип транзакции
    await state.update_data(type='expense')
    await message.answer("Введите сумму расхода:", reply_markup=ReplyKeyboardRemove())


@router.message(F.text == config.markups.main_menu.add_income)
async def start_add_income(message: types.Message, state: FSMContext):
    """Начинает процесс добавления дохода."""
    # Устанавливаем пользователю состояние 'amount' (ожидание ввода суммы)
    await state.set_state(AddTransaction.amount)
    # Сохраняем во временное хранилище FSM тип транзакции
    await state.update_data(type='income')
    await message.answer("Введите сумму дохода:", reply_markup=ReplyKeyboardRemove())


@router.message(AddTransaction.amount)
async def process_amount(message: types.Message, state: FSMContext):
    """Обрабатывает введенную сумму."""
    try:
        # Пытаемся преобразовать текст сообщения в число
        amount = float(message.text.replace(',', '.'))
        # Сохраняем сумму во временное хранилище
        await state.update_data(amount=amount)
        # Переводим пользователя в следующее состояние 'category'
        await state.set_state(AddTransaction.category)
        await message.answer("Отлично! Теперь введите категорию (например, 'Продукты', 'Зарплата', 'Транспорт').")
    except ValueError:
        # Если преобразование не удалось, просим ввести сумму еще раз
        await message.answer("Неверный формат. Пожалуйста, введите число (например, 1500 или 99.90).")


@router.message(AddTransaction.category)
async def process_category(message: types.Message, state: FSMContext):
    """Обрабатывает категорию и сохраняет транзакцию."""
    # Получаем все сохраненные ранее данные из хранилища (тип, сумма)
    data = await state.get_data()
    # Вызываем функцию для добавления транзакции в базу данных

    # Отправляем подтверждение пользователю
    await message.answer(
        f"✅ Транзакция успешно добавлена: **{data['amount']}** в категории '{message.text}'.",
        reply_markup=main_menu_markup,
        parse_mode="Markdown"
    )
    # Сбрасываем состояние пользователя, завершая процесс
    await state.clear()
