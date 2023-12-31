import scrapy


class FiisSpider(scrapy.Spider):
    name = "fiis"
    start_urls = ["https://fiis.com.br/lista-de-fundos-imobiliarios/"]

    def parse(self, response):
        fiis_a_elements = response.css('.tickerFilter__results__box-A [data-element="content-list-ticker"]')

        for fii_element in fiis_a_elements:
            tipo = fii_element.css('.tickerBox__type::text').get()
            link = fii_element.css('.tickerBox__link_ticker::attr(href)').get()
            titulo = fii_element.css('.tickerBox__title::text').get()
            descricao = fii_element.css('.tickerBox__desc::text').get()

            yield {
                'tipo': tipo,
                'link' : link,
                'titulo' : titulo,
                'descricao' : descricao
            }
        
