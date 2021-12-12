################################################################################
## FUNÇÕES DE VALIDAÇÕES DE DADOS
## 
## Documento criado com o intuito de criar validações separadamente do arquivo
## principal (arquivos que manipula as telas). Isso facilitará a manutenção do
## Código a longo prazo.
##
################################################################################

import src.custom_erros as erros
import re
import string



####VALIDAÇÃO PARA INSERÇÃO DE DADOS DOS ALUNOS####
### Verifica se o campo está vazio ###
def valida_campo_vazio(campo):
    if campo == '': raise erros.CampoVazio
    
### Validando o id ###
def valida_id(id):
    if id > 300 or id < 1: raise erros.ValorForaDeRange

### Validando nome do aluno ###
def valida_nome(nome):
    if len(nome) < 6: raise erros.NomeCurto
    acentos = "áàéèóòíìúùãõâêîôû "
    char_validos = string.ascii_letters+acentos+acentos.upper()
    for i in nome:
        if i not in char_validos:
            raise erros.CaractereInvalido

### Validando nome do produto ###
def valida_nome_produto(nome):
    if len(nome) < 3: raise erros.NomeCurto
    acentos = "áàéèóòíìúùãõâêîôû "
    char_validos = string.ascii_letters+acentos+acentos.upper()
    for i in nome:
        if i not in char_validos:
            raise erros.CaractereInvalido

### Validando a idade do aluno ###
def valida_idade(idade):
    if idade < 12 or idade > 90: raise erros.IdadeInvalida

### Validando o cpf do aluno ###
def valida_cpf(cpf: str) -> bool:

    """ Efetua a validação do CPF, tanto formatação quando dígito verificadores.

    Parâmetros:
        cpf (str): CPF a ser validado

    Retorno:
        bool:
            - Falso, quando o CPF não possuir o formato 999.999.999-99;
            - Falso, quando o CPF não possuir 11 caracteres numéricos;
            - Falso, quando os dígitos verificadores forem inválidos;
            - Verdadeiro, caso contrário.

    Exemplos:

    >>> validate('529.982.247-25')
    True
    >>> validate('52998224725')
    False
    >>> validate('111.111.111-11')
    False
    """

    # Verifica a formatação do CPF
    if not re.match(r'\d{3}\.\d{3}\.\d{3}-\d{2}', cpf):
        return False

    # Obtém apenas os números do CPF, ignorando pontuações
    numbers = [int(digit) for digit in cpf if digit.isdigit()]

    # Verifica se o CPF possui 11 números ou se todos são iguais:
    if len(numbers) != 11 or len(set(numbers)) == 1:
        return False

    # Validação do primeiro dígito verificador:
    sum_of_products = sum(a*b for a, b in zip(numbers[0:9], range(10, 1, -1)))
    expected_digit = (sum_of_products * 10 % 11) % 10
    if numbers[9] != expected_digit:
        return False

    # Validação do segundo dígito verificador:
    sum_of_products = sum(a*b for a, b in zip(numbers[0:10], range(11, 1, -1)))
    expected_digit = (sum_of_products * 10 % 11) % 10
    if numbers[10] != expected_digit:
        return False

    return True

### Validando o telefone do aluno ###
def valida_telefone(telefone):
    caracteres_validos = '0123456789()-'
    for i, item in enumerate(telefone):
        if item not in caracteres_validos: raise erros.TelefoneInexistente
        if i == 0 and item != '(': raise erros.TelefoneInexistente
        if i == 3 and item != ')': raise erros.TelefoneInexistente
        if i == 8 and item != '-':
            if i == 9 and item != '-': raise erros.TelefoneInexistente

    posicao_traco = telefone.find('-')
    posicao_parenteses = telefone.find(')')
    primeira_metade_telefone = telefone[posicao_parenteses+1:posicao_traco]
    segunda_metade_telefone = telefone[posicao_traco+1:]
    ## Garantindo que a primeira e segunda metade tenham a quantidade correta de números ##
    if len(primeira_metade_telefone) > 5 or len(primeira_metade_telefone) < 4:
        raise erros.TelefoneInexistente
    if len(segunda_metade_telefone) != 4:
        raise erros.TelefoneInexistente

    if len(telefone) < 13 or len(telefone) > 14: raise erros.TelefoneInexistente

### Validando o email do aluno ###
def valida_email_sintaxe(email):
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        return False
    return True

def valida_cpf_ja_existente(pesquisa ,tabela_alunos):
    cpf_buscado = pesquisa
    for aluno in tabela_alunos:
        cpf = aluno[3]
        if cpf_buscado == aluno[3]:
            raise erros.CpfJaExistente
    return