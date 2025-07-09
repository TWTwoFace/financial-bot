from aiogram.fsm.state import StatesGroup, State


class SetGoal(StatesGroup):
    max_value = State()
