import csv
import os
from itertools import product  # Para gerar combinações

def ler_csv(nome_arquivo, coluna=0):
    """Lê um arquivo CSV e retorna os dados da coluna especificada."""
    with open(nome_arquivo, mode='r', encoding='utf-8') as arquivo:
        leitor = csv.reader(arquivo)
        dados = [linha[coluna] for linha in leitor if len(linha) > coluna]  # Lê apenas a coluna especificada
    return dados

def escrever_csv(nome_arquivo, dados):
    """Escreve os dados em um arquivo CSV, um por linha."""
    with open(nome_arquivo, mode='w', encoding='utf-8', newline='') as arquivo:
        escritor = csv.writer(arquivo)
        for linha in dados:
            escritor.writerow([linha])  # Escreve cada combinação em uma linha

def gerar_combinacoes(nomes, outros_dados):
    """Gera todas as combinações possíveis entre os nomes e os outros dados."""
    combinacoes = []
    for nome in nomes:
        for dado in outros_dados:
            combinacoes.append(f"{nome}{dado}")  # Combina nome + dado
    return combinacoes

def obter_coluna(nome_arquivo):
    """Pergunta ao usuário qual coluna usar no arquivo."""
    with open(nome_arquivo, mode='r', encoding='utf-8') as arquivo:
        leitor = csv.reader(arquivo)
        primeira_linha = next(leitor)  # Lê o cabeçalho ou a primeira linha
        print(f"Arquivo: {nome_arquivo}")
        print(f"Cabeçalho/Primeira linha: {primeira_linha}")
        if len(primeira_linha) > 1:  # Se houver mais de uma coluna
            coluna = input(f"Este arquivo possui {len(primeira_linha)} colunas. Qual coluna deseja usar? (0 a {len(primeira_linha) - 1}): ")
            try:
                coluna = int(coluna)
                if 0 <= coluna < len(primeira_linha):
                    return coluna
                else:
                    print("Número de coluna inválido. Usando a coluna 0 por padrão.")
            except ValueError:
                print("Entrada inválida. Usando a coluna 0 por padrão.")
        return 0  # Usa a primeira coluna por padrão

def main():
    # Perguntar ao usuário o nome do arquivo de nomes
    arquivo_nomes = input("Digite o nome do arquivo CSV com os nomes mais comuns do Brasil: ").strip()

    # Verificar se o arquivo de nomes existe
    if not os.path.exists(arquivo_nomes):
        print(f"Arquivo {arquivo_nomes} não encontrado.")
        return

    # Perguntar ao usuário qual coluna usar no arquivo de nomes
    coluna_nomes = obter_coluna(arquivo_nomes)
    nomes = ler_csv(arquivo_nomes, coluna_nomes)

    # Solicitar ao usuário que escolha outros arquivos
    arquivos_usuario = input("Digite os nomes dos arquivos CSV para combinar (separados por vírgula): ").split(',')

    # Ler os dados dos arquivos escolhidos pelo usuário
    outros_dados = []
    for arquivo in arquivos_usuario:
        arquivo = arquivo.strip()
        if os.path.exists(arquivo):
            coluna = obter_coluna(arquivo)
            dados = ler_csv(arquivo, coluna)
            outros_dados.extend(dados)  # Adiciona os dados à lista
        else:
            print(f"Arquivo {arquivo} não encontrado.")

    # Gerar todas as combinações possíveis
    combinacoes = gerar_combinacoes(nomes, outros_dados)

    # Escrever as combinações em um novo arquivo CSV
    nome_arquivo_saida = input("Digite o nome do arquivo de saída (ex: dicionario.csv): ").strip()
    escrever_csv(nome_arquivo_saida, combinacoes)
    print(f"Foram geradas {len(combinacoes)} combinações e salvas em '{nome_arquivo_saida}'.")

main()
