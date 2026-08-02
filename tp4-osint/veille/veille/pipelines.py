import sqlite3


class CleanPipeline:

    def process_item(self, item):
        for field in item:
            if item[field]:
                item[field] = item[field].strip()

        return item


class SQLitePipeline:

    def open_spider(self):
        self.conn = sqlite3.connect("veille.db")
        self.cursor = self.conn.cursor()

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS mentions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titre TEXT,
            url TEXT UNIQUE,
            source TEXT,
            date_publi TEXT,
            resume TEXT,
            score_alerte INTEGER
        )
        """)

        self.conn.commit()


    def process_item(self, item):

        try:
            self.cursor.execute("""
            INSERT OR IGNORE INTO mentions
            (titre,url,source,date_publi,resume,score_alerte)
            VALUES (?,?,?,?,?,?)
            """,
            (
                item["titre"],
                item["url"],
                item["source"],
                item["date_publi"],
                item["resume"],
                item["score_alerte"]
            ))

            self.conn.commit()

        except Exception as e:
            print("Erreur SQLite :", e)

        return item


    def close_spider(self):
        self.conn.close()