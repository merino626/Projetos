def bubblesort(vetor):
    trocas = 0
    comparações = 0
    for i in range(0, len(vetor)-1): # Laço de "passadas"|
        for j in range(0, len(vetor)- 1 - i) : #  Exclui sempre o ultimo indice, que já é o maior da lista
            
            if vetor[j] > vetor[j + 1]:  #Verifica se a posição da esquerda é maior que a direita
                aux = vetor[j]  #Guardo a pos. da esquerda na minha variavel auxiliar
                vetor[j] = vetor[j + 1] #Na minha posição da esquerdo atribuo o valor da direita
                vetor[j + 1] = aux #Na posição da direita atribuo o antigo valor da pos. da esquerda
                trocas += 1
            comparações += 1

    return vetor, f'Trocas: {trocas}', f'Comparações: {comparações}'



vetor = [1,9,0,3,3,4,6]

print(bubblesort(vetor))
