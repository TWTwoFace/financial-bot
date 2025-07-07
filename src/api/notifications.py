import datetime
from dateutil.relativedelta import relativedelta
from dateutil.parser import parse

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from src.config import config
from src.markups.main_menu import main_menu_markup
from src.markups.notifications import notifications_markup, cancel_processing_notifications_markup
from src.repositories.notifications import NotificationsRepository
from src.repositories.users import UsersRepository
from src.schemas.notifications import AddNotificationSchema
from src.states.notifications import AddNotification, RemoveNotification

router = Router()


@router.message(F.text == config.markups.main_menu.notifications)
async def process_notifications(message: Message):
    await message.answer(
        "Выберите дейтсвие",
        reply_markup=notifications_markup
    )


@router.message(F.text == config.markups.notifications.add_notification)
async def add_notification(message: Message, state: FSMContext):
    await state.set_state(AddNotification.description)
    await message.answer(
        "Введите описание уведомления",
        reply_markup=cancel_processing_notifications_markup
    )


@router.message(AddNotification.description)
async def process_notification_description(message: Message, state: FSMContext):
    if len(message.text) > 100:
        await message.answer("Описание уведомления не должно превышать 100 символов\n"
                             "Попробуйте снова")
        return

    await state.update_data(description=message.text)
    await state.set_state(AddNotification.date)
    await message.answer("Введите день месяца для напоминания")


@router.message(AddNotification.date)
async def process_notification_description(message: Message, state: FSMContext):
    try:
        day = int(message.text)

        if day > 31 or day < 1:
            raise ValueError

        notification_date = datetime.datetime.today().replace(day=day)
        if notification_date < datetime.datetime.today():
            notification_date += relativedelta(months=1)

        data = await state.get_data()

        user = await UsersRepository.get_user_by_telegram(str(message.from_user.id))

        notification = AddNotificationSchema(
            user_id=user.id,
            description=data['description'],
            last_date=str(notification_date.date())
        )

        res = await NotificationsRepository.add_notification(notification)

        await state.clear()

        if res:
            await message.answer("Уведомление успешно создано!", reply_markup=main_menu_markup)
        else:
            await message.answer("Ошибка при создании уведомления", reply_markup=main_menu_markup)
    except ValueError:
        await message.answer("Неверный формат дня месяца.\n\n"
                             "Введите число от 1 до 31")


@router.message(F.text == config.markups.notifications.remove_notification)
async def delete_message(message: Message, state: FSMContext):
    user = await UsersRepository.get_user_by_telegram(str(message.from_user.id))
    notifications = await NotificationsRepository.get_notifications_by_user(user)

    if len(notifications) == 0:
        await message.answer("У вас нет действующих уведомлений", reply_markup=main_menu_markup)
        return

    await state.set_state(RemoveNotification.to_remove)

    correspondences = {}

    builder = ReplyKeyboardBuilder()

    for i in range(len(notifications)):
        notification = notifications[i]
        description = notification.description

        if len(description) > 15:
            description = description[:15] + '...'

        text = f"{i + 1}: {description} | День: {parse(notification.last_date).day}"
        correspondences[text] = notification
        builder.button(text=text)

    builder.button(text=config.markups.back)
    builder.adjust(1)

    await state.update_data(notifications=correspondences)

    markup = builder.as_markup()
    markup.resize_keyboard = True

    await message.answer(
        "Выберите уведомление",
        reply_markup=markup,
    )


@router.message(RemoveNotification.to_remove)
async def process_deleting_notification(message: Message, state: FSMContext):
    notification_text = message.text
    data = await state.get_data()
    correspondences: dict = data['notifications']

    if correspondences.get(notification_text) is None:
        await message.answer("Неверный формат.\n"
                             "Выберите уведомления из списка")
        return

    notification = correspondences.get(notification_text)

    res = await NotificationsRepository.remove_notification(notification)

    await state.clear()

    if res:
        await message.answer("Уведомление успешно удалено!", reply_markup=main_menu_markup)
    else:
        await message.answer("Ошибка при удалении уведомления", reply_markup=main_menu_markup)



