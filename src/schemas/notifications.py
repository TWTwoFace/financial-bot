from pydantic import BaseModel


class AddNotificationSchema(BaseModel):
    user_id: int
    description: str
    last_date: str


class NotificationSchema(AddNotificationSchema):
    id: int



