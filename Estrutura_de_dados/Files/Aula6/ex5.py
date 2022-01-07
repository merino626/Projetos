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


def carros(pilha, placa):
    removidos = []
    i = 1
    while len(pilha) > 0:
        removido = pilha.remove()
        if removido == placa:
            print(removidos)
        removidos.append(f'{i} Carro a ser removido: {removido}')
        i += 1
    return 'O carro não está na rua'

p1 = pilha()
p1.insere('onix')
p1.insere('celta')
p1.insere('palio')
carros(p1, 'onix')