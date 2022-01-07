def ordem_crescente(p1):
    if len(p1) == 0:
        return 'A pilha precisa ter no minimo um valor'
    ### Verificando se os impares da pilha estão em ordem crescente ###
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
                return False
    if min_pilha == -1:
        return 'Não há impares na pilha'
    return True