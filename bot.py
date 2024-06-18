import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode

from bot.handlers import user_handlers
from bot.callbacks import user_callbacks
from storage.models import start_db
from config import BOT_TOKEN


async def main() -> None:
    await start_db()

    bot = Bot(BOT_TOKEN, parse_mode=ParseMode.HTML,
              disable_web_page_preview=True)
    dp = Dispatcher()

    dp.include_routers(user_callbacks.router, user_handlers.router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    loop = asyncio.get_event_loop()

    loop.run_until_complete(main())
