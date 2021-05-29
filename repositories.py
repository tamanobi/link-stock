import sqlite3


class StockDB:
    conn = None
    
    def get_connection(self):
        if self.conn:
            return self.conn

        self.conn = sqlite3.connect("image.db")
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
        self.conn.commit()

    def close(self):
        self.conn.close()
