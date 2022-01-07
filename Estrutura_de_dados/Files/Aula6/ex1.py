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

                
def all_elements(objeto):
    lista_aux = []

    while len(objeto) > 0:
        lista_aux.append(objeto.topo())
        print(objeto.remove())

    for i in reversed(lista_aux):
        objeto.insere(i)

    return objeto

p1 = pilha()
p1.insere(1)
p1.insere(100)
p1.insere(200)
p1 = all_elements(p1)


