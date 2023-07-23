import json
from uploader import upload_orders, upload_user, get_orders_user_count_info


# Класс для работы с БД пользователей и их заказами
class ShopDB:
    def __init__(self, filename):
        self.filename = filename
        try:
            with open(filename, 'r') as f:
                self.db = json.load(f)
        except FileNotFoundError:
            with open(filename, 'w') as f:
                f.write('{}')
                self.db = {}

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
        upload_orders(userid, self.db[userid], order_row)

        self.db[userid] = []
        self._save()

    def _save(self):
        with open(self.filename, 'w') as f:
            json.dump(self.db, f)


DB = ShopDB('orders.json')
