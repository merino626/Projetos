# MDC – Algoritmo de Euclides
def mdc(num1, num2): # num1 > num2
    if num2==0:# TRIVIAL
        return num1
    else: # GERAL
        return mdc(num2, num1 % num2)

'''
Arvore de recursão para mdc(10, 3)
  num1 num2
mdc(10, 3) retorna -> mdc(3, 10 % 3) -> mdc(3, 1) -> 1

mdc(3, 1) retorna  -> mdc(1, 3 % 1) -> mdc(1, 0) -> 1

mdc(1, 0) retorna -> 1

'''