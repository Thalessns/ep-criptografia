import os
import re
import random
import numpy as np
from unidecode import unidecode
from typing import List

class Utils:

    @staticmethod
    def sortear_arquivo_txt(diretorio: str):
        arquivos = os.listdir(diretorio)
        arquivos_txt = [arquivo for arquivo in arquivos if arquivo.endswith('.txt')]

        if not arquivos_txt:
            return "Nenhum arquivo .txt encontrado no diretório."

        arquivo_sorteado = random.choice(arquivos_txt)
        return arquivo_sorteado

    @staticmethod
    def carregar_matriz(diretorio: str):
        with open(diretorio, "r") as f:
            lines = f.readlines()
        
        # Processa cada linha removendo colchetes e espaços
        matrix = []
        for line in lines:
            if line.strip().startswith("["):
                # Remove colchetes e divide por espaços
                clean_line = line.replace("[", "").replace("]", "").strip()
                # Filtra elementos vazios e converte para float
                row = [float(x) for x in clean_line.split() if x]
                matrix.append(row)
        
        return np.array(matrix, dtype=int)

    @staticmethod
    def parse(nome_arquivo: str):
        # abre o arquivo para leitura
        with open(nome_arquivo, 'r', encoding="iso-8859-1") as arquivo_entrada:
            # lê o conteúdo do arquivo
            conteudo = arquivo_entrada.read()
        # transforma as letras em minúsculas
        conteudo = conteudo.lower()
        # remove os acentos das vogais
        conteudo = unidecode(conteudo)
        # remove todos os caracteres que não são letras
        conteudo = re.sub(r'[^a-z]', '', conteudo)
        return conteudo

    @staticmethod
    def salvar_arquivo(nome_arquivo: str, conteudo: str):
        # abre um novo arquivo para escrita
        with open(nome_arquivo, 'w') as arquivo_saida:
            # escreve o conteúdo no arquivo
            arquivo_saida.write(conteudo)

    @staticmethod
    def inv_multiplicativo(b: int, m: int):
        A = np.array([1, 0, m])
        B = np.array([0, 1, b])
        
        while True:
            if B[2] == 0:
                return 0

            if B[2] == 1:
                return B[1] % m 

            Q = np.floor( A[2]/B[2] )
            T = A - Q*B
            A = B
            B = T
