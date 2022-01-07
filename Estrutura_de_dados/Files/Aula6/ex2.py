class pilha():
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


def transfere(pilha1, pilha2):
    lista_aux = []

    while len(pilha1) > 0:
        lista_aux.append(pilha1.topo())
        pilha1.remove()
    
    for i in reversed(lista_aux):
        pilha1.insere(i)
        pilha2.insere(i)
    

p1 = pilha()
p1.insere(1)
p1.insere(2)

p2 = pilha()
transfere(p1, p2)
print(p2.topo())
print(p1.topo())