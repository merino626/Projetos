def sequencial(vetor, x):
    for i in range(len(vetor)):
        if vetor[i] == x:
            return 'Já existe no vetor e esta ordenado'
    vetor.append(x)
    for i in range(len(vetor),0, -1):
        if x < vetor[i-1]:
            aux = vetor[i-1]
            vetor[i-1] = x
            vetor[i] = aux
    return vetor


lista = [1, 3, 6, 8, 10, 14, 18, 20]
print(sequencial(lista,21))
