def bubblesort(vetor):
    for i in range(0, len(vetor)-1): # Laço de "passadas" / iterações, que percorrerá o vetor até que a lista esteja ordenada
        for j in range(0, len(vetor)-1 - i) : #  Exclui sempre o ultimo indice, que já é o maior da lista
            
            if vetor[j] > vetor[j + 1]:  #Verifica se a posição da esquerda é maior que a direita
                aux = vetor[j]  #Guardo a posição da esquerda na minha variavel auxiliar
                vetor[j] = vetor[j + 1] #Na minha posição da esquerdo atribuo o valor da direita
                vetor[j + 1] = aux #Na posição da direita atribuo o antigo valor da pos. da esquerda
                
    return vetor, f'Trocas: {trocas}', f'Comparações: {comparações}'


vetor = [1,6,23,3,4,6,4,8]
print(bubblesort(vetor))
