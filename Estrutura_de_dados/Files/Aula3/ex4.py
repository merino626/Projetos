def insere_ordena(vetor, valor, reverse=False):
    if valor in vetor:
        return

    vetor.append(valor)
    pos = vetor[0]
    for i in range(len(vetor)-1):
        if vetor[i] < vetor[i+1]:
            



insere_ordena([1], 2)