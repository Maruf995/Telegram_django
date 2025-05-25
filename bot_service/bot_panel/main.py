import os
import sys
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.client.bot import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from dotenv import load_dotenv

sys.path.append(os.path.abspath(os.path.dirname(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'admin_panel.settings')

import django
django.setup()

load_dotenv()

from handlers import start, catalog, cart, faq, order, check

async def main():
    bot_token = os.getenv('BOT_TOKEN')
    if not bot_token:
        raise RuntimeError("BOT_TOKEN is not set in environment variables")

    bot = Bot(
        token=bot_token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )

    storage = MemoryStorage()

    dp = Dispatcher(storage=storage)

    dp.include_router(start.router)
    dp.include_router(catalog.router)
    dp.include_router(cart.router)
    dp.include_router(faq.router)
    dp.include_router(order.router)
    dp.include_router(check.router)

    print("Бот успешно запущен!")
    
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
