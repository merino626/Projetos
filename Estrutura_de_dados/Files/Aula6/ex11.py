class Pilha:
	def __init__(self):
		self.itens = []
		self.tamanho = 0
	def insere(self, e):
		self.itens.append(e)
		self.tamanho += 1
	def remove(self):
		self.tamanho -= 1
		return self.itens.pop()
	def topo(self):
		return self.itens[-1]
	def __len__(self):
		return self.tamanho
def exibe(p):
    while len(p)>0:
        print(p.remove(),end="")

def binario(n):
    p=Pilha()
    while n>0:
        p.insere(n%2)
        n=n//2

    return p

v=[10,15,7,18]
for i in range(len(v)):
    print(v[i], " Convertido para binario é ",end="")
    exibe(binario(v[i]))
    print()

