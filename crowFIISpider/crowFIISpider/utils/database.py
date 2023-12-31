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

        conn.execute('''
            CREATE TABLE IF NOT EXISTS detalhes_fiis (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                fii_id INTEGER,
                ticker TEXT,
                nome TEXT,
                dividend_yield REAL,
                ultimo_rendimento REAL,
                patrimonio_liquido REAL,
                pvp TEXT,
                cotacao_atual REAL,
                mudanca REAL,
                min_52_seman REAL,
                max_52_seman REAL,
                variacao REAL,
                valor_em_caixa REAL,
                liquidez_media_diaria REAL,
                valor_patrimonial_p_cota REAL,
                num_cotistas REAL,
                participacao_ifix REAL,
                administrador TEXT,
                cnpj_adm TEXT,
                cnpj TEXT,
                nome_pregao TEXT,
                num_cotas REAL,
                patrimonio REAL,
                tipo_anbima TEXT,
                segmen_anbima TEXT,
                segmento TEXT,
                tipo_gestao TEXT,
                publico_alvo TEXT,
                FOREIGN KEY(fii_id) REFERENCES fiis(id)
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