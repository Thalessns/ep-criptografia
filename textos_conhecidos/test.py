from src.utils import Utils
from src.mono.service import Mono
from src.vigenere.service import Vigenere
from src.hill.service import Hill

if __name__ == "__main__":
    
    # Mono
    """texto_cifrado = Utils.parse("cifrado/mono/teste_texto_cifrado.txt")
    texto_aberto = Utils.parse("texto/avesso_da_pele.txt")
    Mono.decriptar_forca_bruta(texto_cifrado, texto_aberto)"""

    # Vigenere
    arquivo = Utils.sortear_arquivo_txt("cifrado/vigenere/")
    conteudo = Utils.parse("cifrado/vigenere/" + arquivo)
    tamanho_chave = int(arquivo[8:10])
    print(f"Analisando o arquivo: {arquivo}, tamanho da chave: {tamanho_chave}")
    resultado = Vigenere.decriptar_forca_bruta(conteudo, Utils.parse("texto/avesso_da_pele.txt"), tamanho_chave)


    # Hill
    """conteudo = Utils.parse("cifrado/hill/Grupo13_5_texto_cifrado_teste.txt")
    chave = Utils.carregar_matriz("aberto/hill/Grupo13_5_key.txt")
    resultado = Hill.decript(conteudo, chave)
    print(resultado)"""