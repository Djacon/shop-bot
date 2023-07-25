from imports import Message, dp, ADMIN_IDS
from scripts import MSG_ADMIN_ONLY
from database import DB

import os


def isAdmin(message) -> bool:
    return message.from_user.id in ADMIN_IDS


@dp.message_handler(commands=['info'])
async def users(message: Message):
    if not isAdmin(message):
        return await message.answer(MSG_ADMIN_ONLY)

    info = f'Информация о боте:\nКол-во юзеров: {len(DB.db)}'
    await message.answer(info)


@dp.message_handler(commands=['restart'])
async def users(message: Message):
    if not isAdmin(message):
        return await message.answer(MSG_ADMIN_ONLY)

    pid = str(os.getpid())
    with open('restarter.sh', 'w') as restarter:
        restarter.write(f'kill {pid}\ngit pull\npython3 main.py')
    os.system('restarter.sh')
