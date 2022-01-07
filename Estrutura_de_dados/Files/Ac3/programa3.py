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


def ordem_crescente(p1):
    if len(p1) == 0:
        return 'A pilha precisa ter no minimo um valor'
    ### Verificando se os impares da pilha estão em ordem crescente ###
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
                return False
    if min_pilha == -1:
        return 'Não há impares na pilha'
    return True

### Criando a pilha ###
pilha_a = Pilha()

### Inserindo meu RA na pilha (1903593)
pilha_a.insere(1); pilha_a.insere(9); pilha_a.insere(0); pilha_a.insere(3)
pilha_a.insere(5); pilha_a.insere(9); pilha_a.insere(3) # <- Direção do topo até o final da pilha


print(ordem_crescente(pilha_a)) #<- retorno esperado: False

### obs: se os números olhados a partir da ultima inserção até a primeira inserção estiverem em ordem crescente
### a função retornará True, caso não estejam retornará false.
### Se não houver impares a função informará que não há impares na fila

### Este documento contém o código da função, código do programa e os resultados da execução.