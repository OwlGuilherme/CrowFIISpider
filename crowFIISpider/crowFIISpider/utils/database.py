import json
import sqlite3

import polars as pl


def criar_db():
    with sqlite3.connect("fiis.db") as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS fiis (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ticker TEXT,
                link TEXT,
                tipo TEXT,
                nome TEXT
            )
        """
        )

        conn.execute(
            """
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
            dados_tabela_json TEXT,
            FOREIGN KEY(fii_id) REFERENCES fiis(id)
        )
    """
        )


def inserir_dados(fii_data):
    try:
        with sqlite3.connect("fiis.db") as conn:
            conn.execute(
                """
                    INSERT INTO fiis (ticker, link, tipo, nome)
                    VALUES (?, ?, ?, ?)
                """,
                (
                    fii_data["ticker"],
                    fii_data["link"],
                    fii_data["tipo"],
                    fii_data["nome"],
                ),
            ) 
            conn.commit()
    except Exception as e:
        print(f"Erro ao inserir dados no banco de dados: {e}")


def carregar_links():
    with sqlite3.connect("fiis.db") as conn:
        query = "SELECT id, link FROM fiis"
        
        df = pl.read_database(query=query, connection=conn)

        #df = pd.read_sql_query(query, conn)

        return df


def inserir_dados_detalhados(detalhes_fii_data, dados_tabela_yield):
    try:
        with sqlite3.connect("fiis.db") as conn:
            # Verificar se os dados já existem no banco de dados
            existing_data = conn.execute(
                """
                SELECT id FROM detalhes_fiis
                WHERE fii_id = ? AND ticker = ? AND nome = ?
            """,
                (
                    detalhes_fii_data["fii_id"],
                    detalhes_fii_data["ticker"],
                    detalhes_fii_data["nome"],
                ),
            ).fetchone()

            dados_tabela_json = dados_tabela_yield

            if existing_data:
                # Se os dados já existem, atualize-os em vez de inseri-los novamente
                conn.execute(
                    """
                    UPDATE detalhes_fiis
                    SET
                        fii_id = ?,
                        ticker = ?,
                        nome = ?,
                        dividend_yield = ?,
                        ultimo_rendimento = ?,
                        patrimonio_liquido = ?,
                        PVP = ?,
                        cotacao_atual = ?,
                        mudanca = ?,
                        min_52_seman = ?,
                        max_52_seman = ?,
                        variacao = ?,
                        valor_em_caixa = ?,
                        liquidez_media_diaria = ?,
                        valor_patrimonial_P_cota = ?,
                        num_cotistas = ?,
                        participacao_ifix = ?,
                        administrador = ?,
                        cnpj_adm = ?,
                        cnpj = ?,
                        nome_pregao = ?,
                        num_cotas = ?,
                        patrimonio = ?,
                        tipo_anbima = ?,
                        segmen_anbima = ?,
                        segmento = ?,
                        tipo_gestao = ?,
                        publico_alvo = ?,
                        dados_tabela_json = ?
                    WHERE id = ?
                """,
                    (
                        detalhes_fii_data["fii_id"],
                        detalhes_fii_data["ticker"],
                        detalhes_fii_data["nome"],
                        detalhes_fii_data["dividend_yield"],
                        detalhes_fii_data["ultimo_rendimento"],
                        detalhes_fii_data["patrimonio_liquido"],
                        detalhes_fii_data["P/VP"],
                        detalhes_fii_data["cotacao_atual"],
                        detalhes_fii_data["mudanca"],
                        detalhes_fii_data["min_52_seman"],
                        detalhes_fii_data["max_52_seman"],
                        detalhes_fii_data["variacao"],
                        detalhes_fii_data["valor_em_caixa"],
                        detalhes_fii_data["liquidez_media_diaria"],
                        detalhes_fii_data["valor_patrimonial_P_cota"],
                        detalhes_fii_data["num_cotistas"],
                        detalhes_fii_data["participacao_ifix"],
                        detalhes_fii_data["administrador"],
                        detalhes_fii_data["cnpj_adm"],
                        detalhes_fii_data["cnpj"],
                        detalhes_fii_data["nome_pregao"],
                        detalhes_fii_data["num_cotas"],
                        detalhes_fii_data["patrimonio"],
                        detalhes_fii_data["tipo_anbima"],
                        detalhes_fii_data["segmen_anbima"],
                        detalhes_fii_data["segmento"],
                        detalhes_fii_data["tipo_gestao"],
                        detalhes_fii_data["publico_alvo"],
                        dados_tabela_json,
                        existing_data[0],
                    ),
                )
            else:
                # Se os dados não existem, insira-os normalmente
                conn.execute(
                    """
                    INSERT INTO detalhes_fiis (
                        fii_id, ticker, nome, dividend_yield, ultimo_rendimento, patrimonio_liquido,
                        PVP, cotacao_atual, mudanca, min_52_seman, max_52_seman, variacao,
                        valor_em_caixa, liquidez_media_diaria, valor_patrimonial_P_cota,
                        num_cotistas, participacao_ifix, administrador, cnpj_adm, cnpj,
                        nome_pregao, num_cotas, patrimonio, tipo_anbima, segmen_anbima,
                        segmento, tipo_gestao, publico_alvo, dados_tabela_json
                    )
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                    (
                        detalhes_fii_data["fii_id"],
                        detalhes_fii_data["ticker"],
                        detalhes_fii_data["nome"],
                        detalhes_fii_data["dividend_yield"],
                        detalhes_fii_data["ultimo_rendimento"],
                        detalhes_fii_data["patrimonio_liquido"],
                        detalhes_fii_data["P/VP"],
                        detalhes_fii_data["cotacao_atual"],
                        detalhes_fii_data["mudanca"],
                        detalhes_fii_data["min_52_seman"],
                        detalhes_fii_data["max_52_seman"],
                        detalhes_fii_data["variacao"],
                        detalhes_fii_data["valor_em_caixa"],
                        detalhes_fii_data["liquidez_media_diaria"],
                        detalhes_fii_data["valor_patrimonial_P_cota"],
                        detalhes_fii_data["num_cotistas"],
                        detalhes_fii_data["participacao_ifix"],
                        detalhes_fii_data["administrador"],
                        detalhes_fii_data["cnpj_adm"],
                        detalhes_fii_data["cnpj"],
                        detalhes_fii_data["nome_pregao"],
                        detalhes_fii_data["num_cotas"],
                        detalhes_fii_data["patrimonio"],
                        detalhes_fii_data["tipo_anbima"],
                        detalhes_fii_data["segmen_anbima"],
                        detalhes_fii_data["segmento"],
                        detalhes_fii_data["tipo_gestao"],
                        detalhes_fii_data["publico_alvo"],
                        dados_tabela_json,
                    ),
                )

            conn.commit()
    except Exception as e:
        print(f"Erro ao inserir dados detalhados no banco de dados: {e}")


def spider_closed(self, spider, reason):
    # Fechar a conexão com o banco de dados quando a spider for fechada
    if hasattr(self, "conn") and self.conn is not None:
        self.conn.close()


def extrair_dados_tabela_yield(self, response):
    dados = []

    for row in response.css(".yieldChart__table__bloco"):
        dado = {
            "Data Base": row.css(".table__linha:nth-child(1)::text").get(),
            "Data Pagamento": row.css(".table__linha:nth-child(2)::text").get(),
            "Cotação Base": row.css(".table__linha:nth-child(3)::text").get(),
            "Dividend Yield": row.css(".table__linha:nth-child(4)::text").get(),
            "Rendimento": row.css(".table__linha:nth-child(5)::text").get(),
        }
        dados.append(dado)

    # Criando um DataFrame do Pandas
    df = pl.DataFrame(dados)
    return df


def carregar_dividendos():
    ticker = input("Digite o ticker do FII desejado: ").upper()

    try:
        with sqlite3.connect("fiis.db") as conn:
            query = f"""
                SELECT dados_tabela_json
                FROM detalhes_fiis
                WHERE ticker = ?    
            """

            result = conn.execute(query, (ticker,)).fetchone()

            pl.Config.set_tbl_rows(100)

            if result:
                dados_tabela_json = result[0]

                json_data = json.loads(dados_tabela_json)

                df = pl.DataFrame(json_data)

                print(df)
            else:
                print(f"Não foram encontrados dados para o FII com o ticker {ticker}")

    except Exception as e:
        print(f"Erro ao recuperar dados do banco de dados: {e}")
