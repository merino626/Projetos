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


def maximo(pilha):
    lista_aux = []
    while len(pilha) > 0:
        lista_aux.append(pilha.topo())
        pilha.remove()
    for i in reversed(lista_aux):
        pilha.insere(i)     

    return max(lista_aux)

p1 = pilha()
p1.insere(10)
p1.insere(40)
p1.insere(30)
print(maximo(p1))