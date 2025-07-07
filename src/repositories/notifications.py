import logging

from src.database import database
from src.schemas.notifications import AddNotificationSchema, NotificationSchema
from src.schemas.users import UserSchema


class NotificationsRepository:
    @staticmethod
    async def add_notification(notification: AddNotificationSchema) -> bool:
        try:
            await database.execute(f"INSERT INTO notifies(user_id, last_date, description) "
                                   f"VALUES ('{notification.user_id}', '{notification.last_date}', '{notification.description}')")
            return True
        except Exception as e:
            logging.error(e)
            return False

    @staticmethod
    async def remove_notification(notification: NotificationSchema) -> bool:
        try:
            await database.execute(f"DELETE FROM notifies WHERE user_id='{notification.user_id}' AND id='{notification.id}'")
            return True
        except Exception as e:
            logging.error(e)
            return False

    @staticmethod
    async def get_notifications_by_user(user: UserSchema):
        try:
            records = await database.fetchmany(f"SELECT * FROM notifies WHERE user_id='{user.id}'")

            notifications = []

            for record in records:
                notifications.append(
                    NotificationSchema(
                        id=record['id'],
                        user_id=record['user_id'],
                        description=record['description'],
                        last_date=str(record['last_date'])
                    )
                )
            return notifications
        except Exception as e:
            logging.error(e)
            return None

    @staticmethod
    async def get_fired_notifications():
        try:
            records = await database.fetchmany(f"SELECT * FROM notifies WHERE CURRENT_TIMESTAMP > notifies.last_date")

            notifications = []

            for record in records:
                notifications.append(
                    NotificationSchema(
                        id=record['id'],
                        user_id=record['user_id'],
                        description=record['description'],
                        last_date=str(record['last_date'])
                    )
                )
            return notifications
        except Exception as e:
            logging.error(e)
            return None

    @staticmethod
    async def update_notification_date(notification: NotificationSchema, new_date: str):
        try:
            await database.execute(f"UPDATE notifies SET last_date='{new_date}' WHERE id='{notification.id}'")
            return True
        except Exception as e:
            logging.error(e)
            return False
