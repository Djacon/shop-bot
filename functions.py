import requests

from scripts import *
from keyboards import *

from imports import *


# Класс для работы с выбранными командами
class CMD(StatesGroup):
    calc = State()  # Режим прослушивания входного числа


# Запустить окно c оформлением заказа
@dp.callback_query_handler(lambda c: c.data == 'order')
async def show_order(call):
    await bot.answer_callback_query(call.id)
    await call.message.edit_text(MSG_ERR, reply_markup=backKb)


# Запустить окно с калькулятором стоимости
@dp.callback_query_handler(lambda c: c.data == 'calc')
async def show_calc(call):
    await call.message.delete()
    await bot.answer_callback_query(call.id)

    await CMD.calc.set()
    await call.message.answer(MSG_CALC, reply_markup=exitKb)


# Ссылка на отзывы
@dp.callback_query_handler(lambda c: c.data == 'reviews')
async def show_reviews(call):
    await bot.answer_callback_query(call.id)
    await call.message.edit_text(MSG_ERR, reply_markup=backKb)


# Запустить окно с популярными вопросами-ответами
@dp.callback_query_handler(lambda c: c.data == 'faq')
async def show_faq(call):
    await bot.answer_callback_query(call.id)
    await call.message.edit_text(MSG_FAQ, reply_markup=backKb)


# Запустить окно с отслеживанием посылки
@dp.callback_query_handler(lambda c: c.data == 'search')
async def show_search(call):
    await bot.answer_callback_query(call.id)
    await call.message.edit_text(MSG_SEARCH, reply_markup=backKb)


# Запустить окно по вопросам
@dp.callback_query_handler(lambda c: c.data == 'ask')
async def show_ask(call):
    await bot.answer_callback_query(call.id)
    await call.message.edit_text(ASK_MSG, reply_markup=backKb)


# Запустить окно по вопросам
@dp.callback_query_handler(lambda c: c.data == 'market')
async def show_market(call):
    await bot.answer_callback_query(call.id)
    await call.message.edit_text(MSG_ERR, reply_markup=backKb)


#################################################################

URL = 'https://www.x-rates.com/calculator/?from=CNY'


# Перевести цену с юаней в доллары/рубли
def get_price(amount, to):
    text = str(requests.get(f"{URL}&to={to}&amount={amount}").content)
    text = text[text.find('ccOutputRslt')+14:]
    return text[:text.index('<')]


# Сцена для тестовой модели
@dp.message_handler(state=CMD.calc)
async def playEmotion(message: Message, state):
    amount = message.text

    if amount.lower() in ('выход', '/start'):
        await state.finish()
        await message.answer('Выход в Главное меню', reply_markup=noneKb)
        return await show_homepage(message)

    if len(amount) > 15:
        return await message.answer(f'Слишком большой ввод!')

    if not amount.replace('.', '', 1).isdigit():
        return await message.answer(f'Некорректный ввод - `{amount}`')

    amount = round(float(amount), 2)
    rub = get_price(amount, 'RUB')
    usd = get_price(amount, 'USD')

    msg = (f'Текущий курс на {amount} юаней:\n\nРубль - {rub} ₽\n'
           f'Доллар - {usd} $')
    await message.answer(msg)
