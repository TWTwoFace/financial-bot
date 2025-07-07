from src.database import database
from src.schemas.users import UserSchema


class StatsRepository:
    @staticmethod
    async def get_balance(user: UserSchema) -> float:
        try:
            record = await database.fetchone(f"SELECT COALESCE(SUM(i.value), 0) - COALESCE(SUM(e.value), 0) AS balance "
                                             f"FROM users "
                                             f"LEFT JOIN incomes i ON users.id = i.user_id "
                                             f"LEFT JOIN expenses e ON users.id = e.user_id "
                                             f"WHERE users.telegram_id = '{user.telegram_id}' "
                                             f"GROUP BY users.id")
            balance = record['balance']
            return balance
        except Exception as e:
            print(e)
            return 0
