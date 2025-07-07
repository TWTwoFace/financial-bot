from pydantic import BaseModel


class UserSchema(BaseModel):
    id: int = 0
    telegram_id: str
