from pydantic import BaseModel


class TransactionSchema(BaseModel):
    user_id: str
    value: float
    category: str
