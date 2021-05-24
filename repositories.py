import sqlite3


class StockDB:
    conn = None
    
    @classmethod
    def get_connection(cls):
        if cls.conn:
            return cls.conn

        cls.conn = sqlite3.connect("image.db")
        return cls.conn

    @classmethod
    def get_cursor(cls):
        conn = cls.get_connection()
        cls.cur = conn.cursor()
        return cls.cur

    @classmethod
    def create_table_if_not_exists(cls):
        cur = cls.get_cursor()
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