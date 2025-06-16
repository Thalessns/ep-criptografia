import math
import string
import random
import numpy as np
from numpy.linalg import inv
from textos_conhecidos.src.utils import Utils


class Hill():

    @staticmethod
    def encriptar(conteudo: str, tamanho: int, grupo: str, k: int):
        n = len(conteudo) - tamanho + 1
        r = np.random.randint(0, n)
        texto_aberto = conteudo[r:r + tamanho]

        az = string.ascii_lowercase
        alf2dec = {az[i]: i for i in range(26)}
        dec2alf = {i: az[i] for i in range(26)}

        while True:
            # Gera uma matriz triangular superior
            # key = [[0] * k for _ in range(k)]
            key = np.zeros((k, k))
            for i in range(k):
                for j in range(i, k):
                    if i == j:
                        # Garante que os elementos da diagonal sejam coprimos com 26
                        while True:
                            element = random.randint(1, 25)
                            if math.gcd(element, 26) == 1:
                                key[i][j] = element
                                break
                    else:
                        key[i][j] = random.randint(0, 25)

            # Calcula o determinante
            det = int(round(np.linalg.det(key)))

            # Verifica se o determinante é coprimo com 26
            if math.gcd(det, 26) == 1:
                break
            else:
                print('bug')

        texto_numerico = [alf2dec[i] for i in texto_aberto]
        texto_cifrado = np.array(texto_numerico).reshape((int(tamanho / k), k)).T
        texto_cifrado = key @ texto_cifrado % 26
        texto_cifrado = texto_cifrado.T.reshape(tamanho)
        texto_cifrado = [dec2alf[i] for i in texto_cifrado]

        Utils.salvar_arquivo('cifrado/hill/' + grupo + '_' + str(k) + '_' + 'texto_cifrado.txt', ''.join(texto_cifrado))
        Utils.salvar_arquivo('aberto/hill/' + grupo + '_' + str(k) + '_' + 'key.txt', np.array2string(key))
        Utils.salvar_arquivo('aberto/hill/' + grupo + '_' + str(k) + '_' + 'texto_aberto.txt', ''.join(texto_aberto))

    @staticmethod
    def decriptar_forca_bruta(texto_cifrado: str, texto_base: str, k: int):
        """Testa um trecho de tamanho igual ao texto cifrado em todas as posições do texto base.
        Para cada trecho, quebra em blocos de tamanho k * k (mínimo possível para uma chave única).
        Tenta inverter essa matriz do trecho aberto (talvez não seja possível, quanto maior o texto,
        mais provavel algum bloco ser invertível).
         Utiliza K = C * P^-1 mod 26 para descobrir uma chave possível.
         Se a chave criptografar o trecho aberto e gerar o texto cifrado, retorna a chave"""
        tamanho_trecho = len(texto_cifrado)

        for pos in range(len(texto_base) - tamanho_trecho + 1):
            trecho_aberto = texto_base[pos:pos + tamanho_trecho]
            for i in range(0, tamanho_trecho, k):
                if i + k * k > tamanho_trecho:
                    continue
                trecho_aberto_teste = trecho_aberto[i:i + k * k]
                texto_cifrado_teste = texto_cifrado[i:i + k * k]
                matriz_chave = Hill.encontra_possivel_chave(texto_cifrado_teste, trecho_aberto_teste, k)
                if matriz_chave is not None:
                    if Hill.encripta_chave_escolhida(trecho_aberto, matriz_chave, k) == texto_cifrado:
                        print(
                            f"Na posição {pos} encontramos o trecho '{trecho_aberto}' que foi criptografado com a chave:")
                        print(matriz_chave)
                        Utils.salvar_arquivo('aberto/hill/Grupo_13_' + str(k) + '_' + 'key.txt', str(matriz_chave))
                        Utils.salvar_arquivo('aberto/hill/Grupo_13_' + str(k) + '_' + 'texto_aberto.txt', trecho_aberto)
                        return None

        return None

    @staticmethod
    def encontra_possivel_chave(texto_cifrado: str, trecho_aberto: str, k: int) -> np.ndarray or None:
        """ Tenta inverter a matriz do texto aberto para encontrar uma chave possível"""

        matriz_cifrado = Hill.monta_matriz(Hill.convert_letter_to_number(texto_cifrado), k)
        matriz_aberto = Hill.monta_matriz(Hill.convert_letter_to_number(trecho_aberto), k)

        matriz_inversa_aberto = Hill.calcula_matriz_inversa(matriz_aberto)
        if matriz_inversa_aberto is None:
            return None  # Não é possível calcular a inversa

        matriz_chave = (matriz_cifrado @ matriz_inversa_aberto) % 26
        return matriz_chave

    @staticmethod
    def encripta_chave_escolhida(conteudo: str, chave: np.ndarray, k: int) -> str:
        """ Encripta o conteúdo usando a chave fornecida"""
        az = string.ascii_lowercase
        alf2dec = {az[i]: i for i in range(26)}
        dec2alf = {i: az[i] for i in range(26)}

        texto_numerico = Hill.convert_letter_to_number(conteudo)
        tamanho = len(texto_numerico)

        if tamanho % k != 0:
            raise ValueError("O tamanho do texto deve ser múltiplo de k.")

        texto_cifrado = np.array(texto_numerico).reshape((int(tamanho / k), k)).T
        texto_cifrado = chave @ texto_cifrado % 26
        texto_cifrado = texto_cifrado.T.reshape(tamanho)
        texto_cifrado = [dec2alf[i] for i in texto_cifrado]

        return ''.join(texto_cifrado)

    @staticmethod
    def monta_matriz(numeros: list, k: int):
        """ Monta uma matriz a partir de uma lista de números, dividindo-os em blocos de tamanho k"""
        tamanho = len(numeros)
        if tamanho % k != 0:
            raise ValueError("O tamanho do texto deve ser múltiplo de k.")
        matriz = np.array(numeros).reshape((int(tamanho / k), k)).T
        return matriz

    @staticmethod
    def convert_letter_to_number(texto: str) -> list:
        return [ord(char) - ord('a') for char in texto]

    @staticmethod
    def convert_number_to_letter(numeros: list) -> str:
        return ''.join([chr(num + ord('a')) for num in numeros])

    @staticmethod
    def calcula_matriz_inversa(matriz: np.ndarray, modulo: int = 26):
        det = int(round(np.linalg.det(matriz)))
        inv_det = Utils.inv_multiplicativo(det, modulo)

        if inv_det == 0:
            return None  # Não é possível calcular a inversa

        matriz_adjunta = Hill.calcula_matriz_adjunta(matriz)
        matriz_inversa = (inv_det * matriz_adjunta) % modulo
        return matriz_inversa.astype(int)

    @staticmethod
    def calcula_matriz_adjunta(matriz: np.ndarray):
        if matriz.shape[0] != matriz.shape[1]:
            raise ValueError("Matriz deve ser quadrada.")
        n = matriz.shape[0]
        matriz_adjunta = np.zeros((n, n), dtype=int)
        for i in range(n):
            for j in range(n):
                submatriz = np.delete(np.delete(matriz, i, axis=0), j, axis=1)  # Remove a linha i e a coluna j
                xij = ((-1) ** (i + j)) * int(round(np.linalg.det(submatriz)))  # Calcula o determinante da submatriz
                matriz_adjunta[j][i] = xij

        return matriz_adjunta
