MSG_GREET = '''
Добро пожаловать!
Вас приветствует бот команды OQ Store. 🤙

Мы осуществляем выкуп товаров с площадки - POIZON!

❗️Все операции (расчет, оплата) производятся исключительно в боте
'''

MSG_ADMIN_ONLY = 'Извините, команда доступна только администратору!'

MSG_ADMIN_CARD = '''
Введите название банка, номер карты и имя владельца в формате:\n
/changebank Тинькофф XXXX XXXX XXXX XXXX Антон Павлов
'''

ASK_MSG = '''
По всем вопросам насчёт заказа обращайтесь к аккаунту поддержки ❕


   ━ ━ ━ ━ ━
┃@Slarck777 ┃
   ━ ━ ━ ━ ━

❗️ВАЖНО❗️
Поддержка НЕ ПРИНИМАЕТ ОПЛАТУ, только помощь с заказом.
Например:
 1. Дополнительная упаковка для хрупкого заказа
 2. Оптовый заказ
 3. Проблемы с заказом и тому подобное.

Поддержка НЕ ПИШЕТ чтобы вы перевели деньги за заказ, ОПЛАТА ТОЛЬКО В БОТЕ❗️

❗️БУДЬТЕ ВНИМАТЕЛЬНЫ❗️
'''

MSG_SEARCH = '''
🔍Статус заказа(ов):

⚠ Данные обновляются с задержкой, если Ваш статус не обновился не стоит \
переживать все обновляется в ручном режиме.

*Paid - заказ принят в обработку;
*Ordered - заказ оплачен в приложении POIZON и ожидает поступления на склад \
в Китае;
*Отправлено на склад в РФ (20 марта) - означает что Ваш товар был отправлен и \
уже находится в пути примерно через 25 дней от 20 марта товар будет на складе \
в России.
'''

MSG_FAQ = '''
🚚 Сколько времени занимает доставка товара?

🔻Доставка со склада в Китае до Москвы занимает в большинстве случаев (98%) \
~14-18 дней (при условии, что товар доставляется по Китаю до 2-3х дней, все \
что свыше - добавляем к общему сроку доставки)

🔻После оплаты заказа в боте он попадает в нашу базу данных, выкупается в \
течении 4-8 часов, далее он находится в обработке  около 12 часов, в \
последствии продавец отправляет его в распределительный центр Poizon (где \
заказ проверяется вживую на оригинальность, полный комплект, брак)

🔻Доставка по России и СНГ в эти диапазоны не входит и зависит от удаленности \
Вашего региона от г. Москва, в среднем практически во все регионы доставка 3-5\
 дней (CDEK)

🚚 Сколько стоит доставка по России? (CDEK)

🔻Мы работаем по договору на юр. лицо с компанией CDEK, тем самым мы \
предлагаем самые низкие тарифы для логистики

🔹Доставка по Москве 1-2 дня, ~150-200₽.
🔹Доставка по России / СНГ 3-5 дней, ~300-400₽.

‼️ Стоит также уточнить, что стоимость указана без страховки, в случае, если \
страховка нужна, то просьба уведомлять об этом.
В случае утери/кражи CDEK полностью компенсируют стоимость заказа нам на \
расчетный счет, после мы уже компенсируем всю сумму Вам
'''


MSG_ORDER = '''
Здесь Вы можете сделать расчет стоимости интересующих товаров с доставкой 🚚 / \
✈️ до России!

Товары с ≈ НЕ ВЫКУПАЕМ
Цены указывать только в ¥ (юани)

Примечания:
❗️ В случае, если Вы оплатили неверную сумму и хотите вернуть денежные \
средства, либо доплатить нужную сумму для выкупа заказа, напишите нашему \
модератору @Slarck777
❗️ Возврат денежных средств производится в течении 2-3х рабочих дней
❗️ Если стоимость Ваших товаров превышает 1500¥, то к стоимости товара \
следует прибавить 5% в юанях, это сумма страховки заказа, в случае \
утери/кражи полный возврат средств с нашей стороны
'''

MSG_ORDER_EX1 = '''
Вставьте изображение товара, так же, как показано на примере:
'''

MSG_ORDER_EX2 = '''
🔗 Укажите ссылку на товар в необходимом формате: \
https://dw4.co/t/A/1KUOPsbt
'''

MSG_ORDER_EX3 = '''
Предоставьте информацию о размере товара (соответственно, учитывая размер \
обуви и одежды).
Например: (38/42/43), (S/M/XL)
'''

MSG_ORDER_EX4 = '''
Введите стоимость выбранной вещи в <b>ЮАНЯХ</b> (¥) \
(только зачёркнутая цена, например <s>¥889</s>)
'''

MSG_ORDER_EX5 = 'Выберите вариант доставки:'

MSG_ORDER_ERR = 'Ошибка: Некорректный ввод!'

MSG_ORDER_ACS = '''
Для того чтобы преобрести следующий товар, необходимо обратиться \
к администрации 👉 @Slarck777 👈
'''

MSG_CART_ERR = 'Похоже у вас еще нет заказов ¯\\_(ツ)_/¯'

MSG_CART_FULLNAME = '''
👶 Пожалуйста, введите ФИО полностью как в паспорте \
(например Иванов Иван Иванович):

*на эти данные будет отправлена Ваша посылка
'''

MSG_CART_PHONE = '''
📱 Пожалуйста, введите номер телефона в формате 79998887766:

*этот номер будет использован для связи с получателем
'''

MSG_CART_ADDR = '''
🏚 Пожалуйста, введите адрес пунтка выдачи СДЭК в формате (Страна, Область, \
Город, Улица, Номер дома):

*например: Россия, Московская область, Москва, улица Пролетарская 78.

**Доставка по России пока что осуществляется только транспортной компанией \
СДЭК.
'''

MSG_CALC = '💴 Введите стоимость товара в юанях, например 100:'

MSG_ERR = 'Временно недоступно ¯\\_(ツ)_/¯'

MSG_WAIT = 'Пожалуйста подождите...'

MSG_API_ERR = '''
Ведутся технические работы на сервере :(\

Приносим извинения за неудобства!
'''

MSG_FORBIDDEN_SYMB = 'Запрещенный символ: `_`'

MSG_ORDER_SUCCESS = '''
Ваш заказ оформлен!
'''
