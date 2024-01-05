from datetime import datetime

import pandas as pd


def converte_valor(valor_monetario):
    # Mapeia os sufixos para os fatores multiplicativos
    sufixos = {"M": 1e6, "B": 1e9}

    # Filtra apenas os dígitos, ponto e sufixos
    valor_limpo = "".join(
        filter(lambda x: x.isdigit() or x == "." or x in sufixos, valor_monetario)
    )

    # Converte para float
    valor_numerico = float(valor_limpo.replace(",", "."))

    # Multiplica pelo fator apropriado se houver sufixo
    for sufixo, fator in sufixos.items():
        if sufixo in valor_monetario:
            valor_numerico *= fator
            break

    return int(valor_numerico)


def substituir_virgula(numero_c_virgula):
    numero_c_ponto = "".join(
        c if c.isdigit() or c == "," else "." for c in numero_c_virgula
    )
    return float(numero_c_ponto)


def trata_variacao(variacao_element):
    variacao_texto = variacao_element.xpath(".//text()").get()
    variacao_limpa = "".join(
        filter(lambda x: x.isdigit() or x == "." or x == "%", variacao_texto)
    )
    variacao_numerica = float(variacao_limpa.replace(",", "."))

    if "down" in variacao_element.xpath("./@class").get():
        variacao_numerica *= -1

    return variacao_numerica


def extrair_variacao(variacao_element):
    variacao_texto = variacao_element.css("::text").get()

    if "up" in variacao_element.attrib["class"]:
        return float(variacao_texto.strip("%").replace(",", "."))
    elif "down" in variacao_element.attrib["class"]:
        return -float(variacao_texto.strip("%").replace(",", "."))


def remover_ponto(numero_com_ponto):
    return numero_com_ponto.replace(".", "")


def tratar_dados_tabela_yield(df):
    for i, row in df.iterrows():
        # Tratar as datas
        try:
            # Ajustar o formato da data (remover "\n" e converter para datetime)
            data_base_str = row["Data Base"]
            if pd.notna(data_base_str):
                df.at[i, "Data Base"] = (
                    datetime.strptime(data_base_str.replace("\n", ""), "%d.%m.%Y")
                    .date()
                    .isoformat()
                )
            else:
                df.at[i, "Data Base"] = None

            data_pagamento_str = row["Data Pagamento"]
            if pd.notna(data_pagamento_str):
                df.at[i, "Data Pagamento"] = (
                    datetime.strptime(data_pagamento_str.replace("\n", ""), "%d.%m.%Y")
                    .date()
                    .isoformat()
                )
            else:
                df.at[i, "Data Pagamento"] = None

        except ValueError:
            df.at[i, "Data Base"] = None
            df.at[i, "Data Pagamento"] = None

        # Tratar os valores numéricos
        try:
            # Ajustar o formato do número fracionário (substituir "," por "." e converter para float)
            cotacao_base_str = row["Cotação Base"]
            if pd.notna(cotacao_base_str):
                df.at[i, "Cotação Base"] = float(
                    cotacao_base_str.replace("R$", "").replace(",", ".").strip()
                )
            else:
                df.at[i, "Cotação Base"] = None

            dividend_yield_str = row["Dividend Yield"]
            if pd.notna(dividend_yield_str):
                # Modificação para lidar com diferentes formatos de percentagem
                df.at[i, "Dividend Yield"] = float(
                    dividend_yield_str.replace("%", "").replace(",", ".").strip()
                )
            else:
                df.at[i, "Dividend Yield"] = None

            # Tratar o campo de rendimento
            rendimento_str = row["Rendimento"]
            if pd.notna(rendimento_str):
                df.at[i, "Rendimento"] = float(
                    rendimento_str.replace("R$", "").replace(",", ".").strip()
                )
            else:
                df.at[i, "Rendimento"] = None
        except ValueError:
            df.at[i, "Cotação Base"] = None
            df.at[i, "Dividend Yield"] = None
            df.at[i, "Rendimento"] = None

    return df
