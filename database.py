import sqlite3

class DB:
    def __init__(self, wallet: str, user_id: int):
        self.conn = sqlite3.connect('sqlite3.db')
        self.cursor = self.conn.cursor()
        self.wallet = wallet
        self.user_id = user_id
        self.check_and_create_table()

    def check_and_create_table(self):
        _SQL = """CREATE TABLE IF NOT EXISTS ton_wallets(
            id      INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            wallet  TEXT NOT NULL)
        """
        self.cursor.execute(_SQL)
        self.conn.commit()

    def check_wallet_in_database(self) -> bool:
        """Проверка наличия кошелька в таблице."""
        _SQL = """SELECT wallet
            FROM ton_wallets
            WHERE wallet = ?
        """
        self.cursor.execute(_SQL, (self.wallet,))
        return bool(self.cursor.fetchall())
    
    def check_user_in_database(self) -> bool:
        """Проверка наличия юзера в таблице."""
        _SQL = """SELECT user_id
            FROM ton_wallets
            WHERE user_id = ?
        """
        self.cursor.execute(_SQL, (self.user_id,))
        return bool(self.cursor.fetchall())

    def add_wallet_in_database(self):
        """Добавление кошелька в таблицу."""
        _SQL = """INSERT INTO ton_wallets
            (user_id, wallet)
            VALUES
            (?, ?)
        """
        self.cursor.execute(_SQL, (self.user_id, self.wallet,))
        self.conn.commit()

    def close(self):
        self.cursor.close()
        self.conn.close()