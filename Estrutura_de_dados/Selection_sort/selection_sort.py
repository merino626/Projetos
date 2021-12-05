def selectionSort(vetor):
    n = len(vetor)                      #Pego o tamanho do vetor na minha variavel n
    for i in range(n-1):                #Laço que é responsável por descartar os valores que já são considerados como minimos
       min = i                          #Variavel que sempre guardará a primeira posição do vetor como valor minimo de uma iteração.
       for j in range(i+1, n):          #Laço responsável por percorrer o vetor e fazer o "algoritmo do menor"
           if vetor[ j ] < vetor[min]:  #Verifica se o valor da posição é menor que o valor do minimo
               min = j                  # Caso seja, esse valor é o novo minimo
              
       aux = vetor[i]                   #Ao final de toda iteração, o valor minimo irá para o começo da lista, junto com os outros valores minimos
       vetor[i] = vetor[min]            # Perceba que desta forma a lista vai se ordenando aos poucos do menor ao maior
       vetor[min] = aux
    return vetor


vetor = [30, 40, 50, 20, 10]
print(selectionSort(vetor))
