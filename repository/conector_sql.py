import sqlite3

class SQLiteConnector:
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.conn = None

    def conectar(self):
        self.conn = sqlite3.connect(self.db_path)
        return self.conn

    def fechar(self):
        if self.conn:
            self.conn.close()

    def executar(self, query: str, params=None):
        cursor = self.conn.cursor()
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)

        self.conn.commit()
        return cursor

    def consultar(self, query: str, params=None):
        cursor = self.conn.cursor()
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)

        return cursor.fetchall()