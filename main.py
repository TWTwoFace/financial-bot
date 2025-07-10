import asyncio
import logging

from aiogram import Dispatcher

from src.api import main_router
from src.bot import bot
from src.events import router as events_router
from src.jobs.notifications import notify_users_job

logging.basicConfig(level=logging.INFO)


dp = Dispatcher()

dp.include_router(events_router)
dp.include_router(main_router)


async def main():
    asyncio.create_task(notify_users_job())
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
