def sequencial(vetor, palavra):
    for i in range(len(vetor)):
        if vetor[i] == palavra:
            return i
    return -1

def binaria(vetor, palavra):
    inicio = 0
    fim = len(vetor) - 1

    while inicio <= fim:
        meio = (inicio + fim) // 2

        if vetor[meio] == palavra:
            return meio
        elif palavra > vetor[meio]:
            inicio = meio + 1
        else:
            fim = meio - 1
    return -1

def bb(v,x): 
   e = 0
   d = len(v)-1
   while e <= d:
        m = (e + d)//2
        if v[m] == x:
            return m
        elif x > v[m]:
	        e = m+1
        else:
	        d = m-1
   return -1





vetor = ['12','13','1', '42', '51', '92', '28', '28']

vetor2 = sorted(vetor)
print(binaria(vetor2, '122'))
