import sqlite3


def criar_db():
    with sqlite3.connect('fiis.db') as conn:
        c = conn.cursor()

        c.execute('''
            CREATE TABLE IF NOT EXISTIR fiis (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tipo TEXT,
                link TEXT,
                titulo TEXT,
                descricao TEXT
            )
        ''')
