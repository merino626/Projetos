def inverte_max_min(vetor):
    minimo = vetor[0]
    maximo = vetor[0]
    pos_maximo = 0
    pos_minimo = 0
    posicao = 0

    for i in vetor:
        if i > maximo:
            maximo = i
            pos_maximo = posicao
        if i < minimo:
            minimo = i
            pos_minimo = posicao
        posicao += 1

    controle = vetor[pos_minimo]
    vetor[pos_minimo] = vetor[pos_maximo]
    vetor[pos_maximo] = controle
    return vetor

vetor = [500, 2, 3, 4, 5, 6, 1, 2, 4, 5,6]

print(inverte_max_min(vetor))