from aiogram import Router

from src.database import database

router = Router()

router.startup.register(database.connect)
router.shutdown.register(database.disconnect)
