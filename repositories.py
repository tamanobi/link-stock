import sqlite3


class StockDB:
    cur = None
    
    @classmethod
    def get_cursor(cls):
        if cls.cur:
            return cls.cur
        
        conn = sqlite3.connect("image.db")
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