from aiogram import Router, F, types

from src.config import *
from src.markups.statistics import stats_markup
from src.repositories.statistics import StatsRepository
from src.schemas.users import UserSchema

router = Router()


@router.message(F.text == config.markups.main_menu.statistics)
async def show_balance_and_stats(message: types.Message):
    # TODO: получение баланса пользователя из бд
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
    # Получаем данные для аналитики из базы данных
    #analytics = await database.get_monthly_analytics(callback.from_user.id)
    # biggest = analytics.get('biggest')
    # frequent = analytics.get('frequent')
    #
    # # Формируем текстовый ответ
    # response_text = "📊 **Аналитика за этот месяц**\n\n"
    # if biggest:
    #     response_text += f"🔹 **Самая крупная покупка**: {biggest[1]:.2f} в категории '{biggest[0]}'.\n"
    # else:
    #     response_text += "🔹 В этом месяце расходов еще не было.\n"
    #
    # if frequent:
    #     response_text += f"🔹 **Самая частая категория трат**: '{frequent[0]}' ({frequent[1]} раз).\n"
    # else:
    #     response_text += "🔹 Паттерны расходов пока не определены.\n"
    #
    # # Отправляем ответное сообщение
    # await callback.message.answer(response_text, parse_mode="Markdown")
    # # Отвечаем на колбэк, чтобы убрать значок "загрузки" с кнопки
    # await callback.answer()  # Закрываем уведомление о загрузке
    await callback.message.answer("В разработке", parse_mode="Markdown")
    await callback.answer()
