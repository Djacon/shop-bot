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
    await show_homepage(call, is_edit=True)


# Вернуться на главную страницу /start
@dp.callback_query_handler(lambda c: c.data.startswith('order2home'))
async def back_to_homepage(call):
    msg_id = int(call.data.split('?')[1])
    await bot.delete_message(chat_id=call.from_user.id,
                             message_id=msg_id)
    await call.message.delete()
    await call.message.answer(MSG_GREET, reply_markup=mainKb)


# Сообщение об успешном запуске бота
async def on_startup(_):
    for ADMIN_ID in ADMIN_IDS:
        await bot.send_message(ADMIN_ID, 'Бот перезапущен!')


# Запуск бота
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
