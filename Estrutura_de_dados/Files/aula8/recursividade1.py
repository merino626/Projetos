def teste (x):
    print(x)
    if x < 5:
        return 3 * x
    else:
        return 2 * teste(x - 5) +7


'''
O que é retornado nas seguintes chamadas?
teste(4)
teste(10)
teste(12)
Montar a árvore de recursão para essas chamadas
'''
#teste(10)
#teste(10)
#teste(12)

'''
Arvore de recursão para teste(4)
teste(4) retorna (3 * 4) = 12



Arvore de recursão para teste(10)
teste(10) retorna -> teste(5) -> teste(0)  
              21  <-     7    <-    0    <-retorno


Arvore de recursao para teste(12)
teste(12)  retorna ->  teste(7) -> teste(2)
              45     <-     19    <-     6    <- retorno


'''