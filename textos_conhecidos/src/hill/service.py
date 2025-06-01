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
        pass

    @staticmethod
    def encontra_possivel_chave(matriz_trecho: np.ndarray, matriz_cifrado: np.ndarray):
        """Encontra a possível chave da cifra de Hill dado um trecho de texto plano e cifrado."""
        if matriz_trecho.shape != matriz_cifrado.shape:
            raise ValueError("As matrizes devem ter as mesmas dimensões.")

        matriz_inversa = Hill.calcula_matriz_inversa(matriz_trecho)
        if matriz_inversa is None:
            return None  # Não é possível calcular a inversa

        chave = (matriz_cifrado @ matriz_inversa) % 26
        return chave.astype(int)


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


"""# Exemplo de uso
matriz_cifrada = np.array([[4, 23], [19, 21]])
matriz_cifrada = np.array([[11, 14], [11, 19]])
matriz_inversa = Hill.calcula_matriz_inversa(matriz_cifrada)
print(f"Matriz Inversa: {matriz_inversa}")
chave = (matriz_cifrada @ matriz_inversa) % 26
print(f"chave {chave}")
print("----------------")


import numpy as np
from sympy import Matrix

# Função para converter letras para números
def letras_para_numeros(texto):
    return [ord(c) - ord('A') for c in texto]

# Entradas
texto_claro = "LLOT"
texto_cifrado = "ETXV"

# Conversão
P1 = letras_para_numeros(texto_claro[:2])  # LL
P2 = letras_para_numeros(texto_claro[2:])  # OT

C1 = letras_para_numeros(texto_cifrado[:2])  # ET
C2 = letras_para_numeros(texto_cifrado[2:])  # XV

# Matrizes
P = np.array([[P1[0], P2[0]], [P1[1], P2[1]]])  # Texto claro
C = np.array([[C1[0], C2[0]], [C1[1], C2[1]]])  # Texto cifrado

# Inversa modular de P
P_sym = Matrix(P)
P_inv_mod26 = P_sym.inv_mod(26)
P_inv = np.array(P_inv_mod26).astype(int)

# Calculando a chave
K = (C @ P_inv) % 26

# Verificação
C_verificacao = (K @ P) % 26

# Exibindo resultados
print("Matriz do texto claro (P):")
print(P)
print("\nMatriz do texto cifrado (C):")
print(C)
print("\nInversa modular de P (mod 26):")
print(P_inv)
print("\nMatriz-chave K:")
print(K)
print("\nVerificação (K @ P % 26):")
print(C_verificacao)
"""

