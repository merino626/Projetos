
n = 1000000
binario = []
while n > 0:
    binario.append(n % 2)
    n = n // 2

binario.reverse()   
lista_decimais = []  
for i in range(len(binario)):
    lista_decimais.append(2 ** i)
lista_decimais.reverse()

print('Decimais: ',lista_decimais)
print('Binarios: ',binario)