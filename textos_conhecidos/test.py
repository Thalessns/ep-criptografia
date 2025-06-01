from src.utils import Utils
from src.mono.service import Mono
from src.vigenere.service import Vigenere
from src.hill.service import Hill

if __name__ == "__main__":
    
    # Mono
    texto_cifrado = Utils.parse("cifrado/mono/teste_texto_cifrado.txt")
    texto_aberto = Utils.parse("texto/avesso_da_pele.txt")
    Mono.decript_brute_force(texto_cifrado, texto_aberto)

    # Vigenere
    """conteudo = Utils.parse("cifrado/vigenere/Grupo13_20_texto_cifrado_teste.txt")
    chave = Utils.parse("aberto/vigenere/Grupo13_20_key.txt")
    resultado = Vigenere.decript(conteudo, chave)
    print(resultado)"""

    # Hill
    """conteudo = Utils.parse("cifrado/hill/Grupo13_5_texto_cifrado_teste.txt")
    chave = Utils.carregar_matriz("aberto/hill/Grupo13_5_key.txt")
    resultado = Hill.decript(conteudo, chave)
    print(resultado)"""