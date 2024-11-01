from sales import Sales
from department import Department
from product import Product
import sqlite3
import os

print(f"Database path: {os.path.abspath('david.db')}")

CONN = sqlite3.connect('david.db')
CURSOR = CONN.cursor()

def create_tables():
    try:
        CURSOR.execute("""CREATE TABLE IF NOT EXISTS department (
            id INTEGER PRIMARY KEY,
            name TEXT,
            year INTEGER
        );
        """)
        
        CURSOR.execute("""CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY,
            name TEXT,
            price REAL,
            quantity INTEGER,
            department_id INTEGER,
            FOREIGN KEY(department_id) REFERENCES department(id)
        );""")
        
        CURSOR.execute("""CREATE TABLE IF NOT EXISTS sales (
            id INTEGER PRIMARY KEY,
            product_id INTEGER,
            quantity INTEGER,
            total_price REAL,
            sale_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(product_id) REFERENCES products(id)
        );""")
        
        CONN.commit()
        print("Tables created successfully.")
    except sqlite3.Error as e:
        print(f"An error occurred while creating tables: {e}")

def add_product(name, price, quantity, department_id):
    if quantity <= 0 or price < 0:
        print("Quantity must be positive and price cannot be negative.")
        return
    try:
        sql = """INSERT INTO products (name, price, quantity, department_id) VALUES (?, ?, ?, ?);"""
        CURSOR.execute(sql, (name, price, quantity, department_id))
        CONN.commit()
        print(f"Product added: {name} | Price: {price} | Quantity: {quantity} | Department ID: {department_id}")
    except sqlite3.Error as e:
        print(f"An error occurred while adding product: {e}")

def add_department(name, year):
    try:
        sql = """INSERT INTO department (name, year) VALUES (?, ?);"""
        CURSOR.execute(sql, (name, year))
        CONN.commit()
        print(f"Department added: Name: {name}, Year: {year}")
    except sqlite3.Error as e:
        print(f"An error occurred while adding department: {e}")



def process_sale(product_id, quantity):
    if quantity <= 0:
        print("Quantity must be positive.")
        return
    try:
        CURSOR.execute("SELECT price, quantity FROM products WHERE id = ?;", (product_id,))
        product = CURSOR.fetchone()
        
        if product and product[1] >= quantity:
            total_price = product[0] * quantity
            CURSOR.execute("INSERT INTO sales (product_id, quantity, total_price) VALUES (?, ?, ?);", 
                           (product_id, quantity, total_price))
            new_quantity = product[1] - quantity
            CURSOR.execute("UPDATE products SET quantity = ? WHERE id = ?;", (new_quantity, product_id))
            CONN.commit()
            print(f"Sale processed: Product ID {product_id} | Quantity {quantity} | Total Price {total_price}")
        else:
            print("Product unavailable or insufficient quantity.")
    except sqlite3.Error as e:
        print(f"An error occurred while processing sale: {e}")

def view_inventory():
    try:
        CURSOR.execute("SELECT id, name, price, quantity FROM products;")
        products = CURSOR.fetchall()
        print("Current Inventory:")
        for product in products:
            print(f"ID: {product[0]}, Name: {product[1]}, Price: {product[2]}, Quantity: {product[3]}")
    except sqlite3.Error as e:
        print(f"An error occurred while viewing inventory: {e}")

def view_sales():
    try:
        CURSOR.execute("""SELECT sales.id, products.name, sales.quantity, sales.total_price, sales.sale_date
                          FROM sales
                          JOIN products ON sales.product_id = products.id;""")
        sales = CURSOR.fetchall()
        print("Sales History:")
        for sale in sales:
            print(f"Sale ID: {sale[0]}, Product: {sale[1]}, Quantity: {sale[2]}, Total Price: {sale[3]}, Date: {sale[4]}")
    except sqlite3.Error as e:
        print(f"An error occurred while viewing sales: {e}")

if __name__ == "__main__":
    create_tables()
    
    # Add a product
    add_product("rice 1kg", 120, 15, 2)
    add_product("pendo", 75, 12, 2)
    add_product("nkatha", 90, 12, 2)
    add_product("sugar", 160, 25, 2)
    add_product("salt", 50, 25, 2)
    add_product("tea", 50, 12, 2)
    add_product("maize", 120, 25, 1)
    add_product("beans", 80, 25, 1)
    add_product("dengu", 120, 25, 1)
    add_product("njahe", 45, 150, 1)    
    add_product("rice 1kg", 120, 15, 1)
    add_product("pendo", 75, 150, 1)
    add_product("rice 1kg", 120, 15, 1)
    add_product("pendo", 75, 150, 1)
    add_product("rice 1kg", 120, 15, 1)
    add_product("pendo", 75, 150, 1)

    
    # Process a sale
    process_sale(1, 1)  # Sell 3 Apples
    process_sale(2, 1) # Sell 5 Bananas
    process_sale(3, 1)  # Sell 3 Apples
    process_sale(4, 1) # Sell 5 Bananas
    process_sale(5, 1)  # Sell 3 Apples
    process_sale(6, 1) # Sell 5 Bananas
    process_sale(7, 1)  # Sell 3 Apples
    process_sale(8, 1) # Sell 5 Bananas
    process_sale(9, 1)  # Sell 3 Apples
    process_sale(10, 1) # Sell 5 Bananas


    add_department("Cereals",2025)
    add_department("FOOD",2025)
    add_department("Drinks",2025)
    add_department("Snacks",2025)
    add_department("Toys",2025)
    # Department.drop_table()
    # Sales.drop_table()
    # Product.drop_table()
    
    # View inventory
    view_inventory()
    
    # View sales history
    view_sales()

    # Close the connection
    CONN.close()
