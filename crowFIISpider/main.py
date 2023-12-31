from scrapy.crawler import CrawlerProcess
from crowFIISpider.spiders.fiis import FiisSpider
from crowFIISpider.utils.database import criar_db, inserir_dados
from scrapy.utils.project import get_project_settings

def raspar_dados():
    process = CrawlerProcess(get_project_settings())
    process.crawl(FiisSpider)
    process.start()

def exibir_menu():
    print("+---------------------------+")
    print("|        FiisSpider        |")
    print("+---------------------------+")
    print("|  O que deseja fazer?      |")
    print("+- - - - - - - - - - - - - -+")
    print("| 1. Raspar dados novamente |")
    print("| 2. Opção futura           |")
    print("| 3. Sair                   |")
    print("+---------------------------+")

def main():
    criar_db()  # Certifique-se de que o banco de dados está criado antes de exibir o menu

    while True:
        exibir_menu()
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            raspar_dados()
        elif opcao == "2":
            print("Opção futura")
        elif opcao == "3":
            print("Saindo...")
            break
        else:
            print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    main()