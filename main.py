import aiogram
import os

from motor.motor_asyncio import AsyncIOMotorClient

from handlers import general_commands, ganeral_btns

async def run_bot():
    token = os.environ.get("TELEGRAM_API_TOKEN")
    dp = aiogram.Dispatcher()
    dp.include_routers(general_commands.dp, ganeral_btns.dp)
    bot = aiogram.Bot(token)
    db = AsyncIOMotorClient(os.environ.get("DB_MONGO_URL"))[os.environ.get("DB_NAME")]
    await dp.start_polling(bot, db=db)

    
