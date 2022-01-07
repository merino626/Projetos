def selectionSort (vetor):
 
    for i in range(len(vetor)-1):
       min = i
       
       for j in range(i + 1,len(vetor)):
           if vetor[ j ] < vetor[min]:
               min = j

       aux = vetor[i]
       vetor[i] = vetor[min]
       vetor[min] = aux

    return vetor


vetor = [30, 40, 50, 20, 10]
print(selectionSort(vetor))
