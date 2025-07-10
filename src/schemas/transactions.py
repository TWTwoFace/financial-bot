from pydantic import BaseModel


class TransactionSchema(BaseModel):
    user_id: int
    value: float
    category: str
