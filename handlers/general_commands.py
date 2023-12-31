import time
import base64
import random

import aiogram
from aiogram import F
from aiogram.filters import Command
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorCollection
from bson import ObjectId
from aiogram.fsm.context import FSMContext

from keyboards import get_null_answer_keyboard
from states import MainStatesGroup

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

@dp.message(Command("start"))
async def start(mes: aiogram.types.Message, state: FSMContext, command, db: AsyncIOMotorClient, bot):
    await mes.answer("Привет! Как тебя зовут?", reply_markup=get_null_answer_keyboard())
    await state.clear()
    await state.set_state(MainStatesGroup.user_name)
    if not await db["user"].count_documents({ "id": mes.from_user.id }):
        await db["user"].insert_one({
            "id": mes.from_user.id,
            "username": mes.from_user.username,
            "name": mes.from_user.username
        })
    if not await db["user"].count_documents({}):
        await db["user"].create_index({"id": 1 }, { "unique": True })
        await db["user"].create_index({"name": 1 }, { "unique": True })
    if command.args:
        await enter_queue(mes, command, db, bot)

@dp.message(Command("create_queue"))
async def create_queue(mes: aiogram.types.Message, db: AsyncIOMotorClient, command):
    timee = str(time.time())
    name = command.args if command.args and command.args.strip() != "-" else  timee
    result = await db["queue"].insert_one({
        "time": timee,
        "name": name,
        "creator_user_id": mes.from_user.id,
        "times_2_users": { timee: mes.from_user.id }
    })
    await mes.answer(f"Создана очередь {name} c id: ")
    await mes.answer(f"{result.inserted_id}")
    #await mes.answer(f"/enter_queue {str(result.inserted_id)}")
    return result.inserted_id


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
async def get_queue_info(mes: aiogram.types.Message, command, db: AsyncIOMotorClient, bot: aiogram.Bot):
    queue = await db["queue"].find_one({ "_id": ObjectId(command.args)})
    
    listt2 = []
    for i in queue["times_2_users"].values():
        user = await db.user.find_one({ "id": i })
        user = user["name"] if user and "name" in user else i
        listt2.append(user)

    await mes.answer(f"""Очедь {queue["name"]}
Время создания: {queue["time"]}
Создатель: {queue["creator_user_id"]}
""" + "\n".join([f"{i}. {v}" for i, v in enumerate(listt2)]) )


@dp.message(Command("shuffle_queue"))
async def shuffle_queue(mes: aiogram.types.Message, command, db: AsyncIOMotorClient, bot: aiogram.Bot):
    queue = await db["queue"].find_one({ "_id": ObjectId(command.args)})
    users = list(queue["times_2_users"].values())
    random.shuffle(users)
    await db["queue"].update_one(
        { "_id": queue["_id"] },
        { "$set": { "list": users }  }
    )


@dp.message(Command("get_queue"))
async def get_queue(mes: aiogram.types.Message, command, db: AsyncIOMotorClient, bot: aiogram.Bot):
    queue = await db["queue"].find_one({ "_id": ObjectId(command.args)})
    listt = queue["list"] if queue.get("list") else queue["times_2_users"].values()
    listt2 = []
    for i in listt:
        user = await db.user.find_one({ "id": i })
        user = user["name"] if user and "name" in user else i
        listt2.append(user)
    await mes.answer(f"\n".join([f"{i}. {v}" for i, v in enumerate(listt2)]) )


@dp.message(Command("set_my_name"))
async def set_my_name(mes: aiogram.types.Message, command, db: AsyncIOMotorClient, bot: aiogram.Bot):
    name = command.args if command.args and command.args.strip() != "-" else  mes.from_user.username
    await db["user"].update_one({ "id": mes.from_user.id }, { "$set": { "name": name  }  } )
    await mes.answer(f"Привет, {name}!", reply_markup=None)

