from aiogram.types import Message
from aiogram import Bot, Dispatcher
from aiogram.utils.exceptions import MessageNotModified, RetryAfter
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup

from os import environ

from keyboards import mainKb

# Токен для получения доступа к боту
TOKEN = environ['TOKEN']

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


# Показать главное меню
async def show_homepage(call, is_edit=False):
    user = call.from_user.first_name
    greet = (f'Приветствую вас, {user}!\n\n(здесь будет расположено адекватное'
             ' описание):')
    if is_edit:
        await bot.answer_callback_query(call.id)
        return await call.message.edit_text(greet, reply_markup=mainKb)
    await call.answer(greet, reply_markup=mainKb)
