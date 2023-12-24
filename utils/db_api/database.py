import sqlite3
from datetime import datetime


class Database:
    def __init__(self, db_path: str) -> None:
        self.conn = sqlite3.connect(db_path)

    @property
    def connect(self):
        return self.conn

    def select_user(self, tg_id):
        cur = self.connect.cursor()
        SQL = "select * from users where tg_id=?"
        user = cur.execute(SQL, (tg_id, ))
        return user.fetchone()

    def add_user(self, tg_id, username, fullname, phone_number, profile_url):
        conn = self.connect
        cur = conn.cursor()
        SQL = """
        insert into users(tg_id, username, fullname, phone_number, profile_url) 
        values (?, ?, ?, ?, ?);
        """
        cur.execute(SQL, (tg_id, username, fullname, phone_number, profile_url))
        conn.commit()
        user_id = self.select_user(tg_id)[0]
        self.create_order(user_id)

    def create_order(self, user_id):
        conn = self.connect
        cur = conn.cursor()
        order = cur.execute(f'select * from "order" where user_id={user_id} and payment={False}').fetchone()
        if order:
            pass
        else:
            SQL = 'insert into "order" (created_time, update_time, user_id, payment) values (?, ?, ?, ?);'
            cur.execute(SQL, (datetime.now(), datetime.now(), user_id, False))
            conn.commit()

    def select_order(self, user_id):
        conn = self.connect
        cur = conn.cursor()
        resp = cur.execute("select * from 'order' where user_id=? and payment=?", (user_id, False))
        return resp.fetchone()

    def select_order_product(self, user_id, product_id):
        conn = self.connect
        cur = conn.cursor()
        resp = cur.execute("select * from 'order_product' where user_id=? and product_id=?", (user_id, product_id))
        return resp.fetchone()

    def select_order_products(self, order_id):
        conn = self.connect
        cur = conn.cursor()
        SQL = "select * from order_products where order_id=?;"
        resp = cur.execute(SQL, (order_id,))
        return resp.fetchall()

    def select_order_product_all(self, user_id):
        conn = self.connect
        cur = conn.cursor()
        resp = cur.execute("select * from 'order_product' where user_id=?", (user_id, ))
        return resp.fetchall()

    def order_product_add_order(self, order_product_id, order_id):
        conn = self.connect
        cur = conn.cursor()
        SQL = 'insert into "order_products" (order_id, orderproduct_id) values (?, ?);'
        cur.execute(SQL, (order_id, order_product_id))
        conn.commit()

    def add_product(self, product_id, user_id):
        conn = self.connect
        cur = conn.cursor()
        order_product = self.select_order_product(user_id, product_id)
        if order_product:
            SQL_add_order_product = "update 'order_product' set count=? where user_id=? and product_id=?;"
            cur.execute(SQL_add_order_product, (int(order_product[3])+1, user_id, product_id))
        else:
            SQL_create_order_product = "insert into 'order_product' (created_time, update_time, count, product_id, user_id) values (?, ?, ?, ?, ?);"
            cur.execute(SQL_create_order_product, (datetime.now(), datetime.now(), 1, product_id, user_id))
            order_product_id = self.select_order_product(user_id, product_id)[0]
            order_id = self.select_order(user_id)[0]
            self.order_product_add_order(order_product_id, order_id)
        conn.commit()

    def remove_product(self, product_id, user_id):
        conn = self.connect
        cur = conn.cursor()
        order_product = self.select_order_product(user_id, product_id)
        if order_product[3] > 1:
            SQL_remove_order_product = "update 'order_product' set count=? where user_id=? and product_id=?;"
            cur.execute(SQL_remove_order_product, (int(order_product[3]) - 1, user_id, product_id))
        else:
            SQL_delete_order_product = 'delete from "order_product" where product_id=? and user_id=?;'
            cur.execute(SQL_delete_order_product, (product_id, user_id))
        conn.commit()

    def clear_order_products(self, user_id):
        conn = self.connect
        cur = conn.cursor()
        SQL_delete_product = 'delete from "order_product" where user_id=?;'
        cur.execute(SQL_delete_product, (user_id, ))

    def select_categories(self):
        conn = self.connect
        cur = conn.cursor()
        SQL = "select * from category"
        res = cur.execute(SQL).fetchall()
        return res

    def select_sub_categories(self, category_id):
        conn = self.connect
        cur = conn.cursor()
        SQL = "select * from subcategory where category_id=?"
        res = cur.execute(SQL, (category_id, )).fetchall()
        return res

    def select_subcategory(self, subcategory_id):
        conn = self.connect
        cur = conn.cursor()
        SQL = "select * from subcategory where id=?"
        res = cur.execute(SQL, (subcategory_id,)).fetchone()
        return res[1]

    def select_products(self, subcategory_id):
        conn = self.connect
        cur = conn.cursor()
        SQL = "select * from products where subcategory_id=?"
        res = cur.execute(SQL, (subcategory_id,)).fetchall()
        return res

    def select_product(self, product_id):
        conn = self.connect
        cur = conn.cursor()
        SQL = "select * from products where id=?"
        res = cur.execute(SQL, (product_id,)).fetchone()
        return res


# db = Database('C:/Users/Ilhomjon/Desktop/e-commerce-bot/admin/db.sqlite3')
# print(db.select_order_product(2, 3))
# print(db.select_order_products(2))
# print(db.select_order_product())
# all_orders = db.select_order_product_all(5)
# print(all_orders)