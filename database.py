import json
from uploader import upload_orders, upload_user, get_orders_user_count_info


# Класс для работы с БД пользователей и их заказами
class ShopDB:
    def __init__(self, order_fn, user_fn, bank_fn):
        self.order_fn = order_fn
        self.user_fn = user_fn
        self.bank_fn = bank_fn

        try:
            with open(order_fn, 'r') as f:
                self.db = json.load(f)
        except FileNotFoundError:
            with open(order_fn, 'w') as f:
                f.write('{}')
                self.db = {}

        try:
            with open(user_fn, 'r') as f:
                self.userdb = json.load(f)
        except FileNotFoundError:
            with open(user_fn, 'w') as f:
                f.write('{}')
                self.userdb = {}

        try:
            with open(bank_fn, 'r') as f:
                self.bank = json.load(f)
        except FileNotFoundError:
            with open(bank_fn, 'w') as f:
                name = "Тинькофф 5536 9141 0306 7959 Обада Киспе Марк Антонио"
                self.bank = {'name': name}
                json.dump(self.bank, f)

    def addUser(self, userid):
        self.db[str(userid)] = []
        self._save()

    def getOrders(self, userid):
        userid = str(userid)
        if userid not in self.db:
            return []
        return self.db[userid]

    def addOrder(self, userid, type, img, src, size, cost, deliv):
        userid = str(userid)
        if userid not in self.db:
            self.addUser(userid)

        self.db[userid].append({
            'type': type,
            'photo': img,
            'src': src,
            'size': size,
            'cost': cost,
            'deliv': deliv,
        })

        self._save()

    def clearCart(self, userid):
        self.db[str(userid)] = []
        self._save()

    def uploadCart(self, userid, userinfo):
        order_row, user_row = get_orders_user_count_info()

        userid = str(userid)
        upload_user(userinfo, user_row)
        upload_orders(userinfo[0], self.db[userid], order_row)

        self.db[userid] = []
        self._save()

    def addUserinfo(self, userid, userinfo):
        userid = str(userid)
        self.userdb[userid] = {
            'fullname': userinfo[1],
            'phone': userinfo[2],
            'address': userinfo[3],
        }

        with open(self.user_fn, 'w') as f:
            json.dump(self.userdb, f)

    def editBank(self, name):
        self.bank['name'] = name
        with open(self.bank_fn, 'w') as f:
            json.dump(self.bank, f)

    def _save(self):
        with open(self.order_fn, 'w') as f:
            json.dump(self.db, f)


DB = ShopDB('orders.json', 'users.json', 'bank.json')
