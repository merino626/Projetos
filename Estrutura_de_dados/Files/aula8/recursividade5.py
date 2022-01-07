def imprime(n):
    print(n)
    if n == 1: #Trivial
        return
    return imprime(n-1) #Geral

imprime(8)