from src.utils import Utils
from src.mono.service import Mono
from src.vigenere.service import Vigenere
from src.hill.service import Hill

if __name__ == "__main__":
    
    # Mono
    """conteudo = Utils.parse("cifrado/mono/Grupo13_texto_cifrado_teste.txt")
    chave = Utils.parse("aberto/mono/Grupo13_key.txt")
    resultado = Mono.decript(conteudo, chave)
    print(resultado)"""

    # Vigenere
    """conteudo = Utils.parse("cifrado/vigenere/Grupo13_20_texto_cifrado_teste.txt")
    chave = Utils.parse("aberto/vigenere/Grupo13_20_key.txt")
    resultado = Vigenere.decript(conteudo, chave)
    print(resultado)"""

    # Hill
    conteudo = Utils.parse("cifrado/hill/Grupo13_5_texto_cifrado_teste.txt")
    chave = Utils.carregar_matriz("aberto/hill/Grupo13_5_key.txt")
    resultado = Hill.decript(conteudo, chave)
    print(resultado)