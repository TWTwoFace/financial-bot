from aiogram import Router, types, F
from aiogram.filters import CommandStart

from src.config import *
from src.markups.main_menu import main_menu_markup

router = Router()


@router.message(CommandStart())
async def cmd_start(message: types.Message):
    await message.answer(
        "Добро пожаловать в бот 'Финансовый Ассистент'! 👋\n\n"
        "Я помогу вам отслеживать доходы и расходы, а также анализировать ваши траты.\n"
        "Используйте меню ниже для навигации.",
        reply_markup=main_menu_markup
    )


@router.message(F.text == config.markups.main_menu.help)
async def cmd_help(message: types.Message):
    help_text = (
        "**Как пользоваться ботом:**\n\n"
        "🔹 **Добавить расход/доход** — используйте эти кнопки, чтобы записать ваши транзакции. Бот запросит сумму и категорию.\n\n"
        "🔹 **Баланс и статистика** — покажет ваш текущий баланс и предложит посмотреть аналитику за месяц: самую крупную покупку и самую частую категорию трат.\n\n"
        "🔹 **Цели** — эта функция находится в разработке, но скоро позволит вам ставить финансовые цели."
    )
    await message.answer(help_text, parse_mode="Markdown")
