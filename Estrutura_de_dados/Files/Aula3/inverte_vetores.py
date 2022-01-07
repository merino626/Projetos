def inverte(vetor):
    metade_par = (len(vetor) / 2) - 1
    metade_impar = len(vetor) // 2
    controle = len(vetor) -1

    for i in range(0, len(vetor)):
        ultimo = vetor[controle]
        vetor[controle] = vetor[i]
        vetor[i] = ultimo
        controle -= 1
        if (len(vetor) % 2 == 0) and (i == metade_par):
            break
        elif i == metade_impar:
            break

    return vetor

vetor = [10, 9, 8, 7, 6, 122, 4, 3, 2, 15]
print(inverte(vetor))

