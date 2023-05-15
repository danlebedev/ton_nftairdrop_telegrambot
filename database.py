import sqlite3

def check_and_create_db():
    conn = sqlite3.connect('sqlite3.db')
    cursor = conn.cursor()
    _SQL = """CREATE TABLE IF NOT EXISTS ton_wallets(
        id      INTEGER PRIMARY KEY AUTOINCREMENT,
        wallet  TEXT NOT NULL
    )"""
    cursor.execute(_SQL)
    conn.commit()
    cursor.close()
    conn.close()