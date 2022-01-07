#Ex04 - Criar uma função em Python que recebe uma lista como parâmetro e um inteiro e retorna True se o inteiro existe na lista.
# False caso contrário
def esta_na_lista(lista, inteiro):
    existe = False
    if inteiro in lista:
        existe = True
    return existe

print(esta_na_lista([5, 2, 1, 6, 9], 3))