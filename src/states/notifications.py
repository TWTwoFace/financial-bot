from aiogram.fsm.state import StatesGroup, State


class AddNotification(StatesGroup):
    description = State()
    date = State()


class RemoveNotification(StatesGroup):
    to_remove = State()
    notifications = State()
