import logging
import asyncio
import sys


from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram import types

from utils.mk_database import mk_database
from config import api_key, data_base_path, logs_path
from router import router
from handlers import start, mk_basic_qr, payment


logger = logging.getLogger(__name__)
file_handler = logging.FileHandler(filename=logs_path + "logs.log")
stram_handler = logging.StreamHandler()
formatter = logging.Formatter(fmt="%(asctime)s - %(name)s - %(message)s")

stram_handler.setLevel("INFO")
file_handler.setLevel("INFO")
file_handler.setFormatter(formatter)
stram_handler.setFormatter(formatter)
logger.addHandler(file_handler)
logger.addHandler(stram_handler)

logger.setLevel("INFO")


async def main():
    logger.info("подключение к базе данных")
    mk_database(data_base_path)

    logger.info("запуск бота")
    bot = Bot(
        token=api_key,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    dp = Dispatcher(
        storage=MemoryStorage()
    )

    dp.include_router(router=router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=['messages'], close_bot_session=True)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        sys.exit()
