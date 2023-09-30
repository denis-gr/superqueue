import aiogram
from aiogram import Router, F
from aiogram.filters import or_f, and_f, CommandObject
from aiogram.fsm.context import FSMContext

from keyboards import get_null_answer_keyboard, get_start_keyboard, get_wait_keyboard
from states import ModelStatesGroup, MainStatesGroup
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorCollection

import handlers.general_commands


dp = Router(name="general_btn")


@dp.message(and_f(MainStatesGroup.user_name, F.text))
async def getted_username(message, state: FSMContext, db: AsyncIOMotorClient, bot: aiogram.Bot):
    command = CommandObject(command="set_my_name", args=message.text)
    await handlers.general_commands.set_my_name(message, command, db, bot)
    await state.set_data({ "user_name": message.text })
    await state.set_state(MainStatesGroup.is_moder)
    await message.answer("Что будетм делать?", reply_markup=get_start_keyboard())


@dp.message(and_f(MainStatesGroup.is_moder, F.text.contains("Создать очередь")))
async def toM(message, state, db: AsyncIOMotorClient, bot: aiogram.Bot):
    await state.set_data({ "is_moder": True })
    await state.set_state(MainStatesGroup.queue_name_M)
    await message.answer("Как назовем нашу очередь?", reply_markup=get_null_answer_keyboard())


@dp.message(and_f(MainStatesGroup.is_moder, F.text.contains("Войти в очередь")))
async def toO(message, state, db: AsyncIOMotorClient, bot: aiogram.Bot):
    await state.set_data({ "is_moder": False })
    await state.set_state(MainStatesGroup.queue_id_O)
    await message.answer("Какой id очереди, в которую нужно войти?", reply_markup=get_null_answer_keyboard())


@dp.message(and_f(MainStatesGroup.queue_name_M, F.text))
async def create_queure_M(message, state: FSMContext, db: AsyncIOMotorClient, bot: aiogram.Bot):
    command = CommandObject(command="create_queue", args=message.text)
    id = await handlers.general_commands.create_queue(message, db, command)
    await state.set_state(MainStatesGroup.users_entered_M)
    await state.set_data({ "queue_id": id })
    await message.answer("Сообщите мне, когда все войдут в очередь", reply_markup=get_null_answer_keyboard())


@dp.message(and_f(MainStatesGroup.queue_id_O, F.text))
async def enter_O(message, state, db: AsyncIOMotorClient, bot: aiogram.Bot):
    await state.set_data({ "queue_id": id })
    command = CommandObject(command="enter_queue", args=message.text)
    await handlers.general_commands.enter_queue(message, command, db, bot)
    await handlers.general_commands.get_queue(message, command, db, bot)
    await state.set_state(MainStatesGroup.is_waiting)
    await message.answer("Что будем делать?", reply_markup=get_wait_keyboard())



@dp.message(and_f(MainStatesGroup.users_entered_M, F.text))
async def getted_users(message, state: FSMContext, db: AsyncIOMotorClient, bot: aiogram.Bot):
    data = await state.get_data()
    command = CommandObject(command="shuffle_queue", args=data["queue_id"])
    await handlers.general_commands.shuffle_queue(message,  command, db, bot)
    await handlers.general_commands.get_queue(message, command, db, bot)
    await state.set_state(MainStatesGroup.is_waiting)
    await message.answer("Что будем делать?", reply_markup=get_wait_keyboard(is_moder=True))

