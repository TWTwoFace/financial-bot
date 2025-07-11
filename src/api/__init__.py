from aiogram import Router

from src.api.main_menu import router as main_menu_router
from src.api.transactions import router as transactions_router
from src.api.statistics import router as stats_router
from src.api.notifications import router as notifications_router
from src.api.goals import router as goals_router

__all__ = [
    "main_router"
]

main_router = Router()

main_router.include_router(main_menu_router)
main_router.include_router(transactions_router)
main_router.include_router(stats_router)
main_router.include_router(notifications_router)
main_router.include_router(goals_router)
