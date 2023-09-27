import aiogram
import os

from motor.motor_asyncio import AsyncIOMotorClient

from handlers import general_commands

async def run_bot():
    token = os.environ.get("TELEGRAM_API_TOKEN")
    dp = aiogram.Dispatcher()
    dp.include_router(general_commands.dp)
    bot = aiogram.Bot(token)
    db = AsyncIOMotorClient(os.environ.get("DB_MONGO_URL"))[os.environ.get("DB_NAME")]
    await dp.start_polling(bot, db=db)

    
