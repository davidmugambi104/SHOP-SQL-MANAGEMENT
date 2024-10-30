from __init__ import CONN, CURSOR

class Department:
    def __init__(self, employee, year, manager, id=None):
        self.employee = employee
        self.id = id
        self.year = year
        self.manager = manager

    def __repr__(self):
        return f"{self.id}, {self.employee}, {self.manager}, {self.year}"
       
    @staticmethod
    def create_table():
        sql = """CREATE TABLE IF NOT EXISTS department (
            id INTEGER PRIMARY KEY,
            employee TEXT,
            manager TEXT,
            year INTEGER
        );"""
        CURSOR.execute(sql)
        CONN.commit()

    @staticmethod
    def drop_table():
        sql = """DROP TABLE IF EXISTS department"""
        CURSOR.execute(sql)
        CONN.commit()
        
    def insert(self):
        sql = """INSERT INTO department (employee, manager, year) VALUES (?, ?, ?);"""
        CURSOR.execute(sql, (self.employee, self.manager, self.year))
        CONN.commit()
        self.id = CURSOR.lastrowid

    @classmethod
    def save(cls, employee, manager, year):
        department = cls(employee, year, manager)
        department.insert()
        return department
        
    def update(self):
        sql = """UPDATE department SET employee = ?, manager = ?, year = ? WHERE id = ?;"""
        CURSOR.execute(sql, (self.employee, self.manager, self.year, self.id))
        CONN.commit()

    @classmethod
    def instance_by_id(cls, row):
        return cls(id=row[0], employee=row[1], year=row[3], manager=row[2])
        
    def delete(self):
        sql = """DELETE FROM department WHERE id = ?;"""
        CURSOR.execute(sql, (self.id,))
        CONN.commit()
        
    @staticmethod
    def get_all():
        sql = """SELECT * FROM department"""
        CURSOR.execute(sql)
        results = CURSOR.fetchall()
        return results
