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