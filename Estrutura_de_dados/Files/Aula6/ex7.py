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

def preenche(pilha, vetor):
    for i in range(len(vetor)):
        pilha.insere(vetor[i])


p1 = pilha()
vetor = [1,2,3,4,5,6,7,8]
preenche(p1, vetor)
print(p1.topo())