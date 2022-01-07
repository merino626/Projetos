def binaria(vetor, valor):
    inicio = 0
    fim = len(vetor) - 1

    while inicio <= fim:
        meio = (inicio + fim) // 2
        print(vetor[meio])
        if vetor[meio] == valor:
            return vetor[meio]
        elif valor > vetor[meio]:
            inicio = meio + 1
        else:
            fim = meio - 1
    return -1



lista = [3,10,45,75,78,95,105,110]


print(lista)
print(binaria(lista, 46))