from scrapy.crawler import CrawlerProcess
from crowFIISpider.spiders.fiis import FiisSpider
from crowFIISpider.spiders.fiisInfoSpider import FiisinfospiderSpider
from crowFIISpider.utils.database import criar_db, carregar_dividendos
from scrapy.utils.project import get_project_settings

def raspar_dados():
    process = CrawlerProcess(get_project_settings())
    process.crawl(FiisSpider)
    process.start()

def raspar_dados_detalhados():
    process = CrawlerProcess(get_project_settings())
    process.crawl(FiisinfospiderSpider)
    process.start()

def exibir_menu():
    print("+-----------------------------+")
    print("|          FiisSpider         |")
    print("+-----------------------------+")
    print("|  O que deseja fazer?        |")
    print("+- - - - - - - - - - - - - - -+")
    print("| 1. Raspar dados novamente   |")
    print("| 2. Raspar dados detalhados  |")
    print("| 3. Histórico de dividendos  |")
    print("| 4. Sair                     |")
    print("+-----------------------------+")

def main():
    criar_db()

    while True:
        exibir_menu()
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            raspar_dados()
        elif opcao == "2":
            raspar_dados_detalhados()
        elif opcao == '3':
            carregar_dividendos()
        elif opcao == "4":
            print("Saindo...")
            break
        else:
            print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    main()

