from aiogram import Router, types, F
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext

from src.config import *
from src.markups.main_menu import main_menu_markup
from src.repositories.users import UsersRepository
from src.schemas.users import UserSchema

router = Router()


@router.message(CommandStart())
async def cmd_start(message: types.Message):
    user = UserSchema(telegram_id=str(message.from_user.id))
    user_exists = await UsersRepository.is_user_exists(user)
    if not user_exists:
        await UsersRepository.add_user(user)
    await message.answer(
        "Добро пожаловать в бот 'Финансовый Ассистент'! 👋\n\n"
        "Я помогу вам отслеживать доходы и расходы, а также анализировать ваши траты.\n"
        "Используйте меню ниже для навигации.",
        reply_markup=main_menu_markup
    )


@router.message((F.text == config.markups.main_menu.help) | (F.text == '/help'))
async def cmd_help(message: types.Message):
    help_text = (
        "**Как пользоваться ботом:**\n\n"
        "🔹 **Добавить расход/доход** — используйте, чтобы записать ваши транзакции. Бот запросит сумму и категорию.\n\n"
        "🔹 **Баланс и статистика** — покажет ваш текущий баланс и предложит посмотреть аналитику за месяц: Доходы, расходы и ваш топ категорий за текущий месяц.\n\n"
        "🔹 **Цели** — используйте, чтобы поставить цель (лимит) на расходы за месяц\n\n"
        "🔹 **Уведомления** - используйте, чтобы создать ежемесячное уведомление и не пропустить оплату"
    )
    await message.answer(help_text, parse_mode="Markdown")


@router.message(F.text == config.markups.back)
async def go_back(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer("↪ Выход назад", reply_markup=main_menu_markup)