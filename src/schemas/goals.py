from pydantic import BaseModel


class AddGoalSchema(BaseModel):
    user_id: int
    max_value: float


class GoalSchema(AddGoalSchema):
    id: int
