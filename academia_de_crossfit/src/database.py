import psycopg2 as db
from decouple import config

###CONXÃO COM O BANCO ###
def conexao():
    try:
        conexao = db.connect(host=config('dbHost'),
                            user=config('dbUser'),
                            password=config('dbPass'),
                            dbname=config('dbName'))
        #print('conectado')
        return conexao
    except:
        print('Erro ao se conectar com o banco de dados')
        return 'Erro ao se conectar com o banco de dados'


### VERIFICAÇÃO DO LOGIN NO BANCO ###
class LoginVerification():
    def verifica_login(self, usuario):
        try:
            conection = conexao()
            cursor = conection.cursor()  

            sql = '''SELECT * FROM credencials WHERE usuario = %s'''
            cursor.execute(sql, [usuario])
            tabela = cursor.fetchone()
            return tabela

        except:
            # Caso haja erro no try, a conexão é aberta para não dar erro no finally
            conection = conexao()
            cursor = conection.cursor()
            return 'Usuario não existe'

        finally:
            cursor.close()
            conection.close()


### QUERY DE TODOS OS DADOS DO ALUNO ###
class DadosAlunos():
    def select_dados(self):
        try:
            conection = conexao()
            cursor = conection.cursor()

            sql = '''SELECT * FROM aluno'''
            cursor.execute(sql)
            tabela = cursor.fetchall()
            return tabela
        
        except:
            # Caso haja erro no try, a conexão é aberta para não dar erro no finally
            conection = conexao()
            cursor = conection.cursor()
            return 'Tabela vazia'
        
        finally:
            cursor.close()
            conection.close()


    def inserir_dados_sem_id(self, nome, idade, cpf, telefone, email, nome_usuario, senha):
        try:
            conection = conexao()
            cursor = conection.cursor()

            sql = '''INSERT INTO aluno
            (nome_aluno, idade, cpf, telefone, email, nome_usuario, senha)
            VALUES(%s, %s, %s, %s, %s, %s, %s);
            '''
            cursor.execute(sql, [nome, idade, cpf, telefone, email, nome_usuario, senha])
            conection.commit()
            return 'Dados inseridos com sucesso'
        
        except:
            # Caso haja erro no try, a conexão é aberta para não dar erro no finally
            conection = conexao()
            cursor = conection.cursor()
            return 'Tabela vazia'
        
        finally:
            cursor.close()
            conection.close()

    def retornaDadosDosAlunos(self):
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

    def excluir_aluno(self, nome, idade, cpf, telefone, email):
        try:
            conection = conexao()
            cursor = conection.cursor()
            sql = """DELETE FROM aluno where nome_aluno = %s and idade=%s and cpf = %s and telefone=%s and email = %s""" 

            cursor.execute(sql, [nome, idade, cpf, telefone, email])
            conection.commit()
            return 'Dados inseridos com sucesso'
        
        except:
            # Caso haja erro no try, a conexão é aberta para não dar erro no finally
            conection = conexao()
            cursor = conection.cursor()
            return 'Erro'
        
        finally:
            cursor.close()
            conection.close()


    def atualizar_aluno(self, nome, idade, cpf, telefone, email,
    nome2, idade2, cpf2, telefone2, email2):
            try:
                conection = conexao()
                cursor = conection.cursor()
                sql = """update aluno set nome_aluno = %s, idade=%s, cpf = %s, telefone=%s, email = %s
                where nome_aluno = %s and idade = %s and cpf = %s and telefone = %s and email = %s""" 

                cursor.execute(sql, [nome, idade, cpf, telefone, email,
                nome2, idade2, cpf2, telefone2, email2])
                conection.commit()
                return 'Dados inseridos com sucesso'
            
            except:
                # Caso haja erro no try, a conexão é aberta para não dar erro no finally
                conection = conexao()
                cursor = conection.cursor()
                return 'Erro'
            
            finally:
                cursor.close()
                conection.close()
                
    def alunos_sem_av_fisicas(self):
            try:
                conection = conexao()
                cursor = conection.cursor()
                sql = """select a.id_aluno, a.nome_aluno, a.idade,
                    a.cpf, a.telefone, a.email from aluno a 
                    inner join avaliacao_fisica af on a.id_aluno = af.id_aluno 
                    where af.densidade_ossea = 0 and af.gordura_visceral = 0
                    and af.hidratacao = 0 and af.massa_gorda = 0 and af.massa_magra = 0
                    and af.massa_muscular = 0 and af.metabolismo_basal = 0;
                    """ 
                cursor.execute(sql)
                dados = cursor.fetchall()
                return dados 
            except:
                # Caso haja erro no try, a conexão é aberta para não dar erro no finally
                conection = conexao()
                cursor = conection.cursor()
                return 'Erro'
            
            finally:
                cursor.close()
                conection.close()

    def alunos_com_av_fisicas(self):
            try:
                conection = conexao()
                cursor = conection.cursor()
                sql = """select a.id_aluno , a.nome_aluno, a.idade, a.cpf, a.telefone, a.email from aluno a 
                        inner join avaliacao_fisica af on a.id_aluno = af.id_aluno 
                        where af.densidade_ossea != 0 or af.gordura_visceral != 0
                        and af.hidratacao != 0 or af.massa_gorda != 0 or
                        af.massa_magra != 0 or af.massa_muscular != 0 or af.metabolismo_basal != 0;
                    """ 
                cursor.execute(sql)
                dados = cursor.fetchall()
                return dados 
            except:
                # Caso haja erro no try, a conexão é aberta para não dar erro no finally
                conection = conexao()
                cursor = conection.cursor()
                return 'Erro'
            
            finally:
                cursor.close()
                conection.close()
                

class AvFisica():
    def retornaDadosAvFisicas(self):
        try:
            conection = conexao()
            cursor = conection.cursor()
            sql = '''select A.id_aluno, A.nome_aluno, AV.massa_gorda, AV.massa_magra, AV.massa_muscular, AV.hidratacao,
                AV.densidade_ossea, AV.gordura_visceral, AV.metabolismo_basal from avaliacao_fisica as AV inner join aluno as A
                on AV.id_aluno = A.id_aluno '''
            cursor.execute(sql)
            dados_com_join = cursor.fetchall()

    
            return dados_com_join
        
        except Exception as err:
            # Caso haja erro no try, a conexão é aberta para não dar erro no finally
            conection = conexao()
            cursor = conection.cursor()
            return print('Erro ao fazer join de aluno + av_fisica' + str(err))
        
        finally:
            cursor.close()
            conection.close()

    def atualizar_avFisica(self,
    id_aluno, massaGorda, massaMagra, massaMuscular,
    hidratacao, densidadeOssea, gorduraVisceral, metabolismoBasal):

            try:
                conection = conexao()
                cursor = conection.cursor()
                print(id_aluno, massaGorda, massaMagra, massaMuscular,
                hidratacao, densidadeOssea, gorduraVisceral, metabolismoBasal)

                sql = """UPDATE avaliacao_fisica
                SET massa_gorda=%s, massa_magra=%s, massa_muscular=%s,
                hidratacao=%s, densidade_ossea=%s, gordura_visceral=%s, metabolismo_basal=%s
                WHERE id_aluno=%s;
                """ 

                cursor.execute(sql, [massaGorda, massaMagra, massaMuscular,
                hidratacao, densidadeOssea, gorduraVisceral, metabolismoBasal, id_aluno])
                conection.commit()
                return 'Dados inseridos com sucesso'
            
            except Exception as err:
                # Caso haja erro no try, a conexão é aberta para não dar erro no finally
                conection = conexao()
                cursor = conection.cursor()
                print(err)
                return "Erro"
            
            finally:
                cursor.close()
                conection.close()

class Matricula():
    def retornaDadosMatriculas(self):
        try:
            conection = conexao()
            cursor = conection.cursor()
            sql = '''select A.id_aluno, A.nome_aluno, M.matricula_ativa, M.tipo_matricula, M.data_inicio, M.data_fim
                    from matricula as M inner join aluno as A on M.id_aluno = A.id_aluno '''
            cursor.execute(sql)
            dados = cursor.fetchall()
            return dados
        
        except Exception as err:
            # Caso haja erro no try, a conexão é aberta para não dar erro no finally
            conection = conexao()
            cursor = conection.cursor()
            return print('Erro ao fazer join de aluno + Matricula' + str(err))
        
        finally:
            cursor.close()
            conection.close()

    def atualizar_matricula(self,
    id_aluno, matricula_ativa, tipo_matricula, data_inicio, data_fim):
            try:
                conection = conexao()
                cursor = conection.cursor()
                sql = """UPDATE matricula
                SET matricula_ativa=%s, tipo_matricula=%s, data_inicio=%s,
                data_fim=%s WHERE id_aluno=%s;""" 

                cursor.execute(sql, [matricula_ativa, tipo_matricula, 
                data_inicio, data_fim, id_aluno])
                conection.commit()
                return 'Dados inseridos com sucesso'
            
            except Exception as err:
                # Caso haja erro no try, a conexão é aberta para não dar erro no finally
                conection = conexao()
                cursor = conection.cursor()
                print(err)
                return "Erro"
            
            finally:
                cursor.close()
                conection.close()

class Estoque():
    def retornaDadosEstoque(self):
        try:
            conection = conexao()
            cursor = conection.cursor()
            sql = '''select id_produto, produto, qtd, observacao from estoque  '''
            cursor.execute(sql)
            dados = cursor.fetchall()
            return dados
        
        except Exception as err:
            # Caso haja erro no try, a conexão é aberta para não dar erro no finally
            conection = conexao()
            cursor = conection.cursor()
            return print('Erro ao fazer a query do estoque' + str(err))
        
        finally:
            cursor.close()
            conection.close()
    
    def inserir_estoque(self, produto, qtd, observacao):
        try:
            conection = conexao()
            cursor = conection.cursor()

            sql =  """INSERT INTO estoque (produto, qtd, observacao) values(%s, %s, %s);"""
            cursor.execute(sql, [produto, qtd, observacao])
            conection.commit()
            return 'Dados inseridos com sucesso'
        
        except:
            # Caso haja erro no try, a conexão é aberta para não dar erro no finally
            conection = conexao()
            cursor = conection.cursor()
            return 'Tabela vazia'
        
        finally:
            cursor.close()
            conection.close()

    def atualizar_estoque(self,
    id_produto, produto, qtd, observacao):
            try:
                conection = conexao()
                cursor = conection.cursor()
                sql = """UPDATE estoque
                SET produto=%s, qtd=%s, observacao=%s WHERE id_produto=%s;""" 

                cursor.execute(sql, [produto, qtd, 
                observacao, id_produto])
                conection.commit()
                return 'Dados inseridos com sucesso'
            
            except Exception as err:
                # Caso haja erro no try, a conexão é aberta para não dar erro no finally
                conection = conexao()
                cursor = conection.cursor()
                print(err)
                return "Erro"
            
            finally:
                cursor.close()
                conection.close()

    def excluir_produto(self, produto, qtd, observacao):
            try:
                conection = conexao()
                cursor = conection.cursor()
                sql = """DELETE FROM estoque where produto = %s and qtd=%s and observacao = %s""" 

                cursor.execute(sql, [produto, qtd, observacao])
                conection.commit()
                return 'Dados inseridos com sucesso'
            
            except:
                # Caso haja erro no try, a conexão é aberta para não dar erro no finally
                conection = conexao()
                cursor = conection.cursor()
                return 'Erro'
            
            finally:
                cursor.close()
                conection.close()



class Despesa():
    def retornaDadosDespesas(self):
        try:
            conection = conexao()
            cursor = conection.cursor()
            sql = '''select * from orcamento'''
            cursor.execute(sql)
            dados = cursor.fetchall()
            return dados
        
        except Exception as err:
            # Caso haja erro no try, a conexão é aberta para não dar erro no finally
            conection = conexao()
            cursor = conection.cursor()
            return print('Erro ao fazer a query das despesas' + str(err))
        
        finally:
            cursor.close()
            conection.close()

    def inserir_despesa(self, despesa, valor, data_pagamento, observacao):
        try:
            conection = conexao()
            cursor = conection.cursor()
            sql =  """INSERT INTO orcamento (nome_despesa, valor_despesa, data_pagamento ,observacao)
             values(%s, %s, %s, %s);"""
            cursor.execute(sql, [despesa, valor, data_pagamento, observacao])
            conection.commit()
            return 'Dados inseridos com sucesso'
        
        except:
            # Caso haja erro no try, a conexão é aberta para não dar erro no finally
            conection = conexao()
            cursor = conection.cursor()
            return 'Tabela vazia'
        
        finally:
            cursor.close()
            conection.close()

    def atualizar_despesa(self, id_despesa, nome_despesa, valor, data_vencimento, observacao):
            try:
                conection = conexao()
                cursor = conection.cursor()
                sql = """UPDATE orcamento
                SET nome_despesa=%s, valor_despesa=%s, data_pagamento=%s, observacao=%s WHERE id_despesa=%s;""" 

                cursor.execute(sql, [nome_despesa, valor, data_vencimento, observacao, id_despesa])
                conection.commit()
                return 'Dados atualizados com sucesso'
            
            except Exception as err:
                # Caso haja erro no try, a conexão é aberta para não dar erro no finally
                conection = conexao()
                cursor = conection.cursor()
                print(err)
                return "Erro"
            
            finally:
                cursor.close()
                conection.close()

    def excluir_despesa(self, nome_despesa, valor, data_vencimento, observacao):
            try:
                conection = conexao()
                cursor = conection.cursor()
                sql = """DELETE FROM orcamento where nome_despesa = %s and valor_despesa=%s and data_pagamento = %s
                and observacao = %s""" 

                cursor.execute(sql, [nome_despesa, valor, data_vencimento, observacao])
                conection.commit()
                return 'Dados inseridos com sucesso'
            
            except:
                # Caso haja erro no try, a conexão é aberta para não dar erro no finally
                conection = conexao()
                cursor = conection.cursor()
                return 'Erro'
            
            finally:
                cursor.close()
                conection.close()

if __name__ == '__main__':
    # query = LoginVerification()
    # print(query.verifica_login('fivetech'))
    # selectAll = DadosAlunos()
    # print(selectAll.select_dados())
    #inserir = DadosAlunos()
    #print(inserir.inserir_dados_sem_id('Laercio Santos', '29', '391.201.302/21', '(11)92193-1235', 'La_santos@gmail.com'))

    query = AvFisica()
    tabela1= query.retornaDadosAvFisicas()
    print(tabela1)
 