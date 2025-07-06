from aiogram.fsm.state import StatesGroup, State


class AddTransaction(StatesGroup):
    amount = State()
    category = State()
