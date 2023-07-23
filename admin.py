from imports import Message, dp


# ADMIN_IDS = [915782472, 535118187]
ADMIN_IDS = [915782472]


def isAdmin(message) -> bool:
    return message.from_user.id in ADMIN_IDS


@dp.message_handler(commands=['info'])
async def users(message: Message):
    if not isAdmin(message):
        msg = 'Извините, команда доступна только администратору!'
        return await message.answer(msg)

    info = ('Информация о боте:\n\nПока недоступно!')
    await message.answer(info)
