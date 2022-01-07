def busca_binaria(array, valor):
    inicio = 0
    fim = len(array) - 1

    while inicio <= fim:
        meio = (inicio + fim) // 2

        if array[meio] == valor:
            return meio
        elif valor > array[meio]:
            inicio = meio + 1
        else:
            fim = meio - 1

    return -1         



lista_ordenada = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

print(busca_binaria(lista_ordenada, 8))


import math
print(math.log(10, 2))