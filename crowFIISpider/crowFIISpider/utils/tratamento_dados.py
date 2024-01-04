import pandas as pd
import numpy as np

def converte_valor(valor_monetario):
    # Mapeia os sufixos para os fatores multiplicativos
    sufixos = {'M': 1e6, 'B': 1e9}
    
    # Filtra apenas os dígitos, ponto e sufixos
    valor_limpo = ''.join(filter(lambda x: x.isdigit() or x == '.' or x in sufixos, valor_monetario))
    
    # Converte para float
    valor_numerico = float(valor_limpo.replace(',', '.'))

    # Multiplica pelo fator apropriado se houver sufixo
    for sufixo, fator in sufixos.items():
        if sufixo in valor_monetario:
            valor_numerico *= fator
            break

    return int(valor_numerico)
    
def substituir_virgula(numero_c_virgula):
    numero_c_ponto = ''.join(c if c.isdigit() or c == ',' else '.' for c in numero_c_virgula)
    return float(numero_c_ponto)

def trata_variacao(variacao_element):
    variacao_texto = variacao_element.xpath('.//text()').get()
    variacao_limpa = ''.join(filter(lambda x: x.isdigit() or x == '.' or x == '%', variacao_texto))
    variacao_numerica = float(variacao_limpa.replace(',', '.'))

    if 'down' in variacao_element.xpath('./@class').get():
        variacao_numerica *= -1

    return variacao_numerica

def extrair_variacao(variacao_element):
    
    variacao_texto = variacao_element.css('::text').get()

    if 'up' in variacao_element.attrib['class']:
        return float(variacao_texto.strip('%').replace(',', '.'))
    elif 'down' in variacao_element.attrib['class']:
        return -float(variacao_texto.strip('%').replace(',', '.'))

def remover_ponto(numero_com_ponto):
    return numero_com_ponto.replace('.', '')
    


def tratar_detalhes(detalhes):
    detalhes_tratados = {}

    for chave, valor in detalhes.items():
        if chave in ['dividend_yield', 'ultimo_rendimento', 'P/VP', 'cotacao_atual', 'mudança', 'min_52_seman',  'max_52_seman', 'variacao',  'liquidez_media_diaria', 'valor_patrimonial_P_cota', 'participacao_ifix', ]:
            detalhes_tratados[chave] = substituir_virgula(valor)

        elif chave in ['patrimonio_liquido', 'valor_em_caixa']:
            detalhes_tratados[chave] = converte_valor(valor)

        elif chave in ['num_cotistas', 'num_cotas', 'patrimonio']:
            detalhes_tratados[chave] = remover_ponto(valor)

    return detalhes_tratados

def tratar_dados_tabela_yield(df):
    if df is None or df.empty:
        return df

    # Verificar valores inválidos na coluna "Data Base"
    invalid_dates = df[df["Data Base"].apply(lambda x: not pd.to_datetime(x, errors='coerce', dayfirst=True) is pd.NaT)]
    print("Valores inválidos na coluna 'Data Base':", invalid_dates)

    # Substituir valores nulos ou strings vazias
    df = df.replace({None: "", "\n": ""}, regex=True)

    # Remover linhas com todas as células vazias
    df = df.dropna(how="all")

    # Tratar a coluna 'Cotação Base' para converter para float
    df["Cotação Base"] = pd.to_numeric(df["Cotação Base"].replace({",": ".", "R\$": ""}, regex=True), errors="coerce")

    # Tratar a coluna 'Dividend Yield' para remover caracteres não numéricos
    df["Dividend Yield"] = pd.to_numeric(df["Dividend Yield"].str.replace('%', '').replace(",", ".", regex=True), errors="coerce") / 100

    # Tratar a coluna 'Rendimento' para remover caracteres não numéricos
    df["Rendimento"] = pd.to_numeric(df["Rendimento"].str.replace("R\$", "").replace(",", ".", regex=True), errors="coerce")

    # Tratar a coluna 'Data Base' para converter para data e lidar com datas inválidas
    df["Data Base"] = pd.to_datetime(df["Data Base"], format="%d.%m.%Y", errors="coerce", dayfirst=True)

    # Tratar a coluna 'Data Pagamento' para converter para data e lidar com datas inválidas
    df["Data Pagamento"] = pd.to_datetime(df["Data Pagamento"], format="%d.%m.%Y", errors="coerce", dayfirst=True)

    print("DataFrame tratado:")
    print(df)

    return df

