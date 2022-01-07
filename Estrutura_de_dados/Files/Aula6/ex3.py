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


def media(pilha):
    lista_aux = []

    while len(pilha) > 0:
        lista_aux.append(pilha.topo())
        pilha.remove()
    
    for i in reversed(lista_aux):
        pilha.insere(i)
        
    soma = sum(lista_aux)
    media = soma / len(lista_aux)
    return media

p1 = pilha()
p1.insere(10)
p1.insere(9.5)
p1.insere(7)

print(media(p1))