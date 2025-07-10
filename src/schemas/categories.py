from pydantic import BaseModel


class CategorySchema(BaseModel):
    category: str
    total: float
