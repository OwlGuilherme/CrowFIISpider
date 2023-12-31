import sqlite3


def criar_db():
    with sqlite3.connect('fiis.db') as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS fiis (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                titulo TEXT,
                link TEXT,
                tipo TEXT,
                descricao TEXT
            )
        ''')

def inserir_dados(fii_data):
    try:
        with sqlite3.connect('fiis.db') as conn:
            conn.execute('''
                    INSERT INTO fiis (titulo, link, tipo, descricao)
                    VALUES (?, ?, ?, ?)
                ''', (
                    fii_data['titulo'], fii_data['link'], fii_data['tipo'], fii_data['descricao']
                ))
            conn.commit()
    except Exception as e:
        print(f'Erro ao inserir dados no banco de dados: {e}')
       

