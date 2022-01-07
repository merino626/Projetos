def soma_numeros(n):
    if n == 1:
        return 1
    return n + soma_numeros(n-1)

print(soma_numeros(2))