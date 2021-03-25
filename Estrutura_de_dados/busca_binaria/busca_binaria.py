def busca_binaria(array, valor):
    inicio = 0                      #Valor da posição 0 da lista
    fim = len(array) - 1            #Valor ultima posição da lista

    while inicio <= fim:            # O loop continuara enquanto o inicio não encontrar o fim
        meio = (inicio + fim) // 2  # Definição do meio da lista (sempre truncado por 2, pois servirá para lista pares e impares)

        if array[meio] == valor:    #Sempre verifca-se a posição do meio para ver se o valor está lá
            return meio             
        elif valor > array[meio]:   #Caso não esteja, vejo se o valor é maior que o valor da posição do meio
            inicio = meio + 1       #Redefino meu inicio para a posição do meio + 1, já que o valor é maior que o meio
        else:
            fim = meio - 1          #Caso valor seja menor que o valor do meio, então o fim passa a valer meio - 1

    return -1  #Caso este valor não esteja na lista, retorno -1



lista_ordenada = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]  # Para trabalhar com busca binária é essencial uma lista já ordenada.

print(busca_binaria(lista_ordenada, 8))


#Observações:
'''
Para trabalhar com busca binaria eu preciso sempre de uma lista ordenada.
A busca binaria examina sempre a posição do meio do vetor.
A busca binaria examina se o valor procurado está no meio, se não estiver
ela corta a lista pela metade, ou puxando o fim para uma posição antes do meio
ou puxando o inicio para uma posição após o meio.
* A lógica deste algorimo é semelhante em diversas linguagens, a unica diferença aqui
é a sintaxe do python.
'''
