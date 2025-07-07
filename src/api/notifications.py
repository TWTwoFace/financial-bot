from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from src.config import config
from src.markups.notifications import notifications_markup

router = Router()


@router.message(F.text == config.markups.main_menu.notifications)
async def process_notifications(message: Message):
    await message.answer(
        "Выберите дейтсвие",
        reply_markup=notifications_markup
    )

