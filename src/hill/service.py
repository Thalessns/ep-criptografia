import math
import string
import random
import numpy as np

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
