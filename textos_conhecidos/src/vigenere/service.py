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
    def decriptar_forca_bruta(conteudo_cifrado: str, texto_base: str, tamanho_chave: int):
        tamanho = len(conteudo_cifrado)
        for i in range(len(texto_base) - tamanho + 1):
            trecho = texto_base[i:i+tamanho]
            chave = Vigenere.encontra_possivel_chave(trecho, conteudo_cifrado, tamanho_chave)
            if chave:
                print(f"Na posição {i} encontramos '{trecho}' que foi criptografado com a chave '{chave}'")
                Utils.salvar_arquivo('aberto/vigenere/Grupo_13_' + str(tamanho_chave) + '_' + 'key.txt', chave)
                Utils.salvar_arquivo('aberto/vigenere/Grupo_13_' + str(tamanho_chave) + '_' + 'texto_aberto.txt', trecho)
                return

    @staticmethod
    def encontra_possivel_chave(trecho_texto_conhecido: str, mensagem_cifrada: str, tamanho_chave: int):
        """Cria uma chave de tamanho `tamanho_chave` a partir de um trecho de texto conhecido e uma mensagem cifrada,
         tenta cifrar o trecho conhecido com a chave gerada.
        Se a cifra for igual à mensagem cifrada, retorna a chave."""

        possivel_chave = ""

        for letra_texto_conhecido, letra_texto_cifrado in zip(trecho_texto_conhecido, mensagem_cifrada):
            if len(possivel_chave) == tamanho_chave:
                break
            distancia = (ord(letra_texto_cifrado) - ord(letra_texto_conhecido) + 26) % 26
            possivel_chave += chr(ord('a') + distancia)

        while len(possivel_chave) < len(mensagem_cifrada):
            possivel_chave += possivel_chave

        chave_completa = possivel_chave[:len(mensagem_cifrada)]
        if Vigenere.encripta_chave_escolhida(trecho_texto_conhecido, chave_completa) == mensagem_cifrada:
            return chave_completa

        return None

    @staticmethod
    def encripta_chave_escolhida(conteudo: str, chave: str):

        az = string.ascii_lowercase
        alf2dec = {az[i]: i for i in range(26)}
        dec2alf = {i: az[i] for i in range(26)}

        texto_numerico = [alf2dec[i] for i in conteudo]
        chave_int = [alf2dec[i] for i in chave]
        texto_cifrado = (np.array(texto_numerico) + chave_int) % 26
        texto_cifrado = [dec2alf[i] for i in texto_cifrado]
        return ''.join(texto_cifrado)

