from math import sqrt
class Ponto:
    def __init__(self):
        self.x = 1
        self.y = 2

    def distancia(self, p):
        hipotenusa = (sqrt(self.x)) + (sqrt(p.x))
        return hipotenusa

    def translsadara(self, dx, dy):
        pass

z = Ponto()

'''
Na minha visão o TAD é um modo de submeter dados a certas regras que compõem uma estrutura de dados,
ou seja, aplicar um modo que os dados se comportem da forma desejada, usando estruturas existentes
na linguagem para conseguir satisfazer as regras.

Os dados são as informações que passarão a ser "regidas" pelas regras da estruturas do TAD

As operações são as manipulações dos dados dentro do TAD, de acordo com as regras permitidas.

Tentei responder de acordo com o que eu entendi, após a correção olharei os slides de Tad
'''