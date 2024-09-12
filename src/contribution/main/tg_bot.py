from typing import Optional

from aiogram import Bot, Dispatcher

from contribution.infrastructure import env_var_by_key, setup_logging
from contribution.presentation.tg_bot import setup_routes


class TgBotApp:
    def __init__(self, *, bot: Bot, dispatcher: Dispatcher):
        self._bot = bot
        self._dispatcher = dispatcher

    async def start(self, polling_timeout: float) -> None:
        await self._dispatcher.start_polling(
            self._bot,
            polling_timeout=polling_timeout,
        )


def create_tg_bot_app(tg_bot_token: Optional[str] = None) -> TgBotApp:
    tg_bot_token = tg_bot_token or env_var_by_key("TG_BOT_TOKEN")
    bot = Bot(token=tg_bot_token)
    dispatcher = Dispatcher()

    setup_logging()
    setup_routes(dispatcher)

    return TgBotApp(
        bot=bot,
        dispatcher=dispatcher,
    )
