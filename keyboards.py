from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import ReplyKeyboardRemove


# def getModelKeyboard(i: int, isAdmin: bool):
#     sub = InlineKeyboardButton('✍ Воспользоваться нейросетью',
#                                callback_data=f'open-{i}')
#     back = InlineKeyboardButton('⬅ Назад', callback_data='models')
#     homepage = InlineKeyboardButton('🏠 На главную', callback_data='homepage')
#     models_keyboard = InlineKeyboardMarkup(resize_keyboard=True)
#     if not isAdmin:
#         return models_keyboard.add(sub).row(back, homepage)
#     edit = InlineKeyboardButton('Отредактировать',
#                                 callback_data=f'editModel-{i}')
#     return models_keyboard.add(sub).row(edit).row(back, homepage)


def getMainKeyboard():
    order = InlineKeyboardButton('🛍️ Оформить заказ', callback_data='order')
    calc = InlineKeyboardButton('💰 Калькулятор стоимости',
                                callback_data='calc')
    return InlineKeyboardMarkup(resize_keyboard=True, row_width=1).add(order,
                                                                       calc)


def getCancelKeyboard(i: int = 0):
    cancel = InlineKeyboardButton('Отмена', callback_data=f'cancel-{i}')
    return InlineKeyboardMarkup(resize_keyboard=True).add(cancel)


mainKb = getMainKeyboard()

cancelKb = KeyboardButton('Отмена')
cancelKb = ReplyKeyboardMarkup(resize_keyboard=True).add(cancelKb)

exitKb = KeyboardButton('Выход')
exitKb = ReplyKeyboardMarkup(resize_keyboard=True).add(exitKb)

noneKb = ReplyKeyboardRemove()
