import string
import numpy as np
from src.utils import Utils


class Mono():

    @staticmethod
    def encriptar(conteudo: str, tamanho: int, grupo: str):
        n = len(conteudo) - tamanho + 1
        r = np.random.randint(0, n)
        texto_aberto = conteudo[r:r+tamanho]

        az = string.ascii_lowercase

        key = np.random.permutation(26)
        key = ''.join([az[key[i]] for i in range(26)])

        key_enc = {az[i] : key[i] for i in range(26)}
        key_dec = {key[i] : az[i] for i in range(26)}

        texto_cifrado = [key_enc[i] for i in texto_aberto]

        # texto_aberto = [key_dec[i] for i in texto_cifrado]

        Utils.salvar_arquivo('cifrado/mono/' + grupo + '_' + 'texto_cifrado.txt',''.join(texto_cifrado))
        Utils.salvar_arquivo('aberto/mono/' + grupo + '_' + 'key.txt',key)
        Utils.salvar_arquivo('aberto/mono/' + grupo + '_' + 'texto_aberto.txt',''.join(texto_aberto))

    @staticmethod
    def decript(conteudo_crifrado: str, chave: str):
        az = string.ascii_lowercase  
        key_dec = {chave[i]: az[i] for i in range(26)}
        texto_aberto = [key_dec[c] for c in conteudo_crifrado]
        return ''.join(texto_aberto)
