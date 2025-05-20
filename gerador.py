from src.utils import Utils
from src.mono.service import Mono
from src.hill.service import Hill
from src.vigenere.service import Vigenere


def gerador():
	grupo = 'Grupo13'
	diretorio = 'texto/teste.txt'
	
	conteudo = Utils.parse(diretorio)

	Mono.encriptar(conteudo, 10, grupo)
	Hill.encriptar(conteudo, 10, grupo, 5)
	Vigenere.encriptar(conteudo, 10, grupo, 20)


if __name__ == "__main__":
    gerador()
