import logging

from src.database import database
from src.schemas.transactions import TransactionSchema
from src.schemas.users import UserSchema


class TransactionsRepository:
    @staticmethod
    async def add_expense(expense: TransactionSchema) -> bool:
        try:
            await database.execute(f"INSERT INTO expenses (user_id, value, category) "
                                   f"VALUES ('{expense.user_id}', '{expense.value}', '{expense.category}')")
            return True
        except Exception as e:
            logging.error(e)
            return False

    @staticmethod
    async def add_income(income: TransactionSchema) -> bool:
        try:
            await database.execute(f"INSERT INTO incomes (user_id, value, category) "
                                   f"VALUES ('{income.user_id}', '{income.value}', '{income.category}')")
            return True
        except Exception as e:
            logging.error(e)
            return True

    @staticmethod
    async def get_user_expenses_sum(user: UserSchema, date_after: str) -> float:
        try:
            record = await database.fetchone(f"SELECT SUM(value) AS sum FROM expenses WHERE user_id='{user.id}' AND date > '{date_after}'")
            expenses_sum = record['sum']
            return expenses_sum
        except Exception as e:
            logging.error(e)
            return 0


