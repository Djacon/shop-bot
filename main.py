from aiogram import executor

from imports import *

from keyboards import *
from functions import *
from admin import *


# Стандартная команда /start для начала работы с ботом
@dp.message_handler(commands=['start'])
async def start(message: Message):
    await show_homepage(message)


# Вернуться на главную страницу /start
@dp.callback_query_handler(lambda c: c.data == 'homepage')
async def back_to_homepage(call):
    await call.message.delete()
    await show_homepage(call.message, is_edit=True)


# Сообщение об успешном запуске бота
async def on_startup(_):
    for ADMIN_ID in ADMIN_IDS:
        await bot.send_message(ADMIN_ID, 'Бот перезапущен!')


# Запуск бота
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
