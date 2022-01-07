# Ex05 - Criar uma função em Python que recebe uma lista como parâmetro e um inteiro e retorna
# -1 se o inteiro não existe na lista
# A primeira posição onde é encontrado na lista caso contrário
def esta_na_lista(lista, inteiro):
    existe = -1
    if inteiro in lista:
        existe = f'O numero {inteiro}, esta na posicao: {lista.index(inteiro)}' 
    return existe

print(esta_na_lista([1, 4, 5, 7, 9], 10))