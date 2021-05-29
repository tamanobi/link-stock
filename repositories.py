import sqlite3
from contextlib import contextmanager


class StockDB:
    conn = None
    db_name = "image.db"

    def __init__(self):
        self.conn = self.connect()
    
    def connect(self):
        self.conn = sqlite3.connect(self.db_name)
        return self.conn

    def get_connection(self):
        if self.conn:
            return self.conn

        self.conn = self.connect()
        return self.conn

    def get_cursor(self):
        conn = self.get_connection()
        self.cur = conn.cursor()
        return self.cur

    def create_table_if_not_exists(self):
        cur = self.get_cursor()
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS saved
                (
                    id integer
                    , url text
                    , created_at TEXT NOT NULL DEFAULT (DATETIME('now', 'localtime'))
                )
            """
        )

    def get_all(self):
        cur = self.get_cursor()
        cur.execute("SELECT id, url FROM saved")
        return [(x[0], x[1]) for x in cur.fetchall()]

    def insert(self, id_, url):
        cur = self.get_cursor()
        cur.execute(
            """
            INSERT INTO saved (id, url) VALUES (?, ?)
            """,
            [id_, url],
        )

    def commit(self):
        conn = self.get_connection()
        conn.commit()

    def close(self):
        conn = self.get_connection()
        conn.close()


@contextmanager
def stock_db_context():
    db = StockDB() 
    try:
        yield db
    finally:
        db.close()
