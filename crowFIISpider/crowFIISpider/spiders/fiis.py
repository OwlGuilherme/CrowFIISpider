import scrapy
from crowFIISpider.utils.database import inserir_dados

class FiisSpider(scrapy.Spider):
    name = "fiis"
    start_urls = ["https://fiis.com.br/lista-de-fundos-imobiliarios/"]

    def parse(self, response):
        # Encontrar todas as classes correspondentes às letras
        classes_letras = response.css('.tickerFilter__results__box').re(r'tickerFilter__results__box-(\w)')

        for classe_letra in classes_letras:
            # Construir o seletor dinâmico para a letra atual
            seletor_letra = f'.tickerFilter__results__box-{classe_letra} [data-element="content-list-ticker"]'

            # Encontrar os elementos para a letra atual
            fiis_letra_elements = response.css(seletor_letra)

            for fii_element in fiis_letra_elements:
                ticker = fii_element.css('.tickerBox__title::text').get()
                link = fii_element.css('.tickerBox__link_ticker::attr(href)').get()
                tipo = fii_element.css('.tickerBox__type::text').get()
                nome = fii_element.css('.tickerBox__desc::text').get()

                yield {
                    'ticker': ticker,
                    'link': link,
                    'tipo': tipo,                
                    'nome': nome
                }

                # Inserir dados no banco de dados
                inserir_dados({
                    'ticker': ticker,
                    'link': link,
                    'tipo': tipo,
                    'nome': nome
                })
