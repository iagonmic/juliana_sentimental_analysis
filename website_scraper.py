import requests
from bs4 import BeautifulSoup
import pandas as pd
# definimos os 4 principais sites que queremos extrair notícias
# g1.globo.com, noticias.uol.com.br, agenciabrasil.ebc.com.br
# pesquisamos no google da seguinte maneira: site:g1.globo.com "Juliana Marins"
# extraimos manualmente 40 urls desses sites, 10 por fonte, sobre o caso e inserimos em um arquivo url.csv com os campos 'fonte' e 'url'

def get_text_from_website(website):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
    }
    html = requests.get(website, headers=headers).content
    soup = BeautifulSoup(html, 'html.parser')
    textos = []

    if 'g1' in website:
        h1 = soup.find_all('h1')[0]
        h2 = soup.find_all('h2')[0]
        textos.append(h1.get_text(separator=' ', strip=True))
        textos.append(h2.get_text(separator=' ', strip=True))

        divs = soup.find_all('div', id=lambda x: x and 'chunk' in x)
        textos.extend([div.get_text(separator=' ', strip=True) for div in divs])

    return ' '.join(textos)

if __name__ == '__main__':
    df = pd.read_csv('C:/Users/iagof/Desktop/Data Science/juliana_sentimental_analysis/url.csv')
    df['texto'] = df['url'].apply(get_text_from_website)