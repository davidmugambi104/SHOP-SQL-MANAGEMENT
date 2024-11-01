from __init__ import CONN, CURSOR


class Department:
    def __init__(self, name, id=None):
        self.name = name
        self.id = id
        
    def __repr__(self):
        return f"{self.id}, {self.name}"
       
    @staticmethod
    def create_table():
        sql = """CREATE TABLE IF NOT EXISTS department (
            id INTEGER PRIMARY KEY,
            name TEXT

        );"""
        CURSOR.execute(sql)
        CONN.commit()

    @staticmethod
    def drop_table():
        sql = """DROP TABLE IF EXISTS department"""
        CURSOR.execute(sql)
        CONN.commit()
        
    def insert(self):
        sql = """INSERT INTO department (name) VALUES (?);"""
        CURSOR.execute(sql, (self.name))
        CONN.commit()
        self.id = CURSOR.lastrowid

    @classmethod
    def save(cls, name):
        department = cls(name)
        department.insert()
        return department
        
    def update(self):
        sql = """UPDATE department SET employee = ?, manager = ?, year = ? WHERE id = ?;"""
        CURSOR.execute(sql, (self.name, self.id))
        CONN.commit()

    @classmethod
    def instance_by_id(cls, row):
        return cls(id=row[0], name=row[1])
        
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
