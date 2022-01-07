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

def printa_elementos(fila):
    for i in range(len(fila)):
        print(fila.proximo())
        fila.remove()

def transfere_elementos(fila_a, fila_b):
    for i in range(len(fila_a)):
        fila_b.insere(fila_a.proximo())
        fila_a.remove()


fila_a = Fila()
fila_a.insere(1)
fila_a.insere(10)
fila_a.insere(20)

fila_b = Fila()


transfere_elementos(fila_a, fila_b)
printa_elementos(fila_b)
printa_elementos(fila_a)