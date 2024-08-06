import os

from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types, Router
from aiogram.filters import CommandStart, Command
from motor.motor_asyncio import AsyncIOMotorClient
from aiogram.fsm.context import FSMContext
from aiogram.filters.state import State, StatesGroup
from crud.db_config import mongo_db, init_redis_pool
from crud.messages import MessagesCRUD
from schemas.messages import MessageDBList
from schemas.utils import TgOutputAdapter
from constants import MSG_PATTERN, MSG_TG_BOT_CACHE_KEY


load_dotenv()

db: AsyncIOMotorClient = MessagesCRUD(mongo_db, 'messages')


async def get_cache():
    return await init_redis_pool()

bot = Bot(token=os.getenv('TG_BOT_TOKEN'))
dp = Dispatcher()
form_router = Router()
dp.include_router(form_router)


class Form(StatesGroup):
    text = State() 

@dp.message(CommandStart())
async def start_cmd(message: types.Message) -> None:

    await message.answer('Привет, функционал в menu.')

@form_router.message(Command("send"))
async def send_cmd(message: types.Message, state: FSMContext) -> None:

    await state.set_state(Form.text)
    await message.answer("Можно передевать сообщения. Прервать /end")

@form_router.message(Form.text)
async def process_text(message: types.Message, state: FSMContext) -> None:

    text = message.text
    await state.update_data(text=text)

    if text == '/end':
        await state.clear()
        await message.answer("Отправка сообщений завершена.")
    else:
        await db.create_document(
            {'username': message.from_user.username, 'text': text},
        )
        await message.answer("Сообщение успешно сохранено.")

    cache = await get_cache()
    keys = await cache.keys(MSG_PATTERN)
    if keys:
        await cache.delete(*keys)

@dp.message(Command('getall'))
async def get_msg_cmd(message: types.Message):

    cache = await get_cache()
    cache_data = await cache.get(MSG_TG_BOT_CACHE_KEY)
    if cache_data:
        return message.answer(cache_data) 
    
    cursor = db.get_all_document()
    result = []
    async for msg in cursor:
        result.append(msg)

    data_to_transform = MessageDBList(messages=result).model_dump(by_alias=True) # noqa E501
    output_data = TgOutputAdapter(data_to_transform['messages']).transform()
    await cache.set(MSG_TG_BOT_CACHE_KEY, output_data)
    return message.answer(output_data) 


async def start_polling():
    await dp.start_polling(bot)