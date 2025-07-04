import asyncio
import logging
from aiogram import Bot, Dispatcher
from src.config import BOT_TOKEN


logging.basicConfig(level=logging.INFO)
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
