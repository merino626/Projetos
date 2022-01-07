def imprime_digitos(n):
    if n == 0:
        return
    print(n % 10)

    return imprime_digitos(n // 10)

imprime_digitos(2365)


### arvore de recursão para imprime_digitos(2356)
'''

imprime_digitos(2365) retorna -> print(2365 % 10) -> print(5) -> imprime_digitos(2365 // 10) -> imprime_digitos(236) -> None

imprime_digitos(236) retorna -> print(236 % 10) -> print(6) -> imprime_digitos(236 // 10) -> imprime_digitos(23) -> None

imprime_digitos(23) retorna -> print(23 % 10) -> print(3) -> imprime_digitos(23 // 10) -> imprime_digitos(2) -> None

imprime_digitos(2) retorna -> print(2 % 10) -> print(2) -> imprime_digitos(2 // 10) -> imprime_digitos(0) -> None
'''