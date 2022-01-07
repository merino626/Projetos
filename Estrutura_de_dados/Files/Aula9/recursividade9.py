def imprime_digitos(n):
    if n > 0:
        imprime_digitos( n // 10)
        print(n % 10)

imprime_digitos(2365)



### arvore de recursão para imprime_digitos(2365)
'''

'''