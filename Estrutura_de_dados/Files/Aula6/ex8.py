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


def Tpilha(vetor):
    for i in vetor:
        if i % 2 == 0:
            p1.insere(i)
        else: 
            p1.remove()
    while len(p1) > 0:
        print(p1.remove())

vetor = [2, 4, 6, 8, 9]
p1 = pilha()
Tpilha(vetor)