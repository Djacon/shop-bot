from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import ReplyKeyboardRemove

from math import ceil


ITEM_TYPE = {
    'winter': '🥾 Зимняя обувь',
    'summer': '👟 Летняя обувь',
    'tshirt': '👕 Футболки / Штаны / Шорты',
    'shorts': '👖 Джинсы / Худи / Куртки',
    'access': '👜 Сумки / Аксессуары / Парфюмы',
    'underw': '🧦 Нижнее белье',
}


def getMainKeyboard():
    calc = InlineKeyboardButton('💸 Калькулятор стоимости',
                                callback_data='calc')
    order = InlineKeyboardButton('🛍️ Оформить заказ', callback_data='order')
    search = InlineKeyboardButton('🔎 Отследить посылку',
                                  callback_data='search')
    reviews = InlineKeyboardButton('📋 Отзывы о нашей работе ',
                                   callback_data='reviews')
    # mark = InlineKeyboardButton('🛍️ Market OQ (IN STOCK)',
    #                             callback_data='market')
    ask = InlineKeyboardButton('📞 Связь с нами', callback_data='ask')
    faq = InlineKeyboardButton('❔ FAQ', callback_data='faq')
    cart = InlineKeyboardButton('🛒 Мои заказы', callback_data='cart')

    kb = InlineKeyboardMarkup(resize_keyboard=True, row_width=1)
    # return kb.add(order, calc, search, reviews, mark, ask, faq, cart)
    return kb.add(order, calc, search, reviews, ask, faq, cart)


def getOrderKeyboard(msg_id):
    prchs = f'purchase?{msg_id}&'
    btns = []
    for type in ITEM_TYPE:
        btns.append(InlineKeyboardButton(ITEM_TYPE[type],
                                         callback_data=f'{prchs}{type}'))
    search = InlineKeyboardButton('🔍 Где найти цену в юанях?',
                                  callback_data='order2search')
    cancel = InlineKeyboardButton('↪️ Вернуться в меню',
                                  callback_data=f'order2home?{msg_id}')
    kb = InlineKeyboardMarkup(resize_keyboard=True, row_width=1)
    return kb.row(search).row(btns[0], btns[1]).add(*btns[2:], cancel)


def getConfirmOrderKeyboard():
    edit = InlineKeyboardButton('✏️ Изменить', callback_data='_edit')
    yes = InlineKeyboardButton('✅ Верно', callback_data='_yes')
    return InlineKeyboardMarkup(resize_keyboard=True).row(edit).row(yes)


def getBackKeyboard():
    cancel = InlineKeyboardButton('↪️ Вернуться в меню',
                                  callback_data='homepage')
    return InlineKeyboardMarkup(resize_keyboard=True).add(cancel)


def getCartKeyboard():
    clear = InlineKeyboardButton('♻️ Очистить корзину',
                                 callback_data='cart_clear')
    add = InlineKeyboardButton('➕ Добавить товар',
                               callback_data='order')
    checkout = InlineKeyboardButton('📦 Оформить заказ',
                                    callback_data='checkout')
    cancel = InlineKeyboardButton('↪️ Вернуться в меню',
                                  callback_data='homepage')
    kb = InlineKeyboardMarkup(resize_keyboard=True, row_width=1)
    return kb.add(clear, add, checkout, cancel)


def getDelivKeyboard(p1, p2):
    one = InlineKeyboardButton(f'До 15 дней | {p1}₽',
                               callback_data=f'_one={p1}')
    two = InlineKeyboardButton(f'До 7 дней | {p2}₽',
                               callback_data=f'_two={p2}')
    kb = InlineKeyboardMarkup(resize_keyboard=True, row_width=1)
    return kb.add(one, two)


def getDefaultOptionKb(name, userid):
    one = InlineKeyboardButton(f'По умолчанию: [{name}]',
                               callback_data=f'_default_{userid}')
    return InlineKeyboardMarkup(resize_keyboard=True, row_width=1).add(one)


mainKb = getMainKeyboard()
backKb = getBackKeyboard()

cartKb = getCartKeyboard()
confirmKb = getConfirmOrderKeyboard()

exitKb = KeyboardButton('Выход')
exitKb = ReplyKeyboardMarkup(resize_keyboard=True).add(exitKb)

noneKb = ReplyKeyboardRemove()
