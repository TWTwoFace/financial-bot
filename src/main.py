import asyncio
import logging
from aiogram import Bot, Dispatcher, F, types
from src.config import BOT_TOKEN
from src.database import database
from src.api.test_router import router

from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.filters import CommandStart
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton


logging.basicConfig(level=logging.INFO)
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

dp.startup.register(database.connect)
dp.shutdown.register(database.disconnect)

dp.include_router(router)


# --- Определение состояний для машины состояний (FSM) ---
# Создаем класс, который будет хранить состояния для процесса добавления транзакции
class AddTransaction(StatesGroup):
    amount = State()      # Состояние, когда бот ожидает ввода суммы
    category = State()    # Состояние, когда бот ожидает ввода категории


# --- Обработчики команд и сообщений ---


@dp.message(CommandStart())
async def cmd_start(message: types.Message):
    """Обработчик команды /start. Приветствует пользователя."""
    await message.answer(
        "Добро пожаловать в бот 'Финансовый Ассистент'! 👋\n\n"
        "Я помогу вам отслеживать доходы и расходы, а также анализировать ваши траты.\n"
        "Используйте меню ниже для навигации.",
        reply_markup=main_menu
    )


#Главное меню бота
# Создание объекта клавиатуры главного меню (Reply-клавиатура)
main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="➕ Добавить расход"), KeyboardButton(text="💰 Добавить доход")],
        [KeyboardButton(text="📊 Баланс & Статистика"), KeyboardButton(text="🎯 Цели")],
        [KeyboardButton(text="ℹ️ Помощь")]
    ],
    resize_keyboard=True, # Автоматически подгоняет размер кнопок
    input_field_placeholder="Выберите раздел в меню" # Текст-подсказка в поле ввода
)


# Создание объекта встроенной (inline) клавиатуры для раздела статистики
stats_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="📈 Аналитика за месяц", callback_data="monthly_analytics")]
    ]
)


@dp.message(F.text.lower() == "ℹ️ помощь")
async def cmd_help(message: types.Message):
    """Обработчик кнопки 'Помощь'."""
    help_text = (
        "**Как пользоваться ботом:**\n\n"
        "🔹 **Добавить расход/доход** — используйте эти кнопки, чтобы записать ваши транзакции. Бот запросит сумму и категорию.\n\n"
        "🔹 **Баланс и статистика** — покажет ваш текущий баланс и предложит посмотреть аналитику за месяц: самую крупную покупку и самую частую категорию трат.\n\n"
        "🔹 **Цели** — эта функция находится в разработке, но скоро позволит вам ставить финансовые цели."
    )
    # Отправляем сообщение с форматированием Markdown
    await message.answer(help_text, parse_mode="Markdown")


@dp.message(F.text.lower() == "➕ Добавить расход")
async def start_add_expense(message: types.Message, state: FSMContext):
    """Начинает процесс добавления расхода."""
    # Устанавливаем пользователю состояние 'amount' (ожидание ввода суммы)
    await state.set_state(AddTransaction.amount)
    # Сохраняем во временное хранилище FSM тип транзакции
    await state.update_data(type='expense')
    await message.answer("Введите сумму расхода:")


@dp.message(F.text.lower() == "💰 Добавить доход")
async def start_add_income(message: types.Message, state: FSMContext):
    """Начинает процесс добавления дохода."""
    # Устанавливаем пользователю состояние 'amount' (ожидание ввода суммы)
    await state.set_state(AddTransaction.amount)
    # Сохраняем во временное хранилище FSM тип транзакции
    await state.update_data(type='income')
    await message.answer("Введите сумму дохода:")


@dp.message(AddTransaction.amount)
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


@dp.message(AddTransaction.category)
async def process_category(message: types.Message, state: FSMContext):
    """Обрабатывает категорию и сохраняет транзакцию."""
    # Получаем все сохраненные ранее данные из хранилища (тип, сумма)
    data = await state.get_data()
    # Вызываем функцию для добавления транзакции в базу данных
    await database.add_transaction(
        user_id=message.from_user.id,
        type=data['type'],
        amount=data['amount'],
        category=message.text
    )

    # Отправляем подтверждение пользователю
    await message.answer(
        f"✅ Транзакция успешно добавлена: **{data['amount']}** в категории '{message.text}'.",
        reply_markup=main_menu,
        parse_mode="Markdown"
    )
    # Сбрасываем состояние пользователя, завершая процесс
    await state.clear()


@dp.message(F.text.lower() == "📊 Баланс & Статистика")
async def show_balance_and_stats(message: types.Message):
    """Показывает баланс и предлагает опции для аналитики."""
    # Получаем текущий баланс пользователя из базы данных
    balance = await database.get_balance(message.from_user.id)
    # Отправляем сообщение с балансом и встроенной клавиатурой
    await message.answer(
        f"Ваш текущий баланс: **{balance:.2f}**\n\n"
        "Выберите опцию для получения детальной статистики.",
        reply_markup=stats_keyboard,
        parse_mode="Markdown"
    )


@dp.callback_query(F.data == "monthly_analytics")
async def show_monthly_analytics(callback: types.CallbackQuery):
    """Показывает аналитику за месяц по нажатию на кнопку."""
    # Получаем данные для аналитики из базы данных
    analytics = await database.get_monthly_analytics(callback.from_user.id)
    biggest = analytics.get('biggest')
    frequent = analytics.get('frequent')

    # Формируем текстовый ответ
    response_text = "📊 **Аналитика за этот месяц**\n\n"
    if biggest:
        response_text += f"🔹 **Самая крупная покупка**: {biggest[1]:.2f} в категории '{biggest[0]}'.\n"
    else:
        response_text += "🔹 В этом месяце расходов еще не было.\n"

    if frequent:
        response_text += f"🔹 **Самая частая категория трат**: '{frequent[0]}' ({frequent[1]} раз).\n"
    else:
        response_text += "🔹 Паттерны расходов пока не определены.\n"

    # Отправляем ответное сообщение
    await callback.message.answer(response_text, parse_mode="Markdown")
    # Отвечаем на колбэк, чтобы убрать значок "загрузки" с кнопки
    await callback.answer()  # Закрываем уведомление о загрузке


async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
