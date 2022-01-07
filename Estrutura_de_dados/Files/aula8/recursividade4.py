def fibonacci(n):
    if n<=0:# TRIVIAL
        return 0
    elif n==1:
        return 1
    else: # GERAL
        return fibonacci(n-1) + fibonacci(n-2)

'''
Arvore de recursividade para fibonacci(5)

fibonacci(5) retorna -> fibonacci(5 - 1) + fibonacci(5 - 2) -> fibonacci(4) + fibonacci(3) -> 3 + 2 -> 5

fibonacci(4) retorna -> fibonacci(4 - 1) + fibonacci(4 - 2) -> fibonacci(3) + fibonacci(2) -> 2 + 1 -> 3
fibonacci(3) retorna -> fibonacci(3 - 1) + fibonacci(3 - 2) -> fibonacci(2) + fibonacci(1) -> 1 + 1 -> 2


fibonacci(3) retorna -> fibonacci(3 - 1) + fibonacci(3 - 2) -> fibonacci(2) + fibonacci(1) -> 1 + 1 -> 2
fibonacci(2) retorna -> fibonacci(2 - 1) + fibonacci(2 - 2) -> fibonacci(1) + fibonacci(0) -> 1 + 0 -> 1
fibonacci(2) retorna -> fibonacci(2 - 1) + fibonacci(2 - 2) -> fibonacci(1) + fibonacci(0) -> 1 + 0 -> 1
fibbonaci(1) retorna -> 1


fibonacci(2) retorna -> fibonacci(2 - 1) + fibonacci(2 - 2) -> fibonacci(1) + fibonacci(0) -> 1 + 0 -> 1
fibbonaci(1) retorna -> 1
fibbonaci(1) retorna -> 1
fibbonaci(0) retorna -> 0
fibbonaci(1) retorna -> 1
fibbonaci(0) retorna -> 0


fibbonaci(1) retorna -> 1
fibbonaci(0) retorna -> 0
'''


