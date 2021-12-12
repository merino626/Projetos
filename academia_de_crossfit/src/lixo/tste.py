import psycopg2 as db


###CONXÃO COM O BANCO ###
def conexao():
    try:
        conexao = db.connect(host='ec2-107-22-245-82.compute-1.amazonaws.com',
                            user='rsyejmiyfeyijc',
                            password='714711d1d2fdf32ec40bac5563ae9727ec6bc552e0b67e46791371867612023b',
                            dbname='d4ikjgj77j78t7')
        #print('conectado')
        return conexao
    except:
        print('Erro ao se conectar com o banco de dados')
        return 'Erro ao se conectar com o banco de dados'


def select_dados(arg1, arg2, arg3, arg4):
   try:
       conection = conexao()
       cursor = conection.cursor()
       sql = '''call insere_matricula(%s, %s, %s, %s)'''
       cursor.execute(sql, [arg1, arg2, arg3, arg4])
       conection.commit()
       return print('Dado inserido com sucesso')
   
   except Exception as err:
       # Caso haja erro no try, a conexão é aberta para não dar erro no finally
       conection = conexao()
       cursor = conection.cursor()
       return print('Erro ao chamar procedure' + str(err))
   
   finally:
       cursor.close()
       conection.close()

def retornaDadosDosAluno():
   try:
       conection = conexao()
       cursor = conection.cursor()
       sql = '''select * from dados_alunos();'''
       cursor.execute(sql)
       dados = cursor.fetchall()
       return dados
   
   except Exception as err:
       # Caso haja erro no try, a conexão é aberta para não dar erro no finally
       conection = conexao()
       cursor = conection.cursor()
       return print('Erro ao chamar procedure' + str(err))
   
   finally:
       cursor.close()
       conection.close()

   
