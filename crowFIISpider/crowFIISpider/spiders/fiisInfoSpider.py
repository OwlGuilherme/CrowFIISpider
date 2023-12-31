from typing import Any, Iterable, Optional
import scrapy
import pandas as pd
from scrapy.http import Request
from crowFIISpider.utils.database import carregar_links
from crowFIISpider.utils.tratamento_dados import converte_valor, substituir_virgula


class FiisinfospiderSpider(scrapy.Spider):
    name = "fiisInfoSpider"

    def start_requests(self):
        links_df = carregar_links()

        for index, row in links_df.iterrows():
            yield scrapy.Request(url=row['link'], callback=self.parse, meta={'fii_id': row['id']})
    
    def parse(self, response):


        # Verifica se a variação foi positiva ou negativa
        variacao_element = response.css('.variation')
        variacao_texto = variacao_element.css('::text').get()

        if 'up' in variacao_element.attrib['class']:
            variacao = float(variacao_texto.strip('%').replace(',', '.'))
        elif 'down' in variacao_element.attrib['class']:
            variacao = -float(variacao_texto.strip('%').replace(',', '.'))

        detalhes = {
            'ticker' : response.xpath('//*[@id="carbon_fields_fiis_header-2"]/div/div/div[1]/div[1]/p/text()').get(),
            'nome' : response.xpath('//*[@id="carbon_fields_fiis_header-2"]/div/div/div[1]/div[1]/p/text()').get(),
            'dividend_yield' : response.xpath('//*[@id="carbon_fields_fiis_header-2"]/div/div/div[1]/div[2]/div/div[1]/p[1]/b/text()').get(),
            'ultimo_rendimento' : response.xpath('//*[@id="carbon_fields_fiis_header-2"]/div/div/div[1]/div[2]/div/div[2]/p[1]/b/text()').get(),
            'patrimonio_liquido' : response.xpath('//*[@id="carbon_fields_fiis_header-2"]/div/div/div[1]/div[2]/div/div[3]/p[1]/b/text()').get(),
            'P/VP' : response.xpath('//*[@id="carbon_fields_fiis_header-2"]/div/div/div[1]/div[2]/div/div[4]/p[1]/b/text()').get(),
            'cotacao_atual' : response.xpath('//*[@id="carbon_fields_fiis_quotations_chart-2"]/div[1]/div[2]/div[1]/div[1]/span[2]/text()').get(),
            'mudanca' : response.xpath('//*[@id="carbon_fields_fiis_quotations_chart-2"]/div[1]/div[2]/div[1]/div[1]/div/span/text()').get(),
            'min_52_seman' : response.xpath('//*[@id="carbon_fields_fiis_quotations_chart-2"]/div[1]/div[2]/div[2]/div[1]/span[2]/text()') .get(),
            'max_52_seman' : response.xpath('//*[@id="carbon_fields_fiis_quotations_chart-2"]/div[1]/div[2]/div[3]/div[1]/span[2]/text()').get(),
            'variacao' : response.xpath('//*[@id="carbon_fields_fiis_quotations_chart-2"]/div[1]/div[2]/div[4]/div[1]/span/text()').get(),
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
            'segmento' : response.xpath('//*[@id="carbon_fields_fiis_informations-2"]/div[3]/p[7]/span/text()').get(),
            'tipo_gestao' : response.xpath('//*[@id="carbon_fields_fiis_informations-2"]/div[3]/p[8]/b/text()').get(),
            'publico_alvo' : response.xpath('//*[@id="carbon_fields_fiis_informations-2"]/div[3]/p[9]/b/text()').get()
        }


