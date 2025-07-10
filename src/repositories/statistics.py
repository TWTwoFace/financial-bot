import datetime
import logging

from src.database import database
from src.schemas.categories import CategorySchema
from src.schemas.users import UserSchema


class StatsRepository:
    @staticmethod
    async def get_balance(user: UserSchema) -> float:
        try:
            record = await database.fetchone(f"SELECT "
                                             f"(SELECT COALESCE(SUM(value), 0) FROM incomes WHERE user_id = users.id) -"
                                             f"(SELECT COALESCE(SUM(value), 0) FROM expenses WHERE user_id = users.id) "
                                             f"AS balance "
                                             f"FROM users "
                                             f"WHERE users.telegram_id = '{user.telegram_id}'")
            balance = record['balance']
            return balance
        except Exception as e:
            logging.error(e)
            return 0

    @staticmethod
    async def get_balance_by_month(user: UserSchema) -> float:
        try:
            current_date = datetime.date.today() + datetime.timedelta(days=1)
            begin_month_date = datetime.date.today().replace(day=1)
            record = await database.fetchone(f"SELECT "
                                             f"(SELECT COALESCE(SUM(value), 0) FROM incomes WHERE user_id = users.id "
                                             f"AND date BETWEEN '{begin_month_date}' AND '{current_date}') -"
                                             f"(SELECT COALESCE(SUM(value), 0) FROM expenses WHERE user_id = users.id "
                                             f"AND date BETWEEN '{begin_month_date}' AND '{current_date}') "
                                             f"AS balance "
                                             f"FROM users "
                                             f"WHERE users.telegram_id = '{user.telegram_id}'")
            balance = record['balance']
            return balance
        except Exception as e:
            logging.error(e)
            return 0

    @staticmethod
    async def get_expenses_top_categories(user: UserSchema, date_after: str, count: int):
        try:
            records = await database.fetchmany(f"SELECT category, SUM(value) AS total "
                                               f"FROM expenses WHERE user_id = '{user.id}' AND date > '{date_after}' "
                                               f"GROUP BY category ORDER BY total DESC LIMIT {count}")
            categories = [CategorySchema(**record) for record in records]
            return categories
        except Exception as e:
            logging.error(e)
            return []

    @staticmethod
    async def get_incomes_top_categories(user: UserSchema, date_after: str, count: int):
        try:
            records = await database.fetchmany(f"SELECT category, SUM(value) AS total "
                                               f"FROM incomes WHERE user_id = '{user.id}' AND date > '{date_after}' "
                                               f"GROUP BY category ORDER BY total DESC LIMIT {count}")
            categories = [CategorySchema(**record) for record in records]
            return categories
        except Exception as e:
            logging.error(e)
            return []
