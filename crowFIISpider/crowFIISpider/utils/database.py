import sqlite3


def criar_db():
    with sqlite3.connect('fiis.db') as conn:
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS fiis (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tipo TEXT,
                link TEXT,
                titulo TEXT,
                descricao TEXT
            )
        ''')

def inserir_dados(fii_data):
    with sqlite3.connect('fiis.db') as conn:
        c = conn.cursor()
        c.execute('''
            INSERT INTO fiis (tipo, link, titulo, descricao)
            VALUES (?, ?, ?, ?)
        ''', (
            fii_data['tipo'], fii_data['link'], fii_data['titulo'], fii_data['descricao']
        ))

