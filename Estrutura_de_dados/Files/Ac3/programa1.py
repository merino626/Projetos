from collections import deque
class Fila:
  def __init__(self):
       self.itens = deque()
  def insere(self, e):
       self.itens.append(e)
  def remove(self):
       return self.itens.popleft()
  def __len__(self):
       return len(self.itens)
  def proximo(self):
       prox = self.itens.popleft()
       self.itens.appendleft(prox)
       return prox
class Pilha:
	def __init__(self):
		self.__itens = []
		self.__tamanho = 0
	def insere(self, e):
		self.__itens.append(e)
		self.__tamanho += 1
	def remove(self):
		self.__tamanho -= 1
		return self.__itens.pop()
	def topo(self):
		return self.__itens[-1]
	def __len__(self):
		return self.__tamanho


def retorna_min_impar(p1, f1):
    if len(p1) == 0 or len(f1) == 0:
        return 'A pilha e a fila precisam ter no minimo um valor'
    ### Pegando menor impar da fila ###
    flag = 0
    min_fila = -1
    while len(f1) != 0:
        valor = f1.remove()
        if (valor % 2 != 0) and flag == 0:
            min_fila = valor
            flag = 1
        if valor % 2 != 0:
            impar = valor
            if impar < min_fila:
                min_fila = impar
    ### Pegando menor impar da pilha ###
    flag = 0
    min_pilha = -1
    while len(p1) != 0:
        valor = p1.remove()
        if (valor % 2 != 0) and flag == 0:
            min_pilha = valor
            flag = 1
        if valor % 2 != 0:
            impar = valor
            if impar < min_pilha:
                min_pilha = impar
    ### Retornando o menor considerando a fila e pilha ###
    if min_pilha != -1 and min_fila != -1:
        if min_fila < min_pilha:
            return min_fila
        return min_pilha  
    elif min_fila == -1:
        return min_pilha
    else: return min_fila
## Criando a pilha e a fila
f1 = Fila()
p1 = Pilha()
### Inserindo meu RA misturado na pilha e na fila (1903593)
f1.insere(1); f1.insere(9); f1.insere(0); f1.insere(3)
p1.insere(5); p1.insere(9); p1.insere(3)
###Chamando função e printando resultado
print(retorna_min_impar(p1, f1)) # <- Resultado esperado: 1
### Obs: Se retornar -1 é porque não há nenhum impar nem na pilha e nem na fila
### (A função foi feita considerando apenas números positivos).
### A fila e a pilha precisam ter ao menos 1 valor cada para poderem entrar na função.
### Este documento contém o código da função, código do programa e os resultados da execução.