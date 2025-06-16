import os
from src.utils import Utils
from src.mono.service import Mono
from src.vigenere.service import Vigenere
from src.hill.service import Hill

if __name__ == "__main__":
    texto_conhecido = Utils.parse("texto/avesso_da_pele.txt")
    
    # Mono
    for arquivo in os.listdir("cifrado/mono/"):
        if arquivo.endswith("texto_cifrado.txt"):
            texto_cifrado = Utils.parse("cifrado/mono/" + arquivo)
            Mono.decriptar_forca_bruta(texto_cifrado, texto_conhecido)

    # Vigenere
    for arquivo in os.listdir("cifrado/vigenere/"):
        if arquivo.endswith("texto_cifrado.txt"):
            texto_cifrado = Utils.parse("cifrado/vigenere/" + arquivo)
            tamanho_chave = int(arquivo.split('_')[1])
            print(f"Analisando o arquivo: {arquivo}, tamanho da chave: {tamanho_chave}")
            resultado = Vigenere.decriptar_forca_bruta(texto_cifrado, texto_conhecido, tamanho_chave)

    # Hill
    for arquivo in os.listdir("cifrado/hill/"):
        if arquivo.endswith("texto_cifrado.txt"):
            conteudo = Utils.parse("cifrado/hill/" + arquivo)
            tamanho_chave = int(arquivo.split('_')[1])
            print(f"Analisando o arquivo: {arquivo}, tamanho da chave: {tamanho_chave}")
            resultado = Hill.decriptar_forca_bruta(conteudo, texto_conhecido, tamanho_chave)