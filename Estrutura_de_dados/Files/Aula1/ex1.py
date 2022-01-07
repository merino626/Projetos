#Ex01 - Criar um programa que preenche uma lista com 5 elementos. 
# Calcula a soma dos elementos Imprime a soma dos elementos e todos os elementos da lista.
lista = []
for i in range(5):
    lista.append(int(input('Digite um numero inteiro: ')))

print(f'Os elementos da lista: {lista}')
print(f'A soma de todos os elementos: {sum(lista)}')
