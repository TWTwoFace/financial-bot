from src.database import database
from src.schemas.transactions import TransactionSchema


class TransactionsRepository:
    @staticmethod
    async def add_expense(expense: TransactionSchema) -> bool:
        try:
            await database.execute(f"INSERT INTO expenses (user_id, value, category) "
                                   f"VALUES ('{expense.user_id}', '{expense.value}', '{expense.category}')")
            return True
        except Exception as e:
            print(e)
            return False

    @staticmethod
    async def add_income(income: TransactionSchema) -> bool:
        try:
            await database.execute(f"INSERT INTO incomes (user_id, value, category) "
                                   f"VALUES ('{income.user_id}', '{income.value}', '{income.category}')")
            return True
        except Exception as e:
            print(e)
            return True
