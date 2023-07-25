from imports import Message, dp, ADMIN_IDS
from scripts import MSG_ADMIN_ONLY

import os


def isAdmin(message) -> bool:
    return message.from_user.id in ADMIN_IDS


@dp.message_handler(commands=['info'])
async def users(message: Message):
    if not isAdmin(message):
        return await message.answer(MSG_ADMIN_ONLY)

    info = ('Информация о боте:\n\nПока недоступно!')
    await message.answer(info)


@dp.message_handler(commands=['restart'])
async def users(message: Message):
    if not isAdmin(message):
        return await message.answer(MSG_ADMIN_ONLY)

    pid = str(os.getpid())
    with open('restarter.sh', 'w') as restarter:
        restarter.write(f'kill {pid}\npython3 main.py')
    os.system('restarter.sh')
