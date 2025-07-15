import requests
from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import os
from glob import glob

# definimos os 4 principais sites que queremos extrair notícias
# g1.globo.com, noticias.uol.com.br, agenciabrasil.ebc.com.br
# pesquisamos no google da seguinte maneira: site:g1.globo.com "Juliana Marins"
# extraimos manualmente 40 urls desses sites, 10 por fonte, sobre o caso e inserimos em um arquivo url.csv com os campos 'fonte' e 'url'

saidas_dir = os.path.abspath(os.path.join(os.getcwd(), '..', 'saidas')) # Localizando a pasta saidas
os.makedirs(saidas_dir, exist_ok=True)

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
}

def extract_websites_from_google_query(google_query, driver, termo, pages):   
    websites = []

    for page in range(pages):
        driver.get(f'https://www.google.com/search?q={google_query}&tbm=nws&start={page*10}')
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        noticias = soup.find_all('div', attrs={'data-news-cluster-id': True})
        websites.extend([noticia.find('a', attrs={"ping": True})['href'] for noticia in noticias if termo.split(' ')[0] in noticia.text.lower()])

    return websites
            

def start_driver(headless=False):
    chrome_options = Options()
    if headless == True:
        chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument(f"user-agent={headers['User-Agent']}")
    driver = webdriver.Chrome(options=chrome_options)
    return driver


def get_text_from_website(website, driver):
    textos = []

    try:
        if 'g1' in website:
            html = requests.get(website, headers=headers).content
            soup = BeautifulSoup(html, 'html.parser')
            h1 = soup.find('h1')
            h2 = soup.find('h2')
            if h1:
                textos.append(h1.get_text(separator=' ', strip=True))
            if h2:
                textos.append(h2.get_text(separator=' ', strip=True))
            divs = soup.find_all('div', id=lambda x: x and 'chunk' in x)
            textos.extend([div.get_text(separator=' ', strip=True) for div in divs])

        elif 'agenciabrasil' in website:
            html = requests.get(website, headers=headers).content
            soup = BeautifulSoup(html, 'html.parser')
            h1 = soup.find('h1')
            if h1:
                textos.append(h1.get_text(separator=' ', strip=True))
            divs = soup.find('div', class_='conteudo-noticia')
            textos.extend([div.get_text(separator=' ', strip=True) for div in divs])

        elif 'uol' in website:
            # como o uol bloqueia requests, então optamos por usar selenium
            driver.get(website)
            time.sleep(3)
            page_source = driver.page_source
            soup = BeautifulSoup(page_source, 'html.parser')
            h1 = soup.find('h1', class_='title')
            if h1:
                textos.append(h1.get_text(separator=' ', strip=True))
            # pega todos os textos, incluindo comentários
            divs = soup.find_all('div', attrs={'data-metric-area':'texto-noticia'})
            textos.extend([div.get_text(separator=' ', strip=True) for div in divs])
        
    except Exception as e:
        print(f"Erro ao acessar {website}: {e}")
        driver.back()
        return ""

    driver.back()
    return ' '.join(textos)

if __name__ == '__main__':

    print("Você quer escolher um site ou ler um csv pronto?")
    print("escolher | csv")
    escolha_csv = input().lower()

    if escolha_csv == 'escolher':
        sites = {1:'g1.globo.com', 2:'noticias.uol.com.br', 3:'agenciabrasil.ebc.com.br'}

        termo = input('Digite o termo que quer pesquisar no google: ')

        print('Quer escolher um site ou usar todos?')
        print("escolher | todos")

        escolha = input().lower()

        if escolha == "escolher":
            print('Escolha um dos seguintes sites (digite o id)')
            for id, site in sites.items():
                print(f"{id} -> {site}")
            site_escolhido = sites.get(int(input()))

            print('Digite quantas páginas do google você quer captar')
            pages = int(input())

            google_query = f'site:{site_escolhido} {termo}'
            driver = start_driver()
            websites = extract_websites_from_google_query(google_query, driver, termo, pages)
            print(f'Quantidade de sites: {len(websites)}')
            print(websites)

        else:
            websites = []
            for id, site in sites.items():
                google_query = f'site:{site} {termo}'
                driver = start_driver()
                websites.extend(extract_websites_from_google_query(google_query, driver, termo, pages=5))
            print(f'Quantidade de sites: {len(websites)}')
            print(websites)

        df = pd.DataFrame({'url': websites})
        df['texto'] = df['url'].apply(get_text_from_website, driver=driver)
        df.to_excel(os.path.join(saidas_dir, 'noticias.xlsx'), index=False)
    
    else:
        driver = start_driver()
        df = pd.read_csv(glob(os.getcwd() + '/url.csv')[0])
        df['texto'] = df['url'].apply(get_text_from_website, driver=driver)
        df.to_excel(os.path.join(saidas_dir, 'noticias.xlsx'), index=False)
