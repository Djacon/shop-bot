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

MSG_ADMIN_RATE = '''
Введите новый курс в формате:\n
/changerate 14.3
'''

ASK_MSG = '''
По всем вопросам насчёт заказа обращайтесь к аккаунту поддержки ❕

   ━ ━ ━ ━ ━
┃@Slarck777┃
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
❗️В случае, если Вы оплатили неверную сумму и хотите вернуть денежные \
средства, либо доплатить нужную сумму для выкупа заказа, напишите нашему \
модератору @Slarck777
❗️Возврат денежных средств производится в течении 2-3х рабочих дней
❗️Если стоимость Ваших товаров превышает 1500¥, то к стоимости товара \
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
📍Предоставьте, пожалуйста, информацию о размере товара (для обуви размер \
указывается европейский - EU)

- Например:
Размер 👟: 38 / 42 / 43
Размер 👕: S / М / L
'''

MSG_ORDER_EX4 = '''
📍Укажите, пожалуйста, стоимость выбранной позиции - в <b>ЮАНЯХ</b> (¥)
▫️(для ввода стоимости указывать только цену по зачеркнутому значению, \
например: <s>¥899</s>)
'''

MSG_ORDER_EX5 = 'Выберите вариант доставки:'

MSG_ORDER_ERR = 'Ошибка: Некорректный ввод!'

MSG_ORDER_ACS = '''
Для того чтобы преобрести следующий товар, необходимо обратиться \
к администрации 👉 @Slarck777 👈
'''

MSG_CART_ERR = 'Похоже у вас еще нет заказов ¯\\_(ツ)_/¯'

MSG_CART_FULLNAME = '''
👤 Укажите, пожалуйста, полное ФИО в соответствии с паспортом.
Например: Иванов Иван Иванович

📍Указанные Вами данные будут использованы для оформления накладной при \
отправке заказа в ТК.
Будьте внимательны и тщательно проверяйте информацию перед отправкой!
'''

MSG_CART_PHONE = '''
📱Введите, пожалуйста, Ваш контактный номер телефона для оформления заказа.
Например: 79998887766

📍Указанные Вами данные будут использованы для оформления накладной при \
отправке заказа в ТК.
Будьте внимательны и тщательно проверяйте информацию перед отправкой!
'''

MSG_CART_ADDR = '''
🏠Укажите, пожалуйста, адрес удобного / ближайшего для Вас ПВЗ СДЭК.
Например: Россия, Московская область, г. Москва, ул. Пролетарская д. 78.

📍Указанные Вами данные будут использованы для оформления накладной при \
отправке заказа в ТК.
Будьте внимательны и тщательно проверяйте информацию перед отправкой!

❗️Доставка по России временно осуществляется только через транспортную \
компанию - СДЭК, в случае, если нет возможности получить заказ данной ТК \
убедительная просьба написать в тех. поддержку.
'''

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

MSG_TOO_MANY_ORDERS = '''
❗️Извините, но вы не можете заказать больше 10 товаров за раз.
Пожалуйста, оплатите предыдущие товары, либо очистите корзину.
'''
