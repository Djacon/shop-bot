from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import ReplyKeyboardRemove


def getMainKeyboard():
    calc = InlineKeyboardButton('💸 Калькулятор стоимости',
                                callback_data='calc')
    order = InlineKeyboardButton('🛒 Оформить заказ', callback_data='order')
    search = InlineKeyboardButton('🔎 Отследить посылку',
                                  callback_data='search')
    reviews = InlineKeyboardButton('📋 Отзывы о нашей работе ',
                                   callback_data='reviews')
    mark = InlineKeyboardButton('🛍️ Market OQ (IN STOCK)',
                                callback_data='market')
    ask = InlineKeyboardButton('📞 Связь с нами', callback_data='ask')
    faq = InlineKeyboardButton('❔ FAQ', callback_data='faq')

    kb = InlineKeyboardMarkup(resize_keyboard=True, row_width=1)
    return kb.add(calc, order, search, reviews, mark, ask, faq)


def getBackKeyboard():
    cancel = InlineKeyboardButton('↪️ Вернуться в меню',
                                  callback_data=f'homepage')
    return InlineKeyboardMarkup(resize_keyboard=True).add(cancel)


mainKb = getMainKeyboard()
backKb = getBackKeyboard()

exitKb = KeyboardButton('Выход')
exitKb = ReplyKeyboardMarkup(resize_keyboard=True).add(exitKb)

noneKb = ReplyKeyboardRemove()
