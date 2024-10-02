import requests
import unittest

'''
Cada aluno será representado por um dicionário JSON como o seguinte: 
{"id":1,"nome":"marcos"}

Testes 000 e 001:
Na URL /alunos, se o verbo for GET, 
retornaremos uma lista com um dicionário para cada aluno.

Na URL /alunos, com o verbo POST, ocorrerá a criação do aluno,
enviando um desses dicionários 

Teste 002
Na URL /alunos/<int:id>, se o verbo for GET, devolveremos o nome e id do aluno. 
(exemplo. /alunos/2 devolve o dicionário do aluno(a) de id 2)

Teste 003
Na URL /reseta, apagaremos a lista de alunos e professores (essa URL só atende o verbo POST e DELETE).

Teste 004
Na URL /alunos/<int:id>, se o verbo for DELETE, deletaremos o aluno.
(dica: procure lista.remove)

Teste 005
Na URL /alunos/<int:id>, se o verbo for PUT, 
editaremos o aluno, mudando seu nome. 
Para isso, o usuário vai enviar um dicionário 
com a chave nome, que deveremos processar

Se o usuário manda um dicionário {“nome”:”José”} para a url /alunos/40,
com o verbo PUT, trocamos o nome do usuário 40 para José

Tratamento de erros

Testes 006 a 008b: Erros de usuário darão um código de status 400, e retornarão um dicionário descrevendo o erro. 
No teste 006, tentamos fazer GET, PUT e DELETE na URL  /alunos/15, sendo que o aluno de id 15 não existe. Nesse caso, devemos retornar um código de status 400 e um dicionário {“erro”:'aluno nao encontrado'}
No teste 007, tentamos criar dois alunos com a mesma id. Nesse caso, devemos retornar um código de status 400 e um dicionário {‘erro’:'id ja utilizada'}
No teste 008a, tento enviar um aluno sem nome via post. Nesse caso, devemos retornar um código de status 400 e um dicionário {‘erro’:'aluno sem nome'}
No teste 008b, tento editar um aluno, usando o verbo put, mas mando um dicionário sem nome. Nesse caso, devemos retornar um código de status 400 e um dicionário {“erro”:'aluno sem nome'}
Testes 100 a 109: Teremos as URLs análogas para professores.


'''

class TestStringMethods(unittest.TestCase):


    def test_000_alunos_retorna_lista(self):
        #pega a url /alunos, com o verbo get
        r = requests.get('http://localhost:5002/alunos')

        #o status code foi pagina nao encontrada?
        if r.status_code == 404:
            self.fail("voce nao definiu a pagina /alunos no seu server")

        try:
            obj_retornado = r.json()
            #r.json() é o jeito da biblioteca requests
            #de pegar o arquivo que veio e transformar
            #em lista ou dicionario.
            #Vou dar erro se isso nao for possivel
        except:
            self.fail("queria um json mas voce retornou outra coisa")

        #no caso, tem que ser uma lista
        self.assertEqual(type(obj_retornado),type([]))

    def test_001_adiciona_alunos(self):
        #criar dois alunos (usando post na url /alunos)
        r = requests.post('http://localhost:5002/alunos',json={'nome':'fernando','id':1})
        r = requests.post('http://localhost:5002/alunos',json={'nome':'roberto','id':2})
        
        #pego a lista de alunos (do mesmo jeito que no teste 0)
        r_lista = requests.get('http://localhost:5002/alunos')
        lista_retornada = r_lista.json()#le o arquivo que o servidor respondeu
                                        #e transforma num dict/lista de python

        #faço um for para garantir que as duas pessoas que eu criei 
        #aparecem
        achei_fernando = False
        achei_roberto = False
        for aluno in lista_retornada:
            if aluno['nome'] == 'fernando':
                achei_fernando = True
            if aluno['nome'] == 'roberto':
                achei_roberto = True
        
        #se algum desses "achei" nao for True, dou uma falha
        if not achei_fernando:
            self.fail('aluno fernando nao apareceu na lista de alunos')
        if not achei_roberto:
            self.fail('aluno roberto nao apareceu na lista de alunos')

    def test_002_aluno_por_id(self):
        #cria um aluno 'mario', com id 20
        r = requests.post('http://localhost:5002/alunos',json={'nome':'mario','id':20})

        #consulta a url /alunos/20, pra ver se o aluno está lá
        resposta = requests.get('http://localhost:5002/alunos/20')
        dict_retornado = resposta.json() #pego o dicionario retornado
        self.assertEqual(type(dict_retornado),dict)
        self.assertIn('nome',dict_retornado)#o dicionario dict_retornado, que veio do servidor, 
        #tem que ter a chave nome
        self.assertEqual(dict_retornado['nome'],'mario') # no dic, o nome tem que ser o 
                                                   # que eu mandei
                                                   # tem que ser mario


    #adiciona um aluno, mas depois reseta o servidor
    #e o aluno deve desaparecer
    def test_003_reseta(self):
        #criei um aluno, com post
        r = requests.post('http://localhost:5002/alunos',json={'nome':'cicero','id':29})
        #peguei a lista
        r_lista = requests.get('http://localhost:5002/alunos')
        #no momento, a lista tem que ter mais de um aluno
        self.assertTrue(len(r_lista.json()) > 0)

        #POST na url reseta: deveria apagar todos os dados do servidor
        r_reset = requests.post('http://localhost:5002/reseta')

        #estou verificando se a url reseta deu pau
        #se voce ainda nao definiu ela, esse cod status nao vai ser 200
        self.assertEqual(r_reset.status_code,200)

        #pego de novo a lista
        r_lista_depois = requests.get('http://localhost:5002/alunos')
        
        #e agora tem que ter 0 elementos
        self.assertEqual(len(r_lista_depois.json()),0)

    #esse teste adiciona 2 alunos, depois deleta 1
    #e verifica que o numero de alunos realmente diminuiu
    '''
    voce provavelmente vai querer usar o lista.remove
    >>> lista
    [10, 20, 'banana']
    >>> lista.remove('banana')
    >>> lista
    [10, 20]
    >>> lista.remove(10)
    >>> lista
    [20]'''
    def test_004_deleta(self):
        #apago tudo
        r_reset = requests.post('http://localhost:5002/reseta')
        self.assertEqual(r_reset.status_code,200)
        #crio 3 alunos
        requests.post('http://localhost:5002/alunos',json={'nome':'cicero','id':29})
        requests.post('http://localhost:5002/alunos',json={'nome':'lucas','id':28})
        requests.post('http://localhost:5002/alunos',json={'nome':'marta','id':27})
        #pego a lista completa
        r_lista = requests.get('http://localhost:5002/alunos')
        lista_retornada = r_lista.json()
        #a lista completa tem que ter 3 elementos
        self.assertEqual(len(lista_retornada),3)
        #faço um request com delete, pra deletar o aluno de id 28
        requests.delete('http://localhost:5002/alunos/28')
        #pego a lista de novo
        r_lista2 = requests.get('http://localhost:5002/alunos')
        lista_retornada2 = r_lista2.json()
        #e vejo se ficou só um elemento
        self.assertEqual(len(lista_retornada2),2) 

        acheiMarta = False
        acheiCicero = False
        for aluno in lista_retornada:
            if aluno['nome'] == 'marta':
                acheiMarta=True
            if aluno['nome'] == 'cicero':
                acheiCicero=True
        if not acheiMarta or not acheiCicero:
            self.fail("voce parece ter deletado o aluno errado!")

        requests.delete('http://localhost:5002/alunos/27')

        r_lista3 = requests.get('http://localhost:5002/alunos')
        lista_retornada3 = r_lista3.json()
        #e vejo se ficou só um elemento
        self.assertEqual(len(lista_retornada3),1) 

        if lista_retornada3[0]['nome'] == 'cicero':
            pass
        else:
            self.fail("voce parece ter deletado o aluno errado!")


    #cria um usuário, depois usa o verbo PUT
    #para alterar o nome do usuário
    def test_005_edita(self):
        #resetei
        r_reset = requests.post('http://localhost:5002/reseta')
        #verifiquei se o reset foi
        self.assertEqual(r_reset.status_code,200)

        #criei um aluno
        requests.post('http://localhost:5002/alunos',json={'nome':'lucas','id':28})
        #e peguei o dicionario dele
        r_antes = requests.get('http://localhost:5002/alunos/28')
        #o nome enviado foi lucas, o nome recebido tb
        self.assertEqual(r_antes.json()['nome'],'lucas')
        #vou editar. Vou mandar um novo dicionario p/ corrigir o dicionario
        #que já estava no 28 (note que só mandei o nome)
        #para isso, uso o verbo PUT
        requests.put('http://localhost:5002/alunos/28', json={'nome':'lucas mendes'})
        #pego o novo dicionario do aluno 28
        r_depois = requests.get('http://localhost:5002/alunos/28')
        #agora o nome deve ser lucas mendes
        self.assertEqual(r_depois.json()['nome'],'lucas mendes')
        #mas o id nao mudou
        self.assertEqual(r_depois.json()['id'],28)

    #tenta fazer GET, PUT e DELETE num aluno que nao existe
    def test_006a_id_inexistente_no_put(self):
        #reseto
        r_reset = requests.post('http://localhost:5002/reseta')
        #vejo se nao deu pau resetar
        self.assertEqual(r_reset.status_code,200)
        #estou tentando EDITAR um aluno que nao existe (verbo PUT)
        r = requests.put('http://localhost:5002/alunos/15',json={'nome':'bowser','id':15})
        #tem que dar erro 400 ou 404
        #ou seja, r.status_code tem que aparecer na lista [400,404]
        self.assertIn(r.status_code,[400,404])
        #qual a resposta que a linha abaixo pede?
        #um json, com o dicionario {"erro":"aluno nao encontrado"}
        self.assertEqual(r.json()['erro'],'aluno nao encontrado')
    

    def test_006b_id_inexistente_no_get(self):
        #reseto
        r_reset = requests.post('http://localhost:5002/reseta')
        #vejo se nao deu pau resetar
        self.assertEqual(r_reset.status_code,200)
        #agora faço o mesmo teste pro GET, a consulta por id
        r = requests.get('http://localhost:5002/alunos/15')
        self.assertIn(r.status_code,[400,404])
        #olhando pra essa linha debaixo, o que está especificado que o servidor deve retornar
        self.assertEqual(r.json()['erro'],'aluno nao encontrado')
        #                ------
        #                string json
        #                ----------------
        #                que representa um dicionario
        #                o dict tem a chave erro
        #                                 ----------------------
        #                                 o valor da chave erro
        
    def test_006c_id_inexistente_no_delete(self):
        #reseto
        r_reset = requests.post('http://localhost:5002/reseta')
        #vejo se nao deu pau resetar
        self.assertEqual(r_reset.status_code,200)
        r = requests.delete('http://localhost:5002/alunos/15')
        self.assertIn(r.status_code,[400,404])
        self.assertEqual(r.json()['erro'],'aluno nao encontrado')

        #404 usuário tentou acessar um recurso inexistente
        #400 usuário fez alguma besteira
        #toda vez que o servidor retorna 404, ele
        #poderia, se quisesse, retornar o erro MENOS INFORMATIVO
        #400. Talvez fosse sacanagem com o programador do outro
        #lado, mas nao seria mentira

    #tento criar 2 caras com a  mesma id
    def test_007_criar_com_id_ja_existente(self):

        #dou reseta e confiro que deu certo
        r_reset = requests.post('http://localhost:5002/reseta')
        self.assertEqual(r_reset.status_code,200)

        #crio o usuario bond e confiro
        r = requests.post('http://localhost:5002/alunos',json={'nome':'bond','id':7})
        self.assertEqual(r.status_code,200)

        #tento usar o mesmo id para outro usuário
        r = requests.post('http://localhost:5002/alunos',json={'nome':'james','id':7})
        # o erro é muito parecido com o do teste anterior
        self.assertEqual(r.status_code,400)
        self.assertEqual(r.json()['erro'],'id ja utilizada')


    #cria alunos sem nome, o que tem que dar erro
    def test_008a_post_sem_nome(self):
        r_reset = requests.post('http://localhost:5002/reseta')
        self.assertEqual(r_reset.status_code,200)

        #tentei criar um aluno, sem enviar um nome
        r = requests.post('http://localhost:5002/alunos',json={'id':8})
        self.assertEqual(r.status_code,400)
        self.assertEqual(r.json()['erro'],'aluno sem nome')
    
    #tenta editar alunos sem passar nome, o que também
    #tem que dar erro (se vc nao mudar o nome, vai mudar o que?)
    def test_008b_put_sem_nome(self):
        r_reset = requests.post('http://localhost:5002/reseta')
        self.assertEqual(r_reset.status_code,200)

        #criei um aluno sem problemas
        r = requests.post('http://localhost:5002/alunos',json={'nome':'maximus','id':7})
        self.assertEqual(r.status_code,200)

        #mas tentei editar ele sem mandar o nome
        r = requests.put('http://localhost:5002/alunos/7',json={'id':7})
        self.assertEqual(r.status_code,400)
        self.assertEqual(r.json()['erro'],'aluno sem nome')
    

    
    def test_100_professores_retorna_lista(self):
        r = requests.get('http://localhost:5002/professores')
        self.assertEqual(type(r.json()),type([]))
    
    def test_100b_nao_confundir_professor_e_aluno(self):
        r_reset = requests.post('http://localhost:5002/reseta')
        r = requests.post('http://localhost:5002/alunos',json={'nome':'fernando','id':1})
        self.assertEqual(r.status_code,200)
        r = requests.post('http://localhost:5002/alunos',json={'nome':'roberto','id':2})
        self.assertEqual(r.status_code,200)
        r_lista = requests.get('http://localhost:5002/professores')
        self.assertEqual(len(r_lista.json()),0)
        r_lista_alunos = requests.get('http://localhost:5002/alunos')
        self.assertEqual(len(r_lista_alunos.json()),2)

    def test_101_adiciona_professores(self):
        r = requests.post('http://localhost:5002/professores',json={'nome':'fernando','id':1})
        r = requests.post('http://localhost:5002/professores',json={'nome':'roberto','id':2})
        r_lista = requests.get('http://localhost:5002/professores')
        achei_fernando = False
        achei_roberto = False
        for professor in r_lista.json():
            if professor['nome'] == 'fernando':
                achei_fernando = True
            if professor['nome'] == 'roberto':
                achei_roberto = True
        if not achei_fernando:
            self.fail('professor fernando nao apareceu na lista de professores')
        if not achei_roberto:
            self.fail('professor roberto nao apareceu na lista de professores')

    def test_102_professores_por_id(self):
        r = requests.post('http://localhost:5002/professores',json={'nome':'mario','id':20})
        r_lista = requests.get('http://localhost:5002/professores/20')
        self.assertEqual(r_lista.json()['nome'],'mario')


    
    def test_103_adiciona_e_reseta(self):
        r = requests.post('http://localhost:5002/professores',json={'nome':'cicero','id':29})
        r_lista = requests.get('http://localhost:5002/professores')
        self.assertTrue(len(r_lista.json()) > 0)
        r_reset = requests.post('http://localhost:5002/reseta')
        self.assertEqual(r_reset.status_code,200)
        r_lista_depois = requests.get('http://localhost:5002/professores')
        self.assertEqual(len(r_lista_depois.json()),0)

    def test_104_deleta(self):
        r_reset = requests.post('http://localhost:5002/reseta')
        self.assertEqual(r_reset.status_code,200)
        requests.post('http://localhost:5002/professores',json={'nome':'cicero','id':29})
        requests.post('http://localhost:5002/professores',json={'nome':'lucas','id':28})
        r_lista = requests.get('http://localhost:5002/professores')
        self.assertEqual(len(r_lista.json()),2)
        requests.delete('http://localhost:5002/professores/28')
        r_lista = requests.get('http://localhost:5002/professores')
        self.assertEqual(len(r_lista.json()),1)
    
    def test_105_edita(self):
        r_reset = requests.post('http://localhost:5002/reseta')
        self.assertEqual(r_reset.status_code,200)
        requests.post('http://localhost:5002/professores',json={'nome':'lucas','id':28})
        r_antes = requests.get('http://localhost:5002/professores/28')
        self.assertEqual(r_antes.json()['nome'],'lucas')
        requests.put('http://localhost:5002/professores/28', json={'nome':'lucas mendes'})
        r_depois = requests.get('http://localhost:5002/professores/28')
        self.assertEqual(r_depois.json()['nome'],'lucas mendes')

    def test_106_id_inexistente(self):
        r_reset = requests.post('http://localhost:5002/reseta')
        self.assertEqual(r_reset.status_code,200)
        r = requests.put('http://localhost:5002/professores/15',json={'nome':'bowser','id':15})
        self.assertEqual(r.status_code,400)
        self.assertEqual(r.json()['erro'],'professor nao encontrado')
        r = requests.get('http://localhost:5002/professores/15')
        self.assertEqual(r.status_code,400)
        self.assertEqual(r.json()['erro'],'professor nao encontrado')
        r = requests.delete('http://localhost:5002/professores/15')
        self.assertEqual(r.status_code,400)
        self.assertEqual(r.json()['erro'],'professor nao encontrado')

    def test_107_criar_com_id_ja_existente(self):
        r_reset = requests.post('http://localhost:5002/reseta')
        self.assertEqual(r_reset.status_code,200)
        r = requests.post('http://localhost:5002/professores',json={'nome':'bond','id':7})
        self.assertEqual(r.status_code,200)
        r = requests.post('http://localhost:5002/professores',json={'nome':'james','id':7})
        self.assertEqual(r.status_code,400)
        self.assertEqual(r.json()['erro'],'id ja utilizada')

    def test_108_post_ou_put_sem_nome(self):
        r_reset = requests.post('http://localhost:5002/reseta')
        self.assertEqual(r_reset.status_code,200)
        r = requests.post('http://localhost:5002/professores',json={'id':8})
        self.assertEqual(r.status_code,400)
        self.assertEqual(r.json()['erro'],'professor sem nome')
        r = requests.post('http://localhost:5002/professores',json={'nome':'maximus','id':7})
        self.assertEqual(r.status_code,200)
        r = requests.put('http://localhost:5002/professores/7',json={'id':7})
        self.assertEqual(r.status_code,400)
        self.assertEqual(r.json()['erro'],'professor sem nome')

    def test_109_nao_confundir_professor_e_aluno(self):
        r_reset = requests.post('http://localhost:5002/reseta')
        r = requests.post('http://localhost:5002/professores',json={'nome':'fernando','id':1})
        self.assertEqual(r.status_code,200)
        r = requests.post('http://localhost:5002/professores',json={'nome':'roberto','id':2})
        self.assertEqual(r.status_code,200)
        r_lista = requests.get('http://localhost:5002/professores')
        self.assertEqual(len(r_lista.json()),2)
        r_lista_alunos = requests.get('http://localhost:5002/alunos')
        self.assertEqual(len(r_lista_alunos.json()),0)




        


        





    

    


def runTests():
        suite = unittest.defaultTestLoader.loadTestsFromTestCase(TestStringMethods)
        unittest.TextTestRunner(verbosity=2,failfast=True).run(suite)


if __name__ == '__main__':
    runTests()
