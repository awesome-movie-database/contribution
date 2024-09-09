from aiogram import Dispatcher, Router

from .routers import start_router


def setup_routes(dispatcher: Dispatcher) -> None:
    router = Router()

    router.include_router(start_router)

    dispatcher.include_router(router)
