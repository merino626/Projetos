def retorna_soma(p1, f1):
    if len(p1) == 0 or len(f1) == 0:
        return 'A pilha e a fila precisam ter no minimo um valor'
    ### Pegando maior par da fila ###
    flag = 0
    max_fila = -1
    while len(f1) != 0:
        valor = f1.remove()
        if (valor % 2 == 0) and flag == 0:
            max_fila = valor
            flag = 1
        if valor % 2 == 0:
            par = valor
            if par > max_fila:
                max_fila = par
    ### Pegando menor impar da pilha ###
    flag = 0
    min_pilha = -1
    while len(p1) != 0:
        valor = p1.remove()
        if (valor % 2 != 0) and flag == 0:
            min_pilha = valor
            flag = 1
        if valor % 2 != 0:
            impar = valor
            if impar < min_pilha:
                min_pilha = impar
    ### Retornando a soma considerando a fila e pilha ###
    if min_pilha != -1 and max_fila != -1:
        return max_fila + min_pilha 
    elif max_fila == -1:
        return min_pilha
    else: return max_fila