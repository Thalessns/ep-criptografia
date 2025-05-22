from src.utils import Utils
from src.mono.service import Mono

if __name__ == "__main__":
    
    conteudo = Utils.parse("cifrado/mono/Grupo13_texto_cifrado_teste.txt")
    chave = Utils.parse("aberto/mono/Grupo13_key.txt")
    resultado = Mono.decript(conteudo, chave)
    print(resultado)