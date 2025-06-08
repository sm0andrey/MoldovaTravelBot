from aiogram import Bot, Dispatcher, Router, F
import asyncio
from aiogram.types import Message
from aiogram.filters import CommandStart, Command
from routers import cities, greeting, requests
from aiogram.fsm.storage.memory import MemoryStorage
import logging
from config.bot_settings import bot_config
from middleware.log_middleware import MessageLog

bot = Bot(token=bot_config.telegram_api_key)
storage = MemoryStorage()
router=Router()
dp = Dispatcher(storage=storage)


async def main():
    dp.include_router(cities.router)
    dp.include_router(greeting.router)
    dp.include_router(requests.router)
    logging.basicConfig(level=logging.INFO)  # Выставляем уровень логов на INFO
    dp.message.outer_middleware(MessageLog())
    router.message.filter(F.chat.type == 'private')
    dp.include_router(router)
    await dp.start_polling(bot)



asyncio.run(main())
