from processamento.str_transform import carregar_dados, printar_textos_brutos, limpar_e_printar_textos
from processamento.analise_nlp import lematizar_e_printar, gerar_nuvem_palavras

def main():
    caminho = ('saidas/dados_coletados.xlsx').strip()
    df = carregar_dados(caminho)

    if df.empty:
        return

    df_limpo = None
    df_processado = None

    while True:
        print("\nMENU:")
        print("1 - Mostrar textos brutos")
        print("2 - Limpar textos (Regex)")
        print("3 - Lematizar textos (spaCy)")
        print("4 - Gerar nuvem de palavras")
        print("0 - Sair")

        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            printar_textos_brutos(df)
        elif opcao == "2":
            df_limpo = limpar_e_printar_textos(df)
        elif opcao == "3":
            if df_limpo is None:
                print("Primeiro limpe os textos (opção 2).")
            else:
                df_processado = lematizar_e_printar(df_limpo)
        elif opcao == "4":
            if df_processado is None:
                print("Primeiro lematize os textos (opção 3).")
            else:
                gerar_nuvem_palavras(df_processado)
        elif opcao == "0":
            print("Encerrando.")
            break
        else:
            print("Opção inválida.")

if __name__ == "__main__":
    main()
