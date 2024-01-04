from typing import Any, Iterable, Optional
import scrapy
import pandas as pd
from scrapy.http import Request
from crowFIISpider.utils.database import carregar_links, inserir_dados_detalhados
from crowFIISpider.utils.tratamento_dados import extrair_variacao, tratar_dados_tabela_yield
import sqlite3


class FiisinfospiderSpider(scrapy.Spider):
    name = "fiisInfoSpider"

    def __init__(self, *args, **kwargs):
        super(FiisinfospiderSpider, self).__init__(*args, **kwargs)
        self.conn = sqlite3.connect('fiis.db')

    def start_requests(self):
        links_df = carregar_links()

        for index, row in links_df.iterrows():
            yield scrapy.Request(url=row['link'], callback=self.parse, meta={'fii_id': row['id']})

    
    def parse(self, response):

        variacao_element = response.css('.variation')

        detalhes = {
            'ticker' : response.xpath('//*[@id="carbon_fields_fiis_header-2"]/div/div/div[1]/div[1]/h1/text()').get(),
            'nome' : response.xpath('//*[@id="carbon_fields_fiis_header-2"]/div/div/div[1]/div[1]/p/text()').get(),
            'dividend_yield' : response.xpath('//*[@id="carbon_fields_fiis_header-2"]/div/div/div[1]/div[2]/div/div[1]/p[1]/b/text()').get(),
            'ultimo_rendimento' : response.xpath('//*[@id="carbon_fields_fiis_header-2"]/div/div/div[1]/div[2]/div/div[2]/p[1]/b/text()').get(),
            'patrimonio_liquido' : response.xpath('//*[@id="carbon_fields_fiis_header-2"]/div/div/div[1]/div[2]/div/div[3]/p[1]/b/text()').get(),
            'P/VP' : response.xpath('//*[@id="carbon_fields_fiis_header-2"]/div/div/div[1]/div[2]/div/div[4]/p[1]/b/text()').get(),
            'cotacao_atual' : response.xpath('//*[@id="carbon_fields_fiis_quotations_chart-2"]/div[1]/div[2]/div[1]/div[1]/span[2]/text()').get(),
            'mudanca' : response.xpath('//*[@id="carbon_fields_fiis_quotations_chart-2"]/div[1]/div[2]/div[1]/div[1]/div/span/text()').get().strip(),
            'min_52_seman' : response.xpath('//*[@id="carbon_fields_fiis_quotations_chart-2"]/div[1]/div[2]/div[2]/div[1]/span[2]/text()') .get(),
            'max_52_seman' : response.xpath('//*[@id="carbon_fields_fiis_quotations_chart-2"]/div[1]/div[2]/div[3]/div[1]/span[2]/text()').get(),
            # A variação é estraída de forma diversa vista que o elemento é dinâmico a depender do caso.
            'variacao': extrair_variacao(variacao_element),
            'valor_em_caixa' : response.xpath('//*[@id="carbon_fields_fiis_quotations_chart-2"]/div[2]/div[1]/p[1]/b/text()').get(),
            'liquidez_media_diaria': response.xpath('//*[@id="carbon_fields_fiis_quotations_chart-2"]/div[2]/div[2]/p[1]/b/text()').get(),
            'valor_patrimonial_P_cota': response.xpath('//*[@id="carbon_fields_fiis_quotations_chart-2"]/div[2]/div[3]/p[1]/b/text()').get(),
            'num_cotistas' : response.xpath('//*[@id="carbon_fields_fiis_quotations_chart-2"]/div[2]/div[4]/p[1]/b/text()').get(),
            'participacao_ifix' : response.xpath('//*[@id="carbon_fields_fiis_quotations_chart-2"]/div[2]/div[5]/p[1]/b/text()').get(),
            'administrador' : response.xpath('//*[@id="carbon_fields_fiis_informations-2"]/div[1]/div[1]/p/text()').get(),
            'cnpj_adm' : response.xpath('//*[@id="carbon_fields_fiis_informations-2"]/div[1]/div[1]/span[2]/text()').get(),
            'cnpj' : response.xpath('//*[@id="carbon_fields_fiis_informations-2"]/div[3]/p[1]/b/text()').get(),
            'nome_pregao' : response.xpath('//*[@id="carbon_fields_fiis_informations-2"]/div[3]/p[2]/b/text()').get(),
            'num_cotas' : response.xpath('//*[@id="carbon_fields_fiis_informations-2"]/div[3]/p[3]/b/text()').get(),
            'patrimonio' : response.xpath('//*[@id="carbon_fields_fiis_informations-2"]/div[3]/p[4]/b/text()').get(),
            'tipo_anbima' : response.xpath('//*[@id="carbon_fields_fiis_informations-2"]/div[3]/p[4]/b/text()').get(),
            'segmen_anbima' : response.xpath('//*[@id="carbon_fields_fiis_informations-2"]/div[3]/p[6]/b/text()').get(),
            'segmento' : response.xpath('//*[@id="carbon_fields_fiis_informations-2"]/div[3]/p[7]/b/text()').get(),
            'tipo_gestao' : response.xpath('//*[@id="carbon_fields_fiis_informations-2"]/div[3]/p[8]/b/text()').get(),
            'publico_alvo' : response.xpath('//*[@id="carbon_fields_fiis_informations-2"]/div[3]/p[9]/b/text()').get()
        }

        detalhes['fii_id'] = response.meta['fii_id']
        

        # Extrair e salvar tabela de dividendos
        dados_tabela_yield = self.extrair_dados_tabela_yield(response)

        inserir_dados_detalhados(detalhes, dados_tabela_yield)


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

            for chave, valor in dado.items():
                if valor is not None:
                    dado[chave] = valor.strip()

            dados.append(dado)

        # Criando um DataFrame do Pandas
        df = pd.DataFrame(dados)

        # Tratando os dados com a função existente
        df_tratado = tratar_dados_tabela_yield(df)

        # Convertendo o DataFrame tratado para JSON
        dados_json = df_tratado.to_json(orient='records')

        return dados_json

def spider_closed(self, spider, reason):
    # Fechar a conexão com o banco de dados quando a spider for fechada
    if hasattr(self, 'conn') and self.conn is not None:
        self.conn.close()

