from scrapy.crawler import CrawlerProcess
from crowFIISpider.spiders.fiis import FiisSpider
from crowFIISpider.utils.database import criar_db, inserir_dados

criar_db()

process = CrawlerProcess()
process.crawl(FiisSpider)
process.start()
