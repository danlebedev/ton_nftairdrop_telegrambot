import sqlite3

class DB:
    def __init__(self, wallet: str):
        self.conn = sqlite3.connect('sqlite3.db')
        self.cursor = self.conn.cursor()
        self.wallet = wallet
        self.check_and_create_table()

    def check_and_create_table(self):
        _SQL = """CREATE TABLE IF NOT EXISTS ton_wallets(
            id      INTEGER PRIMARY KEY AUTOINCREMENT,
            wallet  TEXT NOT NULL)
        """
        self.cursor.execute(_SQL)
        self.conn.commit()

    def check_wallet_in_database(self) -> bool:
        # Проверка наличия кошелька в таблице.
        _SQL = """SELECT wallet
            FROM ton_wallets
            WHERE wallet = ?
        """
        self.cursor.execute(_SQL, (self.wallet,))
        return bool(self.cursor.fetchall())

    def add_wallet_in_database(self):
        # Добавление кошелька в таблицу.
        _SQL = """INSERT INTO ton_wallets
            (wallet)
            VALUES
            (?)
        """
        self.cursor.execute(_SQL, (self.wallet,))
        self.conn.commit()

    def close(self):
        self.cursor.close()
        self.conn.close()