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


def getOrderKeyboard(msg_id):
    search = InlineKeyboardButton('🔍 Где найти цену в юанях?',
                                  callback_data='order2search')
    winter = InlineKeyboardButton('🥾 Зимняя обувь', callback_data='winter')
    summer = InlineKeyboardButton('👟 Летняя обувь', callback_data='summer')

    tshirt = InlineKeyboardButton('👕 Футболки / Шорты / Худи',
                                  callback_data='tshirt')
    shorts = InlineKeyboardButton('👖 Джинсы / Штаны / Шорты',
                                  callback_data='shorts')
    access = InlineKeyboardButton('👜 Сумки / Аксессуары / Парфюмы',
                                  callback_data='access')
    underw = InlineKeyboardButton('🧦 Нижнее белье', callback_data='underw')
    cancel = InlineKeyboardButton('↪️ Вернуться в меню',
                                  callback_data=f'order2home?{msg_id}')
    kb = InlineKeyboardMarkup(resize_keyboard=True, row_width=1)
    return kb.row(search).row(winter, summer).add(tshirt, shorts, access,
                                                  underw, cancel)


def getBackKeyboard():
    cancel = InlineKeyboardButton('↪️ Вернуться в меню',
                                  callback_data='homepage')
    return InlineKeyboardMarkup(resize_keyboard=True).add(cancel)


mainKb = getMainKeyboard()
backKb = getBackKeyboard()

exitKb = KeyboardButton('Выход')
exitKb = ReplyKeyboardMarkup(resize_keyboard=True).add(exitKb)

noneKb = ReplyKeyboardRemove()
