import scrapy
from crowFIISpider.utils.database import inserir_dados

class FiisSpider(scrapy.Spider):
    name = "fiis"
    start_urls = ["https://fiis.com.br/lista-de-fundos-imobiliarios/"]

    def parse(self, response):
        fiis_a_elements = response.css('.tickerFilter__results__box-A [data-element="content-list-ticker"]')

        for fii_element in fiis_a_elements:
            titulo = fii_element.css('.tickerBox__title::text').get()
            link = fii_element.css('.tickerBox__link_ticker::attr(href)').get()
            tipo = fii_element.css('.tickerBox__type::text').get()
            descricao = fii_element.css('.tickerBox__desc::text').get()

            yield {
                'titulo': titulo,
                'link': link,
                'tipo': tipo,                
                'descricao': descricao
            }
            
            # Inserir dados no banco de dados
            inserir_dados({
                'titulo': titulo,
                'link': link,
                'tipo': tipo,
                'descricao': descricao
            })
