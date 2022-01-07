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

def retira_primeiro_elemento(fila_a):
    elemento = fila_a.proximo()
    fila_a.remove()
    fila_a.insere(elemento)


fila_a = Fila()
fila_a.insere(1)
fila_a.insere(2)
fila_a.insere(3)
fila_a.insere(4)


retira_primeiro_elemento(fila_a)
printa_elementos(fila_a)



