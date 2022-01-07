def teste2 (x, y):
    if x < y:
        return -3
    else:
        return teste2(x-y,y+3)+y


'''
O que é retornado nas seguintes chamadas?
teste2(2,7)
teste2(5,3)
teste2(15,3)
Montar a árvore de recursão para essas chamadas
'''


'''
Arvore de recursão para teste(2, 7)

teste(2, 7) return -3
'''

'''
Arvore de recursão para teste(5, 3)

teste2(5, 3) retorna teste2(5 - 3, 3 + 3) + 3 -> teste2(2, 6) + 3 ->  -3 + 3 -> 0


teste2(2, 6) retorna -3
'''

'''
Arvore de recursão para teste(15, 3)

teste2(15, 3) retorna -> teste2(15 - 3, 3 + 3)+3 -> teste2(12, 6)+3 -> 0 + 3 -> 6

teste2(12, 6) retorna -> teste2(12 - 6, 6 + 3 )+6 -> teste2(6, 9)+3 -> -3 + 6 -> 3

teste2(6, 9) retorna  -> -3



'''