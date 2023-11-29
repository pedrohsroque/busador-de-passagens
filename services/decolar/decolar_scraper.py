import time
#import pandas as pd
#from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager


class DecolarScraper:
    def __init__(self) -> None:
        self.options = webdriver.ChromeOptions()
        self.options.add_experimental_option('excludeSwitches', ['enable-logging'])
        self.gc = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=self.options)

    def generate_url(self, data_inicio='2023-05-30',data_fim='2023-06-06',origem="MEM", destino="PUJ"):
        return f"https://www.decolar.com/shop/flights/results/roundtrip/{origem}/{destino}/{data_inicio}/{data_fim}/1/0/0/NA/NA/NA/NA/NA?from=SB&di=1-0"

    def get_preco(self, url):
        self.gc.get(url)
        xpath_preco = '//*[@id="clusters"]/span[1]/div/span/cluster/div/div/div[2]/fare/span/span/main-fare/span/span[2]/span/flights-price/span/flights-price-element/span/span/em/span[2]'
        xpath_preco = '//*[@id="toolbox-tabs-position"]/toolbox-tabs/div/tabs/div/div[2]/tab[1]/div/airlines-matrix/span[1]/div/div/div/div/airlines-matrix-airline[1]/ul/li[2]'
        xpath_preco_2 ='//*[@id="toolbox-tabs-position"]/toolbox-tabs/div/tabs/div/div[2]/tab[1]/div/airlines-matrix/span[1]/div/div/div/div/airlines-matrix-airline[1]/ul/li[3]'
        preco = ''
        while preco == '':
            try:
                preco = self.gc.find_element(By.XPATH, xpath_preco)
                print(preco.text)
            except NoSuchElementException:
                print('Aguardando a página carregar')
                time.sleep(2)
            except Exception as e:
                print(e)
                time.sleep(1)
        if preco.text == '':
            print('Buscando outro preço')
            preco = self.gc.find_element(By.XPATH, xpath_preco_2)
            print(preco.text)
        return preco.text

if __name__ == '__main__':
    decolar_scraper = DecolarScraper()
    url = decolar_scraper.generate_url()
    decolar_scraper.get_preco(url)
