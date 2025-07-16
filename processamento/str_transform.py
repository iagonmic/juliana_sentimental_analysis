import pandas as pd
import re

def carregar_dados(caminho_arquivo: str) -> pd.DataFrame:
    try:
        df = pd.read_excel(caminho_arquivo)
        print(f"\nDados carregados: {len(df)} linhas.\n")
        return df
    except Exception as e:
        print(f"Erro ao carregar dados: {e}")
        return pd.DataFrame()

def printar_textos_brutos(df: pd.DataFrame, coluna: str = 'texto'):
    print("\nTextos Brutos:\n")
    for i, texto in enumerate(df[coluna].dropna(), start=1):
        print(f"[{i}] {texto}")
        print("-" * 40)

def limpar_texto(texto: str) -> str:
    texto = re.sub(r"http\S+|www\.\S+", "", texto)
    texto = re.sub(r"[^\w\s,.!?]", "", texto)
    texto = re.sub(r"\s+", " ", texto).strip()
    return texto

def limpar_e_printar_textos(df: pd.DataFrame, coluna: str = 'texto') -> pd.DataFrame:
    print("\nTextos Limpos:\n")
    df = df.dropna(subset=[coluna]).copy()
    df['clean_text'] = df[coluna].apply(limpar_texto)

    for i, texto in enumerate(df['clean_text'], start=1):
        print(f"[{i}] {texto}")
        print("-" * 40)

    return df
