from aiogram.types import Message
from aiogram import Bot, Dispatcher
from aiogram.utils.exceptions import MessageToDeleteNotFound
from aiogram.utils.exceptions import MessageNotModified, RetryAfter
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup

from os import environ

from scripts import *
from keyboards import mainKb

# Токен для получения доступа к боту
TOKEN = environ['TOKEN']
FILE_PATH = f'https://api.telegram.org/file/bot{TOKEN}'

# Класс для работы с Ботом
bot = Bot(TOKEN)

# Создание хранилища для состояний сцен
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


# Игнорирование ошибки при неизмененном сообщении
@dp.errors_handler(exception=MessageNotModified)
async def message_not_modified_handler(*_):
    return True


# Игнорирование ошибки при большом кол-ве запросов
@dp.errors_handler(exception=RetryAfter)
async def exception_handler(*_):
    return True


@dp.errors_handler(exception=MessageToDeleteNotFound)
async def message_not_modified_handler(*_):
    return True


# Показать главное меню
async def show_homepage(call, is_edit=False):
    if is_edit:
        await bot.answer_callback_query(call.id)
        return await call.message.edit_text(MSG_GREET, reply_markup=mainKb)
    await call.answer(MSG_GREET, reply_markup=mainKb)
