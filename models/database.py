import sqlite3

class DataBase:
    def __init__(self):
        self.db = sqlite3.connect('database.db')

    def getAll(self, sql):
        cur = self.db.cursor()
        cur.execute(sql)
        a = cur.fetchall()
        cur.close()
        return a

    def getAll2(self, sql ,tup):
        cur = self.db.cursor()
        cur.execute(sql, tup)
        a = cur.fetchall()
        cur.close()
        return a

    def getOne(self, sql, tup):
        cur = self.db.cursor()
        cur.execute(sql, tup)
        a = cur.fetchone()
        cur.close()
        return a

    def changeOne(self, sql, tup):
        cur = self.db.cursor()
        cur.execute(sql, tup)
        self.db.commit()
        ret = cur.rowcount
        cur.close()
        return ret

    def changeMany(self, sql, tup):
        cur = self.db.cursor()
        cur.executemany(sql, tup)
        self.db.commit()
        ret = cur.rowcount
        cur.close()
        return ret

    
    def __del__(self):
        self.db.close()