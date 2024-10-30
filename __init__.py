import sqlite3
import os
print(f"Database path: {os.path.abspath('david.db')}")


CONN = sqlite3.connect('david.db')

# Create a cursor object to interact with the database
CURSOR = CONN.cursor()

