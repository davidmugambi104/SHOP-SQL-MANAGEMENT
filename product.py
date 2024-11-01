import sqlite3
from __init__ import CONN, CURSOR

class Product:
    def __init__(self, name: str, price: float, quantity: int, department_id: int, id: int = None):
        self.id = id  # ID for the product (None for new products)
        self.department_id = department_id
        self.price = price
        self.name = name
        self.quantity = quantity

    def __repr__(self):
        return f"<Product: {self.name}, Price: {self.price}, Quantity: {self.quantity}, Department ID: {self.department_id}>"

    @classmethod
    def create_table(cls):
        sql = """CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY,
        name TEXT,
        price REAL,
        quantity INTEGER,
        department_id INTEGER,
        FOREIGN KEY(department_id) REFERENCES department(id) ON DELETE CASCADE
        );"""
        try:
            CURSOR.execute(sql)
            CONN.commit()
            print("Products table created successfully.")
        except Exception as e:
            print(f"An error occurred while creating the products table: {e}")

    @classmethod
    def drop_table(cls):
        sql = """DROP TABLE IF EXISTS products;"""
        try:
            CURSOR.execute(sql)
            CONN.commit()
            print("Products table dropped successfully.")
        except Exception as e:
            print(f"An error occurred while dropping the products table: {e}")

    def insert(self):
        sql = """INSERT INTO products (name, price, quantity, department_id) VALUES (?, ?, ?, ?);"""
        try:
            CURSOR.execute(sql, (self.name, self.price, self.quantity, self.department_id))
            CONN.commit()
            self.id = CURSOR.lastrowid  # Store the generated ID
        except Exception as e:
            print(f"An error occurred while inserting product: {e}")

    @classmethod
    def instance_by_id(cls, row):
        return cls(name=row[1], price=row[2], quantity=row[3], department_id=row[4], id=row[0])

class ProductManager:
    def __init__(self, cursor, connection):
        self.cursor = cursor
        self.connection = connection

    def add_product(self, name: str, price: float, quantity: int, department_id: int):
        if quantity <= 0 or price < 0:
            print("Quantity must be positive and price cannot be negative.")
            return
        try:
            sql = """INSERT INTO products (name, price, quantity, department_id) VALUES (?, ?, ?, ?);"""
            self.cursor.execute(sql, (name, price, quantity, department_id))
            self.connection.commit()
            print(f"Product added: {name} | Price: {price} | Quantity: {quantity} | Department ID: {department_id}")
        except sqlite3.Error as e:
            print(f"An error occurred while adding product: {e}")

    def process_sale(self, product_id: int, quantity: int):
        if quantity <= 0:
            print("Quantity must be positive.")
            return
        try:
            self.cursor.execute("SELECT price, quantity FROM products WHERE id = ?;", (product_id,))
            product = self.cursor.fetchone()
            
            if product and product[1] >= quantity:
                total_price = product[0] * quantity
                self.cursor.execute("INSERT INTO sales (product_id, quantity, total_price) VALUES (?, ?, ?);", 
                                   (product_id, quantity, total_price))
                new_quantity = product[1] - quantity
                self.cursor.execute("UPDATE products SET quantity = ? WHERE id = ?;", (new_quantity, product_id))
                self.connection.commit()
                print(f"Sale processed: Product ID {product_id} | Quantity {quantity} | Total Price {total_price}")
            else:
                print("Product unavailable or insufficient quantity.")
        except sqlite3.Error as e:
            print(f"An error occurred while processing sale: {e}")

    def view_inventory(self):
        try:
            self.cursor.execute("SELECT id, name, price, quantity FROM products;")
            products = self.cursor.fetchall()
            print("Current Inventory:")
            for product in products:
                print(f"ID: {product[0]}, Name: {product[1]}, Price: {product[2]}, Quantity: {product[3]}")
        except sqlite3.Error as e:
            print(f"An error occurred while viewing inventory: {e}")

    def view_sales(self):
        try:
            self.cursor.execute("""SELECT sales.id, products.name, sales.quantity, sales.total_price, sales.sale_date
                                  FROM sales
                                  JOIN products ON sales.product_id = products.id;""")
            sales = self.cursor.fetchall()
            print("Sales History:")
            for sale in sales:
                print(f"Sale ID: {sale[0]}, Product: {sale[1]}, Quantity: {sale[2]}, Total Price: {sale[3]}, Date: {sale[4]}")
        except sqlite3.Error as e:
            print(f"An error occurred while viewing sales: {e}")

# Example usage
if __name__ == "__main__":
    product_manager = ProductManager(CURSOR, CONN)
    Product.create_table()  # Ensure the products table exists
    
    # Add a product
    product_manager.add_product("Apple", 0.50, 100, 1)  # Example with department_id 1
    product_manager.add_product("Banana", 0.30, 150, 1)
    
    # Process a sale
    product_manager.process_sale(1, 3)  # Sell 3 Apples
    product_manager.process_sale(2, 5)  # Sell 5 Bananas
    
    # View inventory
    product_manager.view_inventory()
    
    # View sales history
    product_manager.view_sales()
    
    # Close the connection when done
    CONN.close()
