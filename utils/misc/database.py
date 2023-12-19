import sqlite3


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
        print("Foydalanuvchi qo'shildi")

    def select_categories(self):
        conn = self.connect
        cur = self.connect.cursor()
        SQL = "select * from category"
        res = cur.execute(SQL).fetchall()
        return res

    def select_sub_categories(self, category_id):
        conn = self.connect
        cur = self.connect.cursor()
        SQL = "select * from subcategory where category_id=?"
        res = cur.execute(SQL, (category_id, )).fetchall()
        return res

    def select_subcategory(self, subcategory_id):
        conn = self.connect
        cur = self.connect.cursor()
        SQL = "select * from subcategory where id=?"
        res = cur.execute(SQL, (subcategory_id,)).fetchone()
        return res[1]

    def select_products(self, subcategory_id):
        conn = self.connect
        cur = self.connect.cursor()
        SQL = "select * from products where subcategory_id=?"
        res = cur.execute(SQL, (subcategory_id,)).fetchall()
        return res

    def select_product(self, product_id):
        conn = self.connect
        cur = self.connect.cursor()
        SQL = "select * from products where id=?"
        res = cur.execute(SQL, (product_id,)).fetchone()
        return res
