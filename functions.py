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
@dp.callback_query_handler(lambda c: c.data == 'fqa')
async def show_fqa(call):
    await bot.answer_callback_query(call.id)
    await call.message.edit_text(MSG_ERR, reply_markup=backKb)


# Запустить окно с отслеживанием посылки
@dp.callback_query_handler(lambda c: c.data == 'search')
async def show_fqa(call):
    await bot.answer_callback_query(call.id)
    await call.message.edit_text(MSG_ERR, reply_markup=backKb)


# Запустить окно по вопросам
@dp.callback_query_handler(lambda c: c.data == 'ask')
async def show_ask(call):
    await bot.answer_callback_query(call.id)
    await call.message.edit_text(ASK_MSG, reply_markup=backKb)


#################################################################

# Получить текущую стоимость на бирже
def get_factor():
    return 11.7


# Сцена для тестовой модели
@dp.message_handler(state=CMD.calc)
async def playEmotion(message: Message, state):
    text = message.text

    if text.lower() in ('выход', '/start'):
        await state.finish()
        await message.answer('Выход в Главное меню', reply_markup=noneKb)
        return await show_homepage(message)

    if len(text) > 15:
        return await message.answer(f'Слишком большой ввод!')

    if not text.replace('.', '', 1).isdigit():
        return await message.answer(f'Некорректный ввод - `{text}`')

    factor = get_factor()
    text = float(text)

    msg = f'Текущий курс - 100:{factor}\n\n{text:.2f} ₽ -> {text * factor:.2f} $'
    await message.answer(msg)
