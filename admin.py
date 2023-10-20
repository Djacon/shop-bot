from imports import Message, dp, ADMIN_IDS
from scripts import MSG_ADMIN_ONLY, MSG_ADMIN_RATE, MSG_ADMIN_CARD, MSG_ORDER_ERR  # noqa
from database import DB

import os
import random


def isAdmin(message) -> bool:
    return message.from_user.id in ADMIN_IDS


def isNumber(s):
    return s.replace('.', '', 1).isdigit()


@dp.message_handler(commands=['admin'])
async def users(message: Message):
    if not isAdmin(message):
        return await message.answer(MSG_ADMIN_ONLY)

    info = f'''Админ панель:
/admin - вызов этой панели
/info - узнать инфу о боте
/changerate - изменить текущий обменный курс
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
<b>Текущий курс (CYN/RUB)</b>: {DB.rate['price']}
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
    await message.answer('Успешно изменено!')


@dp.message_handler(commands=['changerate'])
async def users(message: Message):
    if not isAdmin(message):
        return await message.answer(MSG_ADMIN_ONLY)

    text = message.text.split()
    if len(text) == 1:
        return await message.answer(MSG_ADMIN_RATE)
    elif len(text) != 2 or not isNumber(text[1]):
        # return await message.answer(MSG_ORDER_ERR)
        errs = ['Чел, нужно сделать лабу по физике 3.05, 3.06',
                '(PS: Марк ты реально Даун, это не ошибка, ты просто тупишь)',
                'MarkDownError: попробуй еще раз, у тебя получится',
                'У тебя с матаном такая же ситуация?',
                'Попробуй написать количество долгов, может прокатит']
        return await message.answer(errs[random.randint(0, len(errs)-1)])

    DB.editRate(float(text[1]))
    await message.answer('Успешно изменено!')


@dp.message_handler(commands=['restart'])
async def users(message: Message):
    if not isAdmin(message):
        return await message.answer(MSG_ADMIN_ONLY)

    await message.answer('Начинаю перезагрузку...')
    pid = str(os.getpid())
    with open('restarter.sh', 'w') as restarter:
        restarter.write(f'pkill -9 -f {pid}\ngit pull\npython3 main.py')
    os.system('bash restarter.sh')
