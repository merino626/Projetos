
def elevado(x, n):

    if n == 2:   #Trivial
        return x * x
    
    return x * elevado(x, n-1) #Geral


print(elevado(2, 3))



'''
ARVORE DE RECURSÃO PARA elevado(2, 3)

elevado(2, 3) retorna ->  2 * elevado(2, 3 - 1) -> 2 * elevado(2, 2) -> 2 * 4 -> 8

elevado(2, 2) retorna -> 2 * 2 -> 4

'''