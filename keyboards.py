from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import ReplyKeyboardRemove


def getMainKeyboard():
    order = InlineKeyboardButton('🛍️ Оформить заказ', callback_data='order')
    calc = InlineKeyboardButton('💰 Калькулятор стоимости',
                                callback_data='calc')
    reviews = InlineKeyboardButton('💬 Отзывы о нашей работе',
                                   callback_data='reviews')
    fqa = InlineKeyboardButton('📚 Ответы на популярные вопросы',
                               callback_data='fqa')
    search = InlineKeyboardButton('🔎 Отследить посылку',
                                  callback_data='search')
    ask = InlineKeyboardButton('📞 Задать вопрос',
                               callback_data='ask')
    kb = InlineKeyboardMarkup(resize_keyboard=True, row_width=1)
    return kb.add(order, calc, reviews, fqa, search, ask)


def getBackKeyboard():
    cancel = InlineKeyboardButton('↪️ Вернуться в меню',
                                  callback_data=f'homepage')
    return InlineKeyboardMarkup(resize_keyboard=True).add(cancel)


mainKb = getMainKeyboard()
backKb = getBackKeyboard()

exitKb = KeyboardButton('Выход')
exitKb = ReplyKeyboardMarkup(resize_keyboard=True).add(exitKb)

noneKb = ReplyKeyboardRemove()
