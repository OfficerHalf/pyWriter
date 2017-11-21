import sqlite3


class db:
    def __init__(self, dbName):
        # connect to db
        self.conn = sqlite3.connect(dbName)
        self.c = self.conn.cursor()
