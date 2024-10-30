import sqlite3
import os

# Print the absolute path of the database file for verification
print(f"Database path: {os.path.abspath('david.db')}")

# Connect to the SQLite database (or create it if it doesn't exist)
CONN = sqlite3.connect('david.db')
CURSOR = CONN.cursor()

# Create the table if it doesn't exist
def create_table():
    sql = """CREATE TABLE IF NOT EXISTS department (
        id INTEGER PRIMARY KEY,
        employee TEXT,
        manager TEXT,
        year INTEGER
    );"""
    CURSOR.execute(sql)
    CONN.commit()

class Department:
    def __init__(self, employee, year, manager, id=None):
        self.employee = employee
        self.year = year
        self.manager = manager
        self.id = id

    def insert(self):
        """Insert a new department record."""
        sql = """INSERT INTO department (employee, manager, year) VALUES (?, ?, ?);"""
        CURSOR.execute(sql, (self.employee, self.manager, self.year))
        CONN.commit()
        self.id = CURSOR.lastrowid
        print(f"Inserted Department ID: {self.id}")

    def update(self):
        """Update the department record."""
        sql = """UPDATE department SET employee = ?, manager = ?, year = ? WHERE id = ?;"""
        CURSOR.execute(sql, (self.employee, self.manager, self.year, self.id))
        CONN.commit()
        print(f"Updated Department ID {self.id}: {self}")

    def __repr__(self):
        return f"{self.id}, {self.employee}, {self.manager}, {self.year}"

# Retrieve all departments
def get_all_departments():
    CURSOR.execute("SELECT * FROM department;")
    return CURSOR.fetchall()

# Example usage
if __name__ == "__main__":
    # Step 1: Create the table
    create_table()

    # Step 2: Insert a new department
    dept = Department("Lyan Mutura", 2025, "DAVID MUGAMBI")
    dept.insert()

    # Step 3: Retrieve and display all departments
    departments = get_all_departments()
    print("Departments after insertion:", departments)

    # Step 4: Update the department
    dept.employee = "Anna"
    dept.update()  # Update the department's employee name

    # Step 5: Retrieve and display all departments after update
    departments_after_update = get_all_departments()
    print("Departments after update:", departments_after_update)

    # Close the connection
    CONN.close()
