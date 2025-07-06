import asyncio
import logging

from aiogram import Bot, Dispatcher

from src.api import main_router
from src.events import router as events_router
from src.config import config

logging.basicConfig(level=logging.INFO)

bot = Bot(token=config.bot.token)
dp = Dispatcher()

dp.include_router(events_router)
dp.include_router(main_router)


async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
