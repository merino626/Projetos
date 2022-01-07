def binaria(vetor, valor, nvalor):
    inicio = 0
    fim = len(vetor) - 1

    while inicio <= fim:
        meio = (inicio + fim) // 2

        if vetor[meio] == valor:
            vetor[meio] = nvalor
            return vetor
        elif valor > vetor[meio]:
            inicio = meio + 1
        else:
            fim = meio - 1
    return -1



lista = [1, 2, 3, 4, 5, 6, 7, 8]

lista.sort(reverse=True)
print(lista)
print(binaria(lista, 8, 122))