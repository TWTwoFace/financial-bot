import asyncio
from asyncio import Task

from dateutil.parser import parse
from dateutil.relativedelta import relativedelta

from src.bot import bot

from src.repositories.notifications import NotificationsRepository
from src.repositories.users import UsersRepository


async def notify_users():
    notifications = await NotificationsRepository.get_fired_notifications()
    for notification in notifications:
        user = await UsersRepository.get_user(notification.user_id)
        await bot.send_message(chat_id=user.telegram_id, text=f"Уведомление:\n\n"
                                                              f"'{notification.description}' уже сегодня\n"
                                                              f"Не забудте провести оплату.")
        new_date = parse(notification.last_date) + relativedelta(months=1)
        await NotificationsRepository.update_notification_date(notification, str(new_date))


async def notify_users_job():
    while True:
        await asyncio.sleep(3600)
        await notify_users()
