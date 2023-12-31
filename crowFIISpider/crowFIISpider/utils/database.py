import sqlite3
import pandas as pd


def criar_db():
    with sqlite3.connect('fiis.db') as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS fiis (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ticker TEXT,
                link TEXT,
                tipo TEXT,
                nome TEXT
            )
        ''')

def inserir_dados(fii_data):
    try:
        with sqlite3.connect('fiis.db') as conn:
            conn.execute('''
                    INSERT INTO fiis (ticker, link, tipo, nome)
                    VALUES (?, ?, ?, ?)
                ''', (
                    fii_data['ticker'], fii_data['link'], fii_data['tipo'], fii_data['nome']
                ))
            conn.commit()
    except Exception as e:
        print(f'Erro ao inserir dados no banco de dados: {e}')
       

def carregar_links():
    with sqlite3.connect('fiis.db') as conn:
        query = 'SELECT id, link FROM fiis'
        df = pd.read_sql_query(query, conn)

        return df