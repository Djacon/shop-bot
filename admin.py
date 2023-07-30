from imports import Message, dp, ADMIN_IDS
from scripts import MSG_ADMIN_ONLY, MSG_ADMIN_CARD, MSG_ORDER_ERR
from database import DB

import os


def isAdmin(message) -> bool:
    return message.from_user.id in ADMIN_IDS


@dp.message_handler(commands=['admin'])
async def users(message: Message):
    if not isAdmin(message):
        return await message.answer(MSG_ADMIN_ONLY)

    info = f'''Админ панель:
/admin - вызов этой панели
/info - узнать инфу о боте
/changebank - изменить номер карты и имя владельца
    '''
    await message.answer(info)


@dp.message_handler(commands=['info'])
async def users(message: Message):
    if not isAdmin(message):
        return await message.answer(MSG_ADMIN_ONLY)

    info = f'''
Информация о боте:
<b>Кол-во юзеров</b>: {len(DB.db)}
<b>Реквизиты карты</b>: {DB.bank['name']}
    '''
    await message.answer(info, parse_mode='HTML')


@dp.message_handler(commands=['changebank'])
async def users(message: Message):
    if not isAdmin(message):
        return await message.answer(MSG_ADMIN_ONLY)

    text = message.text.split()
    if len(text) == 1:
        return await message.answer(MSG_ADMIN_CARD)
    elif len(text) < 8 or not ''.join(text[2:6]).isnumeric():
        return await message.answer(MSG_ORDER_ERR)

    text = ' '.join(text[1:])
    DB.editBank(text)
    await message.answer('Успешно изменено!')  # noqa


@dp.message_handler(commands=['restart'])
async def users(message: Message):
    if not isAdmin(message):
        return await message.answer(MSG_ADMIN_ONLY)

    await message.answer('Начинаю перезагрузку...')
    pid = str(os.getpid())
    with open('restarter.sh', 'w') as restarter:
        restarter.write(f'pkill -9 -f {pid}\ngit pull\npython3 main.py')
    os.system('bash restarter.sh')
