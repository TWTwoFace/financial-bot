from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from datetime import datetime

from src.config import config
from src.markups.goals import goals_markup
from src.markups.main_menu import main_menu_markup
from src.repositories.goals import GoalsRepository
from src.repositories.transactions import TransactionsRepository
from src.repositories.users import UsersRepository
from src.schemas.goals import GoalSchema, AddGoalSchema
from src.states.goals import SetGoal

router = Router()


@router.message(F.text == config.markups.main_menu.goals)
async def process_goals(message: Message):
    await message.answer("Выберите пунк в меню", reply_markup=goals_markup)


@router.message(F.text == config.markups.goals.get_goal)
async def get_goal(message: Message):
    user = await UsersRepository.get_user_by_telegram(str(message.from_user.id))
    goal: GoalSchema = await GoalsRepository.get_user_goal(user)

    if goal is None:
        await message.answer("У вас не установлена цель")
        return

    date = datetime.today().replace(day=1).replace(hour=0).replace(minute=0).replace(second=0)
    expenses_sum = await TransactionsRepository.get_user_expenses_sum(user, str(date))

    filler_text = '\t'

    for i in range(10):
        if goal.max_value / 10 * (i + 1) <= expenses_sum:
            filler_text += '🟩'
        else:
            filler_text += '⬜'

    over_part = expenses_sum - goal.max_value

    while over_part > 0:
        filler_text += '🟥'
        over_part -= goal.max_value / 10

    if len(filler_text) > 16:
        filler_text = filler_text[:16] + '▶'

    filler_text = 'Диаграмма: \n' + filler_text

    about_text = f'Траты / Цель: {expenses_sum} / {goal.max_value}\n\n'

    if expenses_sum > goal.max_value:
        text = f"<b>Цель невыполнена</b>\n\nЗа текущий месяц потрачено на {expenses_sum - goal.max_value}р. больше\n\n"
    else:
        text = f"<b>Цель выполнена</b>\n\nЛимит по тратам на месяц не превышен\n\n"

    await message.answer(text=text+about_text+filler_text, reply_markup=main_menu_markup, parse_mode='HTML')


@router.message(F.text == config.markups.goals.set_goal)
async def set_goal(message: Message, state: FSMContext):
    await state.set_state(SetGoal.max_value)
    await message.answer("Введите максимальную сумму расходов за месяц")


@router.message(SetGoal.max_value)
async def process_max_value(message: Message, state: FSMContext):
    try:
        amount = float(message.text)
        if amount < 5.000:
            raise ValueError

        user = await UsersRepository.get_user_by_telegram(str(message.from_user.id))

        user_goal = await GoalsRepository.get_user_goal(user)

        add_goal = AddGoalSchema(user_id=user.id, max_value=amount)

        if user_goal is None:
            print('1')
            res = await GoalsRepository.add_goal(add_goal)
        else:
            user_goal.max_value = amount
            res = await GoalsRepository.change_goal(user_goal)

        await state.clear()

        if res:
            await message.answer("Цель успешно добавлена!", reply_markup=main_menu_markup)
        else:
            await message.answer("Произошла ошибка при добавлении цели", reply_markup=main_menu_markup)
    except ValueError:
        await message.answer("Введите положительное число от 5.000 и выше")