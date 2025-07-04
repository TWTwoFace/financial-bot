from aiogram.dispatcher.router import Router
from aiogram import types
from aiogram.filters.command import Command

router = Router(name="test")


@router.message(Command("start"))
async def say_hello(message: types.Message):
    await message.answer("Hello!")
