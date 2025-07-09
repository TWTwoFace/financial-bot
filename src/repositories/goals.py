import logging

from src.database import database
from src.schemas.goals import GoalSchema, AddGoalSchema
from src.schemas.users import UserSchema


class GoalsRepository:
    @staticmethod
    async def get_user_goal(user: UserSchema):
        try:
            record = await database.fetchone(f"SELECT * FROM goals WHERE user_id='{user.id}'")
            if record is None:
                return None
            goal = GoalSchema(**record)
            return goal
        except Exception as e:
            logging.error(e)

    @staticmethod
    async def add_goal(goal: AddGoalSchema):
        try:
            await database.execute(f"INSERT INTO goals(user_id, max_value) "
                                   f"VALUES ('{goal.user_id}', '{goal.max_value}')")
            return True
        except Exception as e:
            logging.error(e)
            return False

    @staticmethod
    async def change_goal(goal: GoalSchema):
        try:
            await database.execute(f"UPDATE goals SET max_value='{goal.max_value}' WHERE user_id='{goal.user_id}'")
            return True
        except Exception as e:
            logging.error(e)
            return False
