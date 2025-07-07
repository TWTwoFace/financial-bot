import logging

from src.database import database
from src.schemas.users import UserSchema


class UsersRepository:
    @staticmethod
    async def add_user(user: UserSchema) -> bool:
        try:
            await database.execute(f"INSERT INTO users (telegram_id) VALUES ('{user.telegram_id}')")
            return True
        except Exception as e:
            logging.error(e)
            return False

    @staticmethod
    async def is_user_exists(user: UserSchema) -> bool:
        try:
            record = await database.fetchone(f"SELECT COUNT(*) > 0 as exists FROM users WHERE telegram_id='{user.telegram_id}'")
            return record["exists"]
        except Exception as e:
            logging.error(e)
            return False

    @staticmethod
    async def get_user_by_telegram(telegram_id: str) -> UserSchema:
        try:
            record = await database.fetchone(f"SELECT * FROM users WHERE telegram_id='{telegram_id}'")
            user = UserSchema(**record)
            return user
        except Exception as e:
            logging.error(e)

    @staticmethod
    async def get_user(user_id) -> UserSchema:
        try:
            record = await database.fetchone(f"SELECT * FROM users WHERE id='{user_id}'")
            user = UserSchema(**record)
            return user
        except Exception as e:
            logging.error(e)
