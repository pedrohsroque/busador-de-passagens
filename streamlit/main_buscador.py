import json
import requests
import pandas as pd
import os, sys
sys.path.append(os.getcwd())
from services.decolar.decolar_scraper import DecolarScraper


def get_cheapest_date(origem="MEM", destino="PUJ"):
    url = f"https://www.decolar.com/passagens-aereas/{origem}/{destino}?from=SB&di=1-0#showModal"
    #url = f"https://www.decolar.com/passagens-aereas/{origem}/{destino}?from=SB&di=1-0&outboundMonthRanges=202402,202403,202404,202405"
    r = requests.get(url=url)
    if r.status_code not in (200, "200"):
        raise RuntimeError("Erro na requisição")
    return r.text


def get_specific_data(data_inicio='2023-05-30',data_fim='2023-06-06',origem="MEM", destino="PUJ"):
    url = f"https://www.decolar.com/shop/flights/results/roundtrip/{origem}/{destino}/{data_inicio}/{data_fim}/1/0/0/NA/NA/NA/NA/NA?from=SB&di=1-0"
    r = requests.get(url=url)
    if r.status_code not in (200, "200"):
        raise RuntimeError("Erro na requisição")
    return r.text


def save_data(text: str,filename='temp.html'):
    with open(filename, "w", encoding='utf8') as f:
        f.writelines(text)


def load_data(path="temp.html"):
    with open(path, "r",encoding='utf8') as f:
        html = f.read()
    return html


def extract_data(html):
    data = json.loads(html.split("var jsonDataItems = ")[1].split("\n")[0])
    if len(data) == 0:
        print("Data not found")
        return None
    for data_item in data:
        try:
            price = data_item["item"]["priceDetail"]["adultTotal"]
            start_date = data_item["item"]["sections"][0]["date"]
            end_date = data_item["item"]["routeChoices"][1]["routes"][0]["segments"][0][
                "departure"
            ]["date"]
            return {
                "price":price,
                "start_date":start_date[:10],
                "end_date":end_date[:10]
            }
        except KeyError:
            print("A chave não existe")


def listar_menores_precos(lista_origens, lista_destinos, force_refresh=False):
    prices = []
    for origem in lista_origens:
        for destino in lista_destinos:
            print(f'{origem=}{destino=}')
            cheapest_filename=f'data/cheapest/{origem}_{destino}.html'
            if not os.path.isfile(cheapest_filename) or force_refresh:
                cheapest_data=get_cheapest_date(origem=origem,destino=destino)
                # save_data(cheapest_data, filename=cheapest_filename)
                html = cheapest_data
            else:
                html = load_data(path=cheapest_filename)
            best_price = extract_data(html=html)
            if not best_price:
                continue
            best_price['origem']=origem
            best_price['destino']=destino
            prices.append(best_price)

    df_prices = pd.DataFrame(prices)
    df_prices.to_csv('data/cheapest/prices.csv', index=False)
    print(df_prices)
    return df_prices


def listar_precos_especificos(origem, destino, data_inicio, data_fim, driver):
    print('Buscando dados')
    url = driver.generate_url(origem=origem,destino=destino,data_inicio=data_inicio, data_fim=data_fim)
    return driver.get_preco(url)


def get_estimation():
    df_prices = pd.read_csv('data/cheapest/prices.csv')
    df_prices_resumido = df_prices.drop_duplicates(subset=['start_date','end_date']) # retirando duplicadas para não pesquisas mais de uma vez

    decolar_scraper = DecolarScraper()
    with open('data/specific_prices.csv','w') as f:
        f.write('ref_id,price,start_date,end_date,origem,destino\n')
        for idx_referencia, item_referencia in df_prices_resumido.iterrows():
            print(f"Buscando preços para {item_referencia['destino']}, data de ida={item_referencia['start_date']}, data de volta={item_referencia['end_date']}")
            for idx, item in df_prices.iterrows():
                if idx!=idx_referencia:
                    new_price = listar_precos_especificos(origem=item['origem'],destino=item['destino'],data_inicio=item_referencia['start_date'],data_fim=item_referencia['end_date'], driver=decolar_scraper)
                    new_price = new_price.replace('.','').replace('R$','')
                    f.write(f"{idx_referencia},{new_price},{item_referencia['start_date']},{item_referencia['end_date']},{item['origem']},{item['destino']}\n")
                    if item['origem'] == 'BHZ': #Write again, since it's 2 people
                        f.write(f"{idx_referencia},{new_price},{item_referencia['start_date']},{item_referencia['end_date']},{item['origem']},{item['destino']}\n")
                else:
                    #print('Já temos dado sobre este item')
                    f.write(f"{idx_referencia},{item_referencia['price']},{item_referencia['start_date']},{item_referencia['end_date']},{item_referencia['origem']},{item_referencia['destino']}\n")
                    if item['origem'] == 'BHZ': #Write again, since it's 2 people
                        f.write(f"{idx_referencia},{item_referencia['price']},{item_referencia['start_date']},{item_referencia['end_date']},{item_referencia['origem']},{item_referencia['destino']}\n")

    specific_prices = pd.read_csv('data/specific_prices.csv')
    specific_prices = specific_prices.groupby(by=['ref_id','start_date','end_date','destino']).sum('price').sort_values(['price'], ascending=True)
    print(specific_prices)
    specific_prices.to_csv('data/estimation.csv')



#pegar os melhores preços para cada um
#lista_origens=['BHZ','BSB','FLN','MEM','SAO','HOU','CCS']
#lista_destinos=['PUJ']
#listar_menores_precos(lista_origens=lista_origens, lista_destinos=lista_destinos,force_refresh=False)

#get_estimation()
