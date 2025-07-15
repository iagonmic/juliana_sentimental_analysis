import spacy
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud

nlp = spacy.load("pt_core_news_sm")

def lematizar_texto(texto: str) -> str:
    doc = nlp(texto)
    return ' '.join([token.lemma_ for token in doc if not token.is_stop])

def lematizar_e_printar(df: pd.DataFrame, coluna: str = 'clean_text') -> pd.DataFrame:
    print("\nTextos Lematizados:\n")
    df = df.dropna(subset=[coluna]).copy()
    df['processed_text'] = df[coluna].apply(lematizar_texto)

    for i, texto in enumerate(df['processed_text'], start=1):
        print(f"[{i}] {texto}")
        print("-" * 40)

    return df

def gerar_nuvem_palavras(df: pd.DataFrame, coluna: str = 'processed_text', salvar: bool = False, caminho: str = "nuvem_palavras.png"):
    print("\nGerando nuvem de palavras em alta resolução...")

    texto_completo = ' '.join(df[coluna].dropna())

    wordcloud = WordCloud(
        width=1920,
        height=1080,
        background_color='white',
        max_words=200,
        colormap='viridis'
    ).generate(texto_completo)

    plt.figure(figsize=(16, 8))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.title("Nuvem de Palavras em Alta Resolução", fontsize=18)

    if salvar:
        plt.savefig(caminho, dpi=400, bbox_inches='tight')
        print(f"Nuvem de palavras salva em: {caminho}")

    plt.show()

