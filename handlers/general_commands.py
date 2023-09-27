import time
import base64
import random

import aiogram
from aiogram import F
from aiogram.filters import Command
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorCollection
from bson import ObjectId

dp = aiogram.Router()

@dp.message(Command("help"))
async def help(mes: aiogram.types.Message):
    await mes.answer("What can i help you")

@dp.message(Command("settings"))
async def settings(mes: aiogram.types.Message):
    await mes.answer("Ok")

@dp.message(Command("support"))
async def support(mes: aiogram.types.Message):
    await mes.answer("My")

#@dp.message(Command("start"))
#async def start(mes: aiogram.types.Message, command):
#    await mes.answer("Hi" + str(command.args))

@dp.message(Command("create_queue"))
async def create_queue(mes: aiogram.types.Message, db: AsyncIOMotorClient, command):
    timee = str(time.time())
    result = await db["queue"].insert_one({
        "time": timee,
        "name": command.args if command.args else f"{timee}",
        "creator_user_id": mes.from_user.id,
        "times_2_users": { timee: mes.from_user.id }
    })
    invite = f"/enter_queue {str(result.inserted_id)}"
    await mes.answer(invite)


@dp.message(Command("enter_queue"))
async def enter_queue(mes: aiogram.types.Message, command, db: AsyncIOMotorClient, bot: aiogram.Bot):
    queue = await db["queue"].find_one({ "_id": ObjectId(command.args)})
    times_2_users = queue["times_2_users"]
    if mes.from_user.id in set(queue["times_2_users"].values()):
        await mes.answer("Вы уже есть в очереди")
        return
    times_2_users[str(time.time())] = mes.from_user.id
    await db["queue"].update_one(
        { "_id": queue["_id"] },
        { "$set": { "times_2_users": times_2_users }  }
    )
    if "list" in queue:
        await db["queue"].update_one(
            { "_id": queue["_id"] },
            { "$set": { "list": queue["list"] + [mes.from_user.id] }  }
        )
    await bot.send_message(queue["creator_user_id"], f"@{mes.from_user.username} присоеденяется к очереди {queue['name']} ")


@dp.message(Command("get_queue_info"))
async def enter_queue(mes: aiogram.types.Message, command, db: AsyncIOMotorClient, bot: aiogram.Bot):
    queue = await db["queue"].find_one({ "_id": ObjectId(command.args)})
    await mes.answer(f"""Очедь {queue["name"]}
Время создания: {queue["time"]}
Создатель: {queue["creator_user_id"]}
""" + "\n".join([f"{i}. {v}" for i, v in enumerate(queue["times_2_users"].values())]) )


@dp.message(Command("shuffle_queue"))
async def enter_queue(mes: aiogram.types.Message, command, db: AsyncIOMotorClient, bot: aiogram.Bot):
    queue = await db["queue"].find_one({ "_id": ObjectId(command.args)})
    users = list(queue["times_2_users"].values())
    random.shuffle(users)
    await db["queue"].update_one(
        { "_id": queue["_id"] },
        { "$set": { "list": users }  }
    )


@dp.message(Command("get_queue"))
async def enter_queue(mes: aiogram.types.Message, command, db: AsyncIOMotorClient, bot: aiogram.Bot):
    queue = await db["queue"].find_one({ "_id": ObjectId(command.args)})
    if queue.get("list"):
        await mes.answer(f"\n".join([f"{i}. {v}" for i, v in enumerate(queue["list"])]) )
    else:
        await mes.answer(f"\n".join([f"{i}. {v}" for i, v in enumerate(queue["times_2_users"].values())]) )



