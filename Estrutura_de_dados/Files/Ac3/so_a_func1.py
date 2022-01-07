def retorna_min_impar(p1, f1):
    if len(p1) == 0 or len(f1) == 0:
        return 'A pilha e a fila precisam ter no minimo um valor'
    ### Pegando menor impar da fila ###
    flag = 0
    min_fila = -1
    while len(f1) != 0:
        valor = f1.remove()
        if (valor % 2 != 0) and flag == 0:
            min_fila = valor
            flag = 1
        if valor % 2 != 0:
            impar = valor
            if impar < min_fila:
                min_fila = impar
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
    ### Retornando o menor considerando a fila e pilha ###
    if min_pilha != -1 and min_fila != -1:
        if min_fila < min_pilha:
            return min_fila
        return min_pilha  
    elif min_fila == -1:
        return min_pilha
    else: return min_fila