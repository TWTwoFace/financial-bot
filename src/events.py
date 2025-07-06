from aiogram import Router

from src.database import database
from src.jobs.notifications import start_notifying, stop_notifying

router = Router()

router.startup.register(database.connect)
router.startup.register(start_notifying)
router.shutdown.register(database.disconnect)
router.shutdown.register(stop_notifying)
