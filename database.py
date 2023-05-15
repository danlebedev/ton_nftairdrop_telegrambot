import sqlite3

def check_and_create_table():
    conn = sqlite3.connect('sqlite3.db')
    cursor = conn.cursor()
    _SQL = """CREATE TABLE IF NOT EXISTS ton_wallets(
        id      INTEGER PRIMARY KEY AUTOINCREMENT,
        wallet  TEXT NOT NULL)
    """
    cursor.execute(_SQL)
    conn.commit()
    cursor.close()
    conn.close()

def check_and_add_wallet(wallet: str) -> bool:
    conn = sqlite3.connect('sqlite3.db')
    cursor = conn.cursor()
    # Проверка наличия кошелька в таблице.
    _SQL = """SELECT wallet
        FROM ton_wallets
        WHERE wallet = ?
    """
    cursor.execute(_SQL, (wallet,))
    flag = not bool(cursor.fetchall())
    
    if flag:
        # Добавление кошелька в таблицу.
        _SQL = """INSERT INTO ton_wallets
            (wallet)
            VALUES
            (?)
        """
        cursor.execute(_SQL, (wallet,))
        conn.commit()

    cursor.close()
    conn.close()
    return flag