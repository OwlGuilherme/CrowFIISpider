import scrapy


class FiisSpider(scrapy.Spider):
    name = "fiis"
    allowed_domains = ["fiis.com.br"]
    start_urls = ["https://fiis.com.br/"]

    def parse(self, response):
        pass
