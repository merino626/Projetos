from collections import deque

class Fila:
  def __init__(self):
       self.__itens = deque()
  def insere(self, e):
       self.__itens.append(e)
  def remove(self):
       return self.__itens.popleft()
  def __len__(self):
       return len(self.__itens)
  def proximo(self):
       prox = self.__itens.popleft()
       self.__itens.appendleft(prox)
       return prox


class Pilha():
    def __init__(self):
        self.itens = []
        self.tamanho = 0

    def insere(self, elemento):
        self.itens.append(elemento)
        self.tamanho += 1

    def remove(self):
        self.tamanho -= 1
        return self.itens.pop()
    
    def topo(self):
        return self.itens[-1]

    def __len__(self):
        return self.tamanho


def printa_elementos(fila):
    for i in range(len(fila)):
        print(fila.proximo())
        fila.remove()


Fpar = Fila()
Fimpar = Fila()
pilha = Pilha

entrada = ''
while entrada != 0:
    if entrada == 0:
        break

    entrada = int(input('Digite um número'))
    if entrada % 2 == 0:
        Fpar.insere(entrada)
    else:
        Fimpar.insere(entrada)


while len(Fimpar) != 0:
    valor_impar = Fimpar.remove()
    if valor_impar > 0:
        pilha.insere(valor_impar)
    else:
        if len(pilha) <= 0:
            break
        pilha.remove()

while len(Fpar) != 0:
    valor_par = Fpar.remove()
    if valor_par > 0:
        pilha.insere(valor_par)
    else:
        if len(pilha) <= 0:
            break
        pilha.remove()

