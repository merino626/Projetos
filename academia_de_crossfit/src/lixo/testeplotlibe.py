import matplotlib.pyplot as plt

qtd_alunos = 10
qtd_matriculas = 8
qtd_produtos = 15
qtd_despesas = 25
data = {'Alunos': qtd_alunos, 'Matriculas':qtd_matriculas, 'Produtos':qtd_produtos,
        'Despesas':qtd_despesas}
courses = list(data.keys())
values = list(data.values())


fig = plt.figure(figsize=(5,3))
ax = fig.add_subplot(111)

ax.set_title("Dados gerais", color="#ffffff")
ax.bar(courses, values, color="green", width = 0.4, edgecolor="#ffffff")



#ax.set_xlabel()
ax.set_ylabel("Quantidade")

### Contornos ###
ax.spines['bottom'].set_color('white')
ax.spines['top'].set_color('white')
ax.spines['right'].set_color('white')
ax.spines['left'].set_color('white')

## Eixo X ##
ax.xaxis.label.set_color('white')
ax.tick_params(axis='x', colors='white')

##Eixo Y##
ax.yaxis.label.set_color('white')
ax.tick_params(axis='y', colors='white')

#plt.show()
plt.savefig('dados_gerais.png',transparent=True)