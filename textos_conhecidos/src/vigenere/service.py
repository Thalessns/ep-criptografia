import string
import numpy as np

from textos_conhecidos.src.utils import Utils


class Vigenere():

    @staticmethod
    def encriptar(conteudo: str, tamanho: int, grupo: str, k: int):
        n = len(conteudo)-tamanho+1

        r = np.random.randint(0, n)
        texto_aberto = conteudo[r:r+tamanho]

        key = np.random.randint(0, 26, (k))
        while key.size < tamanho:
            key = np.concatenate((key,key))
            
        key = key[0:tamanho]

        az = string.ascii_lowercase
        alf2dec = {az[i] : i for i in range(26)}
        dec2alf = {i : az[i] for i in range(26)}

        texto_numerico = [alf2dec[i] for i in texto_aberto]
        texto_cifrado = ( np.array(texto_numerico) + key ) % 26
        texto_cifrado = [dec2alf[i] for i in texto_cifrado]

        key_texto = [dec2alf[i] for i in key]

        Utils.salvar_arquivo('cifrado/vigenere/' + grupo + '_' + str(k) + '_' +  'texto_cifrado_teste.txt',''.join(texto_cifrado))
        Utils.salvar_arquivo('aberto/vigenere/' + grupo + '_' + str(k) + '_' +  'key.txt',''.join(key_texto))
        Utils.salvar_arquivo('aberto/vigenere/' + grupo + '_' + str(k) + '_' +  'texto_aberto.txt',''.join(texto_aberto))

    @staticmethod
    def decript(texto_cifrado: str, chave: str):
        tamanho = len(texto_cifrado)
        
        # Converte a chave de texto para valores numéricos
        az = string.ascii_lowercase
        alf2dec = {az[i]: i for i in range(26)}
        dec2alf = {i: az[i] for i in range(26)}
        
        # Converte a chave e o texto cifrado para valores numéricos
        chave_numerica = [alf2dec[i] for i in chave]
        texto_cifrado_numerico = [alf2dec[i] for i in texto_cifrado]
        
        # Aplica a descriptografia (subtração módulo 26)
        texto_aberto_numerico = (np.array(texto_cifrado_numerico) - np.array(chave_numerica)) % 26
        texto_aberto = [dec2alf[i] for i in texto_aberto_numerico]
        
        return ''.join(texto_aberto)