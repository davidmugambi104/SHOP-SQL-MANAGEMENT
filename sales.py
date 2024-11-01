from __init__ import CONN, CURSOR

class Sales:
    def __init__(self, product_id, quantity, total_price, id=None, transactions=None):
        self.id = id
        self.product_id = product_id
        self.quantity = quantity
        self.total_price = total_price
        self.transactions = transactions

    def __repr__(self):
        return f"<Sales: ID: {self.id}, Product ID: {self.product_id}, Quantity: {self.quantity}, Price: {self.price}>"

    @classmethod
    def create_table(cls):
        sql = """CREATE TABLE IF NOT EXISTS sales (
        id INTEGER PRIMARY KEY,
        product_id INTEGER,
        quantity INTEGER,
        total_price REAL,
        sale_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(product_id) REFERENCES products(id)
        );"""
        CURSOR.execute(sql)
        CONN.commit()

    @classmethod
    def drop_table(cls):
        sql = """DROP TABLE IF EXISTS sales;"""
        CURSOR.execute(sql)
        CONN.commit()

    def insert(self):
        sql = """INSERT INTO sales (product_id, quantity, price) VALUES (?, ?, ?);"""
        CURSOR.execute(sql, (self.product_id, self.quantity, self.price))
        CONN.commit()
        self.id = CURSOR.lastrowid

    @classmethod
    def save(cls, product_id, quantity, price):
        sale = cls(product_id, quantity, price)
        sale.insert()
        return sale

    def update(self):
        sql = """UPDATE sales SET product_id = ?, quantity = ?, price = ? WHERE id = ?;"""
        CURSOR.execute(sql, (self.product_id, self.quantity, self.price, self.id))
        CONN.commit()

    @classmethod
    def instance_by_id(cls, row):
        return cls(id=row[0], product_id=row[1], quantity=row[2], price=row[3])

    def delete(self):
        sql = """DELETE FROM sales WHERE id = ?;"""
        CURSOR.execute(sql, (self.id,))
        CONN.commit()

    @staticmethod
    def get_all():
        sql = """SELECT * FROM sales;"""
        CURSOR.execute(sql)
        results = CURSOR.fetchall()
        return results
