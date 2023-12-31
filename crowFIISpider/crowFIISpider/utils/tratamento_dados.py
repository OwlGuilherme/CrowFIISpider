import pandas as pd

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
    
def substituir_virgula(numero_c_virgula):
    numero_c_ponto = ''.join(c if c.isdigit() or c == ',' else '.' for c in numero_c_virgula)
    return float(numero_c_ponto)