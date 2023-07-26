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
    calc = State()
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


async def show_order(message):
    photo = open('img/guide.jpg', 'rb')
    guide = await message.answer_photo(
        photo, caption='<b>Гайд "Как правильно оформить заказ</b>"',
        parse_mode='HTML', reply_markup=noneKb)
    msg_id = guide.message_id

    photo = open('img/instruction.jpg', 'rb')
    await message.answer_photo(
        photo, caption=MSG_ORDER,
        parse_mode='HTML',
        reply_markup=getOrderKeyboard(msg_id))


@dp.callback_query_handler(lambda c: c.data == 'order')
async def showOrder(call):
    await call.message.delete()
    await show_order(call.message)


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
    elif len(text) < 101 and text.startswith('https://dw4.co/t/a/'):
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
    rub_price = cyn2rub(cyn_price) + ceil(2.5 * TMP[2]) + 20

    async with state.proxy() as data:
        data['order_price'] = (cyn_price, rub_price)

    await CMD.order_deliv.set()
    await msg_ans.delete()
    await message.answer(MSG_ORDER_EX5, reply_markup=delivKb)


@dp.callback_query_handler(text_startswith='_', state=CMD.order_deliv)
async def calculator(call, state):
    message = call.message
    text = call.data

    await message.delete()
    msg_ans = await message.answer(MSG_WAIT, reply_markup=noneKb)

    async with state.proxy() as data:
        type = data['order_type']
        cyn_price, rub_price = data['order_price']
        size, src = data['order_size'], data['order_src']
        deliv_price = get_delivery_price(type, size, text == '2')

        data['order_price'] = rub_price + deliv_price
        data['order_deliv'] = 'Авто' if text == '_one' else 'Авиа'

        photo = data['order_photo'].file_id
        caption = f'''
<b>Тип товара</b>: {ITEM_TYPE[type]}
<b>Ссылка на товар</b>: {src}
<b>Размер товара</b>: {size}
<b>Стоимость в ЮАНЯХ</b>: {cyn_price}
<b>Стоимость в РУБЛЯХ</b>: {data['order_price']}

❕ <b>Внимание</b>, стоимость указана с расчетом веса товара, так же \
внимательно проверяйте товар, удалить отдельно один из списка потом не \
получится.

⚠ Если Вы по ошибке оплатили неверную сумму, и хотите вернуть свои деньги \
обратно, заявка на возврат средств обрабатывается в течении 7 рабочих дней. \
Будьте внимательны! ⚠

⛔ Если Ваш товар стоит больше 2000 юаней, то к стоимости товара следует \
прибавлять 10% в юанях. 10% взымается за страхование товара, в случае утери \
или кражи возврат 100% стоимости товара. ⛔

🚚 Доставка по России <b>включена</b> в стоимость! Отправки идут из Москвы.
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
        return await show_order(message)

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
    await CMD.calc.set()
    await call.message.answer(MSG_CALC, reply_markup=exitKb)


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

# (Time | USDT2CNY | USDT2RUB)
TMP = (0, 7.11, 91.69)


def usdt2cny(amount):
    res = json.loads(requests.get(f'{URL_HUO}{amount}&currPage=1').content)
    data = [float(data['price']) for data in res['data']]

    res = json.loads(requests.get(f'{URL_HUO}{amount}&currPage=2').content)
    data.extend([float(data['price']) for data in res['data']])
    return round(median(data), 2)


def usdt2rub():
    res = json.loads(requests.post(URL_BIN, json=PAYLOAD).content)
    data = [float(data['adv']['price']) for data in res['data']]
    return round(median(data), 2)


# Перевести цену с юаней в рубли
def cyn2rub(amount):
    global TMP

    t = int(time())
    if t - TMP[0] > 59:
        usd = usdt2cny(max(amount, 100))
        rub = usdt2rub()
        TMP = (t, usd, rub)
    return ceil((amount / TMP[1]) * TMP[2])


# Сцена для тестовой модели
@dp.message_handler(state=CMD.calc)
async def calculator(message: Message, state):
    amount = message.text

    if amount.lower() in ('выход', '/start'):
        return await clear_state_and_show_home(message, state)

    if len(amount) > 6:
        return await message.answer('Слишком большой ввод!')

    if not amount.isdigit() or amount == '0':
        return await message.answer(f'Некорректный ввод: `{amount}`')

    msg_ans = await message.answer(MSG_WAIT)

    rub = cyn2rub(int(amount))

    msg = f'💰 Итоговая стоимость {rub} руб с доставкой до России'
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
    await call.message.answer(MSG_CART_FULLNAME, reply_markup=exitKb)


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
        return await message.answer(MSG_CART_PHONE, parse_mode='HTML')

    await message.answer(MSG_ORDER_ERR)


@dp.message_handler(state=CMD.cart_phone)
async def calculator(message: Message, state):
    text = message.text.lower()
    if text in ('выход', '/start'):
        return await clear_state_and_show_home(message, state)
    elif match(r'^7\d{10}$', text):
        async with state.proxy() as data:
            data['cart_phone'] = text

        await CMD.cart_address.set()
        return await message.answer(MSG_CART_ADDR, parse_mode='HTML')

    await message.answer(MSG_ORDER_ERR)


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
    userid = call.from_user.id
    username = call.from_user.username or userid

    if text == '_edit':
        await state.finish()
        msg = await message.answer('Переход в корзину', reply_markup=noneKb)
        await msg.delete()
        return await show_cartpage(message, userid)

    msg_ans = await message.answer(MSG_WAIT, reply_markup=noneKb)

    try:
        count_purchase = len(DB.getOrders(userid))
        async with state.proxy() as data:
            userinfo = (f't.me/{username}', data['cart_fullname'],
                        data['cart_phone'], data['cart_address'])
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
