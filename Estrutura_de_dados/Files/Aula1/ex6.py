#Ex06 - Criar uma função em Python que recebe uma string e uma letra e retorna a quantidade de ocorrências da letra na string
#Não usar a função count
def quantidade_ocorrencias(string, letra):
    contador = 0
    for i in string:
        if i == letra:
            contador += 1
    return contador


print(quantidade_ocorrencias('aaabbc', 'a'))