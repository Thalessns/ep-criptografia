import string
import numpy as np
from textos_conhecidos.src.utils import Utils


class Mono():

    @staticmethod
    def encriptar(conteudo: str, tamanho: int, grupo: str):
        n = len(conteudo) - tamanho + 1
        r = np.random.randint(0, n)
        texto_aberto = conteudo[r:r + tamanho]

        az = string.ascii_lowercase

        key = np.random.permutation(26)
        key = ''.join([az[key[i]] for i in range(26)])

        key_enc = {az[i]: key[i] for i in range(26)}
        key_dec = {key[i]: az[i] for i in range(26)}

        texto_cifrado = [key_enc[i] for i in texto_aberto]

        # texto_aberto = [key_dec[i] for i in texto_cifrado]

        Utils.salvar_arquivo('cifrado/mono/' + grupo + '_' + 'texto_cifrado.txt', ''.join(texto_cifrado))
        Utils.salvar_arquivo('aberto/mono/' + grupo + '_' + 'key.txt', key)
        Utils.salvar_arquivo('aberto/mono/' + grupo + '_' + 'texto_aberto.txt', ''.join(texto_aberto))

    @staticmethod
    def decript_brute_force(conteudo_crifrado: str, texto_base: str):
        """
        faz loop por todas as possibilidades do texto base e tenta achar um mapeamento que daria certo,
        se houver apenas 1 mapeamento, retorna a mensagem original e a chave
        """
        tamanho = len(conteudo_crifrado)
        chaves_possiveis = []

        for pos_texto in range(len(texto_base) - tamanho + 1):
            trecho = texto_base[pos_texto:pos_texto + tamanho]
            chave = Mono.find_possible_key(trecho, conteudo_crifrado)
            if chave:
                chave = Mono.find_possible_key(trecho, conteudo_crifrado) ## para debug
                chaves_possiveis.append((pos_texto, trecho, chave))

        if len(chaves_possiveis) == 1:
            print(f"na posição {chaves_possiveis[0][0]} encontramos {chaves_possiveis[0][1]} que foi criptografado com a chave {chaves_possiveis[0][2]}")

    @staticmethod
    def find_possible_key(trecho_texto_conhecido: str, mensagem_cifrada: str):
        chave_criptografia = {}
        chave_decriptografia = {}

        for letra_texto_conhecido, letra_texto_cifrado in zip(trecho_texto_conhecido, mensagem_cifrada):
            if letra_texto_conhecido in chave_criptografia:
                if chave_criptografia[letra_texto_conhecido] != letra_texto_cifrado:
                    return None  # 1 letra do aberto mapeando em duas da cifrada

            elif letra_texto_cifrado in chave_decriptografia:
                return None  # 2 letras do aberto mapeando na mesma da cifrada

            else:
                # letra nova
                chave_criptografia[letra_texto_conhecido] = letra_texto_cifrado
                chave_decriptografia[letra_texto_cifrado] = letra_texto_conhecido

        return chave_criptografia  # só chega aqui se existir um mapeamento 1:1
