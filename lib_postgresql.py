# lib_postgresql.py

import psycopg2
from psycopg2.extras import RealDictCursor

class LibPostgreSQL:
    def __init__(self, host, dbname, user, password, port=5432):
        self.host = host
        self.dbname = dbname
        self.user = user
        self.password = password
        self.port = port
        self.connection = None

    def connect(self):
        if not self.connection:
            self.connection = psycopg2.connect(
                host=self.host,
                database=self.dbname,
                user=self.user,
                password=self.password,
                port=self.port,
                cursor_factory=RealDictCursor
            )
        return self.connection

    def get_cursor(self):
        conn = self.connect()
        return conn.cursor()

    def commit(self):
        if self.connection:
            self.connection.commit()

    def close(self):
        if self.connection:
            self.connection.close()
            self.connection = None