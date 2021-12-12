class ValorForaDeRange(Exception):
    '''Classe de erro usada quando um valor não está dentro de um range definido na
       regra de negocio
     '''
    pass

class CaractereInvalido(Exception):
    '''
    Classe de erro usada para quando um caractere invalido foi inserido pelo usuario
    '''
    pass

class CampoVazio(Exception):
    '''
    Classe de erro usada para lançar um erro criado a partir de um campo vazio digitado
    pelo usuario
    '''
    pass

class NomeCurto(Exception):
    '''
    Classe de erro usada para lançar um erro criado a partir de um nome muito curto
    digitado pelo usuário.
     '''
    pass

class IdadeInvalida(Exception):
    '''
    Classe de erro usado para lançar um erro criado a partir de um idade inválida digitada
    pelo usuário
    '''
    pass

class CpfInexistente(Exception):
    ### Vou implementar depois para validar o cpf quando estiver em produção ###
    '''
    Classe de erro usada para lançar um erro criado a partir de um cpf inválido
    (No nosso caso o cpf inválido será apenas um cpf que não atende ao tamanho
    necessário do cpf.)
     '''
    pass

class TelefoneInexistente(Exception):
    '''
    Classe de erro usada para lançar um erro criado a partir de um telefone
    com um tamanho que não é permitido no BD
    '''
    pass

class CpfJaExistente(Exception):
    '''
    Classe de erro usada para quando é tentado cadastrar um cpf que já existe
    na base de alunos
    '''
    pass
