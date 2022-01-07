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


def eh_igual(pilha1, pilha2):
    while len(pilha1) > 0:
        n1 = pilha1.remove()
        n2 = pilha2.remove()
        if n1 != n2:
            return 'Não são iguais'
    return 'São iguais'
        

p1 = pilha()
p2 = pilha()
p1.insere(1)
p1.insere(2)
p2.insere(5)
p2.insere(2)
print(eh_igual(p1,p2))