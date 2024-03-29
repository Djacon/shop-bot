import requests
from re import match
from time import time
from math import ceil
from statistics import median

from keyboards import *
from database import *
from imports import *


# Класс для работы с выбранными командами
class CMD(StatesGroup):
    calc_type = State()
    calc_price = State()
    ###
    order_type = State()
    order_photo = State()
    order_src = State()
    order_size = State()
    order_price = State()
    order_deliv = State()
    order_confirm = State()
    ###
    cart_fullname = State()
    cart_phone = State()
    cart_address = State()
    cart_confirm = State()
    cart_receipt = State()


def get_delivery_price(type, size, by_plane=False):
    comm, mass = 0, (120 if by_plane else 55)
    if type == 'winter':
        comm = 1190
        mass *= 2 if size < 42 else 2.3
    elif type == 'summer':
        comm = 1190
        mass *= 1.5 if size < 42 else 1.8
    elif type == 'shorts':
        comm = 1000
    elif type == 'tshirt':
        comm = 890
        mass *= .6
    elif type == 'underw':
        comm = 590
        mass *= .4
    return ceil(comm + cyn2rub(mass))


async def get_filepath(file):
    file = await file.get_file()
    return f"{FILE_PATH}/{file['file_path']}"


async def clear_state_and_show_home(message, state):
    await state.finish()
    msg = await message.answer('Выход в Главное меню', reply_markup=noneKb)
    await msg.delete()
    await show_homepage(message)


async def show_order(call):
    if len(DB.getOrders(call.from_user.id)) > 9:
        return await call.message.answer(MSG_TOO_MANY_ORDERS,
                                         reply_markup=manyOrderKb)

    photo = open('img/guide.jpg', 'rb')
    guide = await call.message.answer_photo(
        photo, caption='<b>Гайд "Как правильно оформить заказ</b>"',
        parse_mode='HTML', reply_markup=noneKb)
    msg_id = guide.message_id

    photo = open('img/instruction.jpg', 'rb')
    await call.message.answer_photo(
        photo, caption=MSG_ORDER,
        parse_mode='HTML',
        reply_markup=getOrderKeyboard(msg_id))


@dp.callback_query_handler(lambda c: c.data == 'order')
async def showOrder(call):
    await call.message.delete()
    await show_order(call)


# Вернуться на главную страницу /start
@dp.callback_query_handler(lambda c: c.data.startswith('order2home'))
async def back_to_homepage(call):
    msg_id = int(call.data.split('?')[1])
    try:
        await bot.delete_message(chat_id=call.from_user.id,
                                 message_id=msg_id)
    except Exception:
        pass

    await call.message.delete()
    await show_homepage(call.message)


@dp.callback_query_handler(lambda c: c.data.startswith('purchase'))
async def show_order_example(call):
    msg_id, cat = call.data.split('?')[1].split('&')
    msg_id = int(msg_id)

    try:
        await bot.delete_message(chat_id=call.from_user.id,
                                 message_id=msg_id)
    except Exception:
        pass

    await call.message.delete()

    if cat == 'access':
        return await call.message.answer(MSG_ORDER_ACS,
                                         reply_markup=backKb)

    state = Dispatcher.get_current().current_state()
    await state.update_data(order_type=cat)

    photo = open('img/example1.jpg', 'rb')
    await CMD.order_photo.set()
    await call.message.answer_photo(
        photo, caption=MSG_ORDER_EX1, parse_mode='HTML',
        reply_markup=exitKb)


@dp.message_handler(state=CMD.order_photo, content_types='any')
async def calculator(message: Message, state):
    if (message.content_type == 'text'
            and message.text.lower() in ('выход', '/start')):
        return await clear_state_and_show_home(message, state)
    elif message.content_type == 'photo':
        async with state.proxy() as data:
            data['order_photo'] = message.photo[-1]

        photo = open('img/example2.jpg', 'rb')
        await CMD.order_src.set()
        return await message.answer_photo(
            photo, caption=MSG_ORDER_EX2, parse_mode='HTML',
            reply_markup=exitKb)

    await message.answer(MSG_ORDER_ERR)


@dp.message_handler(state=CMD.order_src)
async def calculator(message: Message, state):
    text = message.text.lower()
    if text in ('выход', '/start'):
        return await clear_state_and_show_home(message, state)
    elif len(text) < 101 and match(r'https:\/\/dw4\.co\/t\/a\/\w+', text):
        async with state.proxy() as data:
            data['order_src'] = text

        photo = open('img/example3.jpg', 'rb')
        await CMD.order_size.set()
        return await message.answer_photo(
            photo, caption=MSG_ORDER_EX3, parse_mode='HTML',
            reply_markup=exitKb)

    await message.answer(MSG_ORDER_ERR)


@dp.message_handler(state=CMD.order_size)
async def calculator(message: Message, state):
    text = message.text
    if text.lower() in ('выход', '/start'):
        return await clear_state_and_show_home(message, state)

    async with state.proxy() as data:
        if data['order_type'] in ('winter', 'summer'):
            if (match(r'^[3-5]\d(\.5)?$', text) and 33 <= float(text) <= 59):
                text = float(text)
                data['order_size'] = text if text % 1 else int(text)
            else:
                return await message.answer(MSG_ORDER_ERR)
        elif not match(r'^(M|(X{0,3}(S|L)))$', text):
            return await message.answer(MSG_ORDER_ERR)
        else:
            data['order_size'] = text

        photo = open('img/example4.jpg', 'rb')
        await CMD.order_price.set()
        return await message.answer_photo(
            photo, caption=MSG_ORDER_EX4, parse_mode='HTML',
            reply_markup=exitKb)


@dp.message_handler(state=CMD.order_price)
async def calculator(message: Message, state):
    text = message.text.lower()
    if text in ('выход', '/start'):
        return await clear_state_and_show_home(message, state)
    elif not text.isdigit() or text == '0' or int(text) > 1_000_000:
        return await message.answer(MSG_ORDER_ERR)

    msg_ans = await message.answer(MSG_WAIT, reply_markup=noneKb)

    cyn_price = int(text)
    # rub_price = (юань-рубль) + комиссия
    rub_price = cyn2rub(cyn_price + 22)

    async with state.proxy() as data:
        type, size = data['order_type'], data['order_size']

        deliv_price1 = get_delivery_price(type, size, False)
        deliv_price2 = get_delivery_price(type, size, True)

        price1, price2 = rub_price + deliv_price1, rub_price + deliv_price2

    async with state.proxy() as data:
        data['order_price'] = cyn_price

    await CMD.order_deliv.set()
    await msg_ans.delete()
    await message.answer(MSG_ORDER_EX5,
                         reply_markup=getDelivKeyboard(price1, price2))


@dp.callback_query_handler(lambda c: c.data[:4] in ('_one', '_two'),
                           state=CMD.order_deliv)
async def calculator(call, state):
    message = call.message
    text = call.data

    await message.delete()
    msg_ans = await message.answer(MSG_WAIT, reply_markup=noneKb)

    async with state.proxy() as data:
        type = data['order_type']
        cyn_price = data['order_price']
        rub_price = int(text.split('=')[1])
        size, src = data['order_size'], data['order_src']

        data['order_price'] = rub_price
        data['order_deliv'] = 'Авто' if text.startswith('_one') else 'Авиа'

        photo = data['order_photo'].file_id
        caption = f'''
<b>Тип товара</b>: {ITEM_TYPE[type]}
<b>Ссылка на товар</b>: {src}
<b>Размер товара</b>: {size}
<b>Стоимость в ЮАНЯХ</b>: {cyn_price}
<b>Стоимость в РУБЛЯХ</b>: {data['order_price']}

📌В случае, если вы посчитали или оплатили неправильную сумму, а также сделали \
заказ со знаком «≈», то будет произведен возврат средств в период от 3 до 5 \
рабочих дней

❗️Если стоимость ваших товаров превышает 1500¥, то к стоимости товара \
следует прибавить 5% в юанях, это сумма страховки заказа, в случае \
утери/кражи полный возврат средств с нашей стороны
        '''
        await CMD.order_confirm.set()
        await msg_ans.delete()
        await message.answer_photo(
            photo, caption=caption, parse_mode='HTML',
            reply_markup=confirmKb)

        data['order_photo'] = await get_filepath(data['order_photo'])


@dp.callback_query_handler(text_startswith='_', state=CMD.order_confirm)
async def calculator(call, state):
    await call.message.delete()

    message = call.message
    text = call.data
    if text == '_edit':
        await state.finish()
        return await show_order(call)

    userid = call.from_user.id
    async with state.proxy() as data:
        DB.addOrder(userid, data['order_type'], data['order_photo'],
                    data['order_src'], data['order_size'],
                    data['order_price'], data['order_deliv'])

    await state.finish()
    msg = await message.answer('Переход в корзину', reply_markup=noneKb)
    await msg.delete()
    await show_cartpage(message, userid)


######################################################################


# Запустить окно с калькулятором стоимости
@dp.callback_query_handler(lambda c: c.data == 'calc')
async def show_calc(call):
    await call.message.delete()
    await CMD.calc_type.set()

    photo = open('img/instruction.jpg', 'rb')
    await call.message.answer_photo(
        photo, caption=MSG_ORDER,
        parse_mode='HTML',
        reply_markup=getOrderKeyboard(0))


# Ссылка на отзывы
@dp.callback_query_handler(lambda c: c.data == 'reviews')
async def show_reviews(call):
    await call.message.delete()
    await call.message.answer(MSG_ERR, reply_markup=backKb)


# Запустить окно с популярными вопросами-ответами
@dp.callback_query_handler(lambda c: c.data == 'faq')
async def show_faq(call):
    await call.message.delete()
    await call.message.answer(MSG_FAQ, reply_markup=backKb)


# Запустить окно с отслеживанием посылки
@dp.callback_query_handler(lambda c: c.data == 'search')
async def show_search(call):
    await call.message.delete()
    await call.message.answer(MSG_SEARCH, reply_markup=backKb)


# Запустить окно по вопросам
@dp.callback_query_handler(lambda c: c.data == 'ask')
async def show_ask(call):
    await call.message.delete()
    await call.message.answer(ASK_MSG, reply_markup=backKb)


# Запустить окно по вопросам
@dp.callback_query_handler(lambda c: c.data == 'market')
async def show_market(call):
    await call.message.delete()
    await call.message.answer(MSG_ERR, reply_markup=backKb)


# Запустить окно по вопросам
@dp.callback_query_handler(lambda c: c.data == 'cart')
async def show_cart(call):
    await call.message.delete()
    userid = call.from_user.id
    await show_cartpage(call.message, userid)

#################################################################

URL_HUO = 'https://www.huobi.co.il/-/x/otc/v1/data/trade-market?coinId=2&currency=172&tradeType=buy&payMethod=2&acceptOrder=-1&country=&blockType=general&online=1&range=0&onlyTradable=false&isFollowed=false&amount='  # noqa
URL_BIN = 'https://p2p.binance.com/bapi/c2c/v2/friendly/c2c/adv/search'
PAYLOAD = {"fiat": "RUB", "page": 1, "rows": 10, "tradeType": "BUY",
           "asset": "USDT", "countries": [], "proMerchantAds": False,
           "shieldMerchantAds": False, "publisherType": None,
           "payTypes": ["TinkoffNew"], "transAmount": 1000}


# Перевести цену с юаней в рубли
def cyn2rub(amount):
    return ceil(amount * DB.rate['price'])


# Сцена для тестовой модели
@dp.callback_query_handler(state=CMD.calc_type)
async def calculator(call, state):
    await call.message.delete()

    message = call.message
    cat = call.data

    if cat == 'order2home?0':
        return await clear_state_and_show_home(message, state)

    cat = cat[11:]

    if cat == 'access':
        await state.finish()
        return await call.message.answer(MSG_ORDER_ACS, reply_markup=backKb)

    async with state.proxy() as data:
        data['calc_type'] = cat

    photo = open('img/example4.jpg', 'rb')
    await CMD.calc_price.set()
    await message.answer_photo(
        photo, caption=MSG_ORDER_EX4, parse_mode='HTML',
        reply_markup=exitKb)


@dp.message_handler(state=CMD.calc_price)
async def calculator(message: Message, state):
    amount = message.text.lower()

    if amount in ('выход', '/start'):
        return await clear_state_and_show_home(message, state)

    if len(amount) > 6:
        return await message.answer('Слишком большой ввод!')

    if not amount.isdigit() or amount == '0':
        return await message.answer(MSG_ORDER_ERR)

    msg_ans = await message.answer(MSG_WAIT)

    async with state.proxy() as data:
        cat = data['calc_type']

    rub = cyn2rub(int(amount))
    auto = get_delivery_price(cat, 38, False)
    aero = get_delivery_price(cat, 38, True)

    msg = f'''
Итоговая стоимость с доставкой до России составляет:
🚚 Обычная (14-18 дн.): {rub + auto} руб.
✈️ Экспресс (4-8 дн.): {rub + aero} руб.
    '''
    await msg_ans.edit_text(msg)


#################################################################


async def show_cartpage(message, userid):
    orders = DB.getOrders(userid)
    if not orders:
        return await message.answer(MSG_CART_ERR, reply_markup=backKb)

    purch = [f'🛒 Количество вещей в корзине: {len(orders)}']
    total = 0
    for order in orders:
        purch.append(f"Тип товара: {ITEM_TYPE[order['type']]}"
                     f"\nСсылка на товар: {order['src']}"
                     f"\nРазмер: {order['size']}\n"
                     f"Стоимость: {order['cost']} руб")
        total += order['cost']
    purch.append(f'💴 Итоговая стоимость корзины: {total} руб')
    await message.answer('\n\n'.join(purch), reply_markup=cartKb)


@dp.callback_query_handler(lambda c: c.data == 'cart_clear')
async def show_cart(call):
    await call.message.delete()

    userid = call.from_user.id
    DB.clearCart(userid)
    await show_homepage(call.message)


@dp.callback_query_handler(lambda c: c.data == 'checkout')
async def show_cart(call):
    await call.message.delete()

    await CMD.cart_fullname.set()

    msg = await call.message.answer(MSG_WAIT, reply_markup=exitKb)
    await msg.delete()

    userid = str(call.from_user.id)
    if userid in DB.userdb:
        kb = getDefaultOptionKb(DB.userdb[userid]['fullname'], userid)
    else:
        kb = None
    await call.message.answer(MSG_CART_FULLNAME, reply_markup=kb)


@dp.callback_query_handler(text_startswith='_default', state=CMD.cart_fullname)
async def calculator(call, state):
    await call.message.delete()
    userid = call.data.split('_')[2]
    text = DB.userdb[userid]['fullname']

    async with state.proxy() as data:
        data['cart_fullname'] = text
        await CMD.cart_phone.set()

    kb = getDefaultOptionKb(DB.userdb[userid]['phone'], userid)
    return await call.message.answer(MSG_CART_PHONE, reply_markup=kb,
                                     parse_mode='HTML')


@dp.message_handler(state=CMD.cart_fullname)
async def calculator(message: Message, state):
    text = message.text
    if text.lower() in ('выход', '/start'):
        return await clear_state_and_show_home(message, state)
    elif '_' in text:
        return await message.answer(MSG_FORBIDDEN_SYMB)
    elif len(text) < 101 and len(text.split()) > 1:
        async with state.proxy() as data:
            data['cart_fullname'] = text

        await CMD.cart_phone.set()

        userid = str(message.from_user.id)
        if userid in DB.userdb:
            kb = getDefaultOptionKb(DB.userdb[userid]['phone'], userid)
        else:
            kb = None
        return await message.answer(MSG_CART_PHONE, reply_markup=kb,
                                    parse_mode='HTML')

    await message.answer(MSG_ORDER_ERR)


@dp.callback_query_handler(text_startswith='_default', state=CMD.cart_phone)
async def calculator(call, state):
    await call.message.delete()
    userid = call.data.split('_')[2]
    text = DB.userdb[userid]['phone']

    async with state.proxy() as data:
        data['cart_phone'] = text
        await CMD.cart_address.set()

    kb = getDefaultOptionKb(DB.userdb[userid]['address'], userid)
    return await call.message.answer(MSG_CART_ADDR, reply_markup=kb,
                                     parse_mode='HTML')


@dp.message_handler(state=CMD.cart_phone)
async def calculator(message: Message, state):
    text = message.text.lower()
    if text in ('выход', '/start'):
        return await clear_state_and_show_home(message, state)
    elif match(r'^7\d{10}$', text):
        async with state.proxy() as data:
            data['cart_phone'] = text

        await CMD.cart_address.set()

        userid = str(message.from_user.id)
        if userid in DB.userdb:
            kb = getDefaultOptionKb(DB.userdb[userid]['address'], userid)
        else:
            kb = None
        return await message.answer(MSG_CART_ADDR, reply_markup=kb,
                                    parse_mode='HTML')

    await message.answer(MSG_ORDER_ERR)


@dp.callback_query_handler(text_startswith='_default', state=CMD.cart_address)
async def calculator(call, state):
    await call.message.delete()
    userid = call.data.split('_')[2]
    text = DB.userdb[userid]['address']

    async with state.proxy() as data:
        data['cart_address'] = text
        await CMD.cart_phone.set()

        caption = f'''
👤 Ваши данные для получения посылки

<b>ФИО</b>: {data['cart_fullname']}
<b>Номер телефона</b>: {data['cart_phone']}
<b>Курьерская служба</b>: СДЭК
<b>Адрес доставки</b>: {text}

❕ Внимание! Проверяйте данные для получения внимательно, на них будет \
отправлена посылка по России.

🚚 Доставка по России в оплату ВКЛЮЧЕНА!
        '''

        await CMD.cart_confirm.set()
        return await call.message.answer(caption, parse_mode='HTML',
                                         reply_markup=confirmKb)


@dp.message_handler(state=CMD.cart_address)
async def calculator(message: Message, state):
    text = message.text
    if text.lower() in ('выход', '/start'):
        return await clear_state_and_show_home(message, state)
    elif '_' in text:
        return await message.answer(MSG_FORBIDDEN_SYMB)
    elif len(text) < 201:
        async with state.proxy() as data:
            data['cart_address'] = text

        caption = f'''
👤 Ваши данные для получения посылки

<b>ФИО</b>: {data['cart_fullname']}
<b>Номер телефона</b>: {data['cart_phone']}
<b>Курьерская служба</b>: СДЭК
<b>Адрес доставки</b>: {text}

❕ Внимание! Проверяйте данные для получения внимательно, на них будет \
отправлена посылка по России.

🚚 Доставка по России в оплату ВКЛЮЧЕНА!
        '''

        await CMD.cart_confirm.set()
        return await message.answer(caption, parse_mode='HTML',
                                    reply_markup=confirmKb)

    await message.answer(MSG_ORDER_ERR)


@dp.callback_query_handler(text_startswith='_', state=CMD.cart_confirm)
async def calculator(call, state):
    await call.message.delete()

    text = call.data
    message = call.message

    if text == '_edit':
        userid = call.from_user.id
        await state.finish()
        msg = await message.answer('Переход в корзину', reply_markup=noneKb)
        await msg.delete()
        return await show_cartpage(message, userid)
    elif text == '_yes':
        await CMD.cart_receipt.set()
        await message.answer(f'''
Произведите оплату на банк карты:
«<b>{DB.bank['name']}</b>»
И отправьте чек с оплатой боту:
            ''', reply_markup=exitKb, parse_mode='HTML')


@dp.message_handler(state=CMD.cart_receipt, content_types='any')
async def calculator(message: Message, state):
    text = message.text
    userid = message.from_user.id
    username = message.from_user.username or userid

    if (message.content_type == 'text'
            and text.lower() in ('выход', '/start')):
        return await clear_state_and_show_home(message, state)
    elif message.content_type != 'photo':
        return await message.answer(MSG_ORDER_ERR)

    msg_ans = await message.answer(MSG_WAIT, reply_markup=noneKb)

    try:
        count_purchase = len(DB.getOrders(userid))
        async with state.proxy() as data:
            photo_src = await get_filepath(message.photo[-1])
            userinfo = (f't.me/{username}', data['cart_fullname'],
                        data['cart_phone'], data['cart_address'],
                        photo_src)
            DB.addUserinfo(userid, userinfo)
            DB.uploadCart(userid, userinfo)
            caption = f'''
Информация о новом покупателе:

<b>Юзер</b>: @{username}
<b>ФИО</b>: {userinfo[1]}
<b>Номер телефона</b>: {userinfo[2]}
<b>Адрес доставки</b>: {userinfo[3]}
<b>Кол-во товаров</b> {count_purchase}'''

        for ADMIN_ID in ADMIN_IDS:
            await bot.send_message(ADMIN_ID, caption, parse_mode='HTML')

        await state.finish()
        await msg_ans.delete()
        await message.answer(MSG_ORDER_SUCCESS, reply_markup=backKb)

    except Exception as e:
        await state.finish()
        await bot.send_message(915782472, f'!!!! Error: {e}')
        return await msg_ans.edit_text(MSG_API_ERR, reply_markup=backKb)
