dados = {
    "alunos": [
        {"nome": "lucas", "id": 15},
        {"nome": "cicero", "id": 29},
    ],
    "professores": []
}

class AlunoNaoEncontrado(Exception):
    pass

def aluno_por_id(id_aluno):
    lista_alunos = dados['alunos']
    for dicionario in lista_alunos:
        if dicionario['id'] == id_aluno:
            return dicionario
    raise AlunoNaoEncontrado

def listar_alunos():
    return dados['alunos']

def adicionar_aluno(aluno):
    dados['alunos'].append(aluno)

def atualizar_aluno(id_aluno, novos_dados):
    aluno = aluno_por_id(id_aluno)
    aluno.update(novos_dados)

def excluir_aluno(id_aluno):
    aluno = aluno_por_id(id_aluno)
    dados['alunos'].remove(aluno)
