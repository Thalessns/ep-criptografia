import math
import string
import random
import numpy as np
from numpy.linalg import inv

from src.utils import Utils


class Hill():

    @staticmethod
    def encriptar(conteudo: str, tamanho: int, grupo: str, k: int):
        n = len(conteudo)-tamanho+1
        r = np.random.randint(0, n)
        texto_aberto = conteudo[r:r+tamanho]

        az = string.ascii_lowercase
        alf2dec = {az[i] : i for i in range(26)}
        dec2alf = {i : az[i] for i in range(26)}

        while True:
        # Gera uma matriz triangular superior
            #key = [[0] * k for _ in range(k)]
            key = np.zeros((k,k))
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
        texto_cifrado = np.array(texto_numerico).reshape((int(tamanho/k),k)).T
        texto_cifrado = key@texto_cifrado % 26
        texto_cifrado = texto_cifrado.T.reshape(tamanho)
        texto_cifrado = [dec2alf[i] for i in texto_cifrado]

        Utils.salvar_arquivo('cifrado/hill/' + grupo + '_' + str(k) + '_' +  'texto_cifrado_teste.txt',''.join(texto_cifrado))
        Utils.salvar_arquivo('aberto/hill/' + grupo + '_' + str(k) + '_' +  'key.txt',np.array2string(key))
        Utils.salvar_arquivo('aberto/hill/' + grupo + '_' + str(k) + '_' +  'texto_aberto.txt',''.join(texto_aberto))

    @staticmethod
    def decript(texto_cifrado: str, chave: np.ndarray):
        # Converte o texto cifrado para valores numéricos
        az = string.ascii_lowercase
        alf2dec = {az[i]: i for i in range(26)}
        dec2alf = {i: az[i] for i in range(26)}
        
        texto_cifrado_numerico = [alf2dec[i] for i in texto_cifrado]
        tamanho = len(texto_cifrado)
        k = chave.shape[0]  # Assume que a chave é uma matriz quadrada
        
        # Calcula a matriz inversa modular
        def mod_inv_matrix(matrix, mod):
            det = int(round(np.linalg.det(matrix)))
            det_inv = pow(det, -1, mod)  # Inverso multiplicativo do determinante
            
            adj = np.round(det * inv(matrix)).astype(int)  # Matriz adjunta
            inv_matrix = (det_inv * adj) % mod
            return inv_matrix
        
        chave_inversa = mod_inv_matrix(chave, 26)
        
        # Processa o texto cifrado
        texto_cifrado_arr = np.array(texto_cifrado_numerico).reshape((int(tamanho/k), k)).T
        texto_aberto = (chave_inversa @ texto_cifrado_arr) % 26
        texto_aberto = texto_aberto.T.reshape(tamanho)
        texto_aberto = [dec2alf[int(i)] for i in texto_aberto]
        
        return ''.join(texto_aberto)