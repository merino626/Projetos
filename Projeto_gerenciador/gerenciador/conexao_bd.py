import datetime
import sqlite3
from sqlite3.dbapi2 import Cursor, connect

#CRUD Create, read, Update e delete

def conexao():
    try:
        # Conexão ao banco de dados
        connection = sqlite3.connect("db_cliente.db")
        return connection
    except:
        print('Erro ao conectar ao banco de dados')

def create_table():
    try:
        # Script para criar tabela
        sql = '''
                CREATE TABLE matriculas(
                    id_aluno integer primary key,
                    nome_aluno varchar(100),
                    matricula_ativa integer,
                    tipo_matricula integer,
                    data_inicio varchar(12),
                    data_fim varchar(12)
                )'''

        # Criando o cursor
        connection = conexao()
        cursor = connection.cursor()
        # Executando meu código sql acima
        cursor.execute(sql)
        # Efetivo a criação da tabela
        connection.commit()

        print('Tabela criada com sucesso')

    except:
        print('Erro ao conectar com o banco de dados. Função create_table')

    finally:
        # Sempre fecha o cursor e a conexão
        cursor.close()
        connection.close()


def insert(id_aluno,nome_aluno, matricula_ativa, tipo_matricula):
    existe_na_tabela = read_one_id(id_aluno)
    if existe_na_tabela != None:
        return 'Este id de aluno já existe na tabela'

    data_inicio = datetime.date.today()
    data_fim = data_inicio + datetime.timedelta(days=tipo_matricula)
    
    try:
        # Script para inserção
        sql = '''INSERT INTO matriculas(id_aluno, nome_aluno, matricula_ativa, tipo_matricula, data_inicio, data_fim)
             VALUES (?, ?, ?, ?, ?, ?)'''
    
        connection = conexao()
        cursor = connection.cursor()
        # Método em que passo a string, e uma lista que substituirá os simbolos "?" respectivamente.
        cursor.execute(sql, [id_aluno, nome_aluno, matricula_ativa, tipo_matricula, data_inicio, data_fim])
        connection.commit()
        print("Inserido com sucesso!")
        return ("Inserido com sucesso!")


    except:
        print('Erro ao conectar com o banco de dados. Função insert')
        return ('Erro ao conectar com o banco de dados.')

    finally:
        cursor.close()
        connection.close()

def update_table(matricula_ativa, nome_aluno, tipo_matricula, id_aluno):
    try:
        # Script para atualização
        update = '''
                UPDATE matriculas
                SET matricula_ativa = ?, nome_aluno = ? ,tipo_matricula = ?
                WHERE id_aluno = ?
                '''
        connection = conexao()
        cursor = connection.cursor()
        cursor.execute(update, [matricula_ativa, nome_aluno, tipo_matricula, id_aluno ])
        connection.commit()
        print('Update feito com sucesso')

    except:
        print('Erro ao conectar com o banco de dados. Função update')

    finally:
        cursor.close()
        connection.close()

def delete(id_aluno):
    try:
        #Script para a remoção de uma linha
        delete = '''DELETE FROM matriculas WHERE id_aluno = ?'''

        connection = conexao()
        cursor = connection.cursor()
        cursor.execute(delete, [id_aluno] )
        connection.commit()
        print('Registro deletado')

    except:
        print('Erro ao conectar com o banco de dados. função delete')

    finally:
        cursor.close()
        connection.close()

def read_all():
    try:
        # Script para ler todos os dados
        sql = '''SELECT * FROM matriculas'''

        connection = conexao()
        cursor = connection.cursor()
        cursor.execute(sql)

        # rows são todos os meus registros
        rows = cursor.fetchall()

        return rows


    except:
        print('Falha ao conectar-se com o banco. Função read_all')
    finally:
        cursor.close()
        connection.close()


def read_one_id(id_aluno):
    try:
        # Script para ler apenas um dado
        sql = '''SELECT * FROM matriculas WHERE id_aluno = ?'''

        connection = conexao()
        cursor = connection.cursor()
        cursor.execute(sql, [id_aluno])

        # row é apenas um registro
        row = cursor.fetchall()
        
        return row
        #print(f'Id do Cliente: {row[0]}, Nome: {row[1]}, Comentario: {row[2]}')

    except:
        print('Falha ao conectar-se com o banco. Função read_one_id')
    finally:
        cursor.close()
        connection.close()


def read_tipo_matricula(tipo_matricula):
    try:
        # Script para ler apenas um dado
        sql = '''SELECT * FROM matriculas WHERE tipo_matricula = ?'''

        connection = conexao()
        cursor = connection.cursor()
        cursor.execute(sql, [tipo_matricula])

        # row é apenas um registro
        rows = cursor.fetchall()
        return rows

    except:
        print('Falha ao conectar-se com o banco. Função read_one_tipo_matricula ')
    finally:
        cursor.close()
        connection.close()


def read_matricula_ativa(matricula_ativa):
    try:
        # Script para ler apenas um dado
        sql = '''SELECT * FROM matriculas WHERE matricula_ativa = ?'''

        connection = conexao()
        cursor = connection.cursor()
        cursor.execute(sql, [matricula_ativa])

        # row é apenas um registro
        rows = cursor.fetchall()
        return rows

    except:
        print('Falha ao conectar-se com o banco. Função read_one_matricula_ativa')
    finally:
        cursor.close()
        connection.close()


def read_data_inicio(data_inicio):
    try:
        # Script para ler apenas um dado
        sql = '''SELECT * FROM matriculas WHERE data_inicio = ?'''

        connection = conexao()
        cursor = connection.cursor()
        cursor.execute(sql, [data_inicio])

        # row é apenas um registro
        rows = cursor.fetchall()
        return rows

    except:
        print('Falha ao conectar-se com o banco. Função read_one_data_inicio')
    finally:
        cursor.close()
        connection.close()

def read_nome_aluno(nome_aluno):
    try:
        nome_aluno = ('%'+ nome_aluno + '%')
        # Script para ler apenas um dado
        sql =  '''SELECT * FROM matriculas WHERE nome_aluno like ? '''

        connection = conexao()
        cursor = connection.cursor()
        cursor.execute(sql, [nome_aluno])

        # row é apenas um registro
        rows = cursor.fetchall()
        return rows

    except:
        print('Falha ao conectar-se com o banco. Função read_one_data_inicio')
    finally:
        cursor.close()
        connection.close() 


if __name__ == '__main__':
    '''
    #insert(1, 1, 90)
    #insert(2, 1, 30)
    #insert(3, 1, 180)
    #insert(4, 1, 360)
    #update_table(0, 90, 4)
    #delete(4)
    #print(read_all())
    #print(read_one(1)  )'''


    #print(read_one_id(3))
    #print(read_data_inicio('2021-03-18'))
    #print(read_matricula_ativa(1))
    #print(read_tipo_matricula(30))

    #print(read_nome_aluno('d'))
