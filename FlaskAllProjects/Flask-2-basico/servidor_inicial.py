
from flask import Flask, request
import model_aluno_professor as model


app = Flask(__name__) 

		
@app.route("/") 
def hello():
        print("rodei mesmo") 
        return "Hello World!"

@app.route("/alunos", methods=["GET"])
def alunos():
    print("lista de todos os alunos")
    return model.lista_alunos()

@app.route("/alunos/<int:nAluno>", methods=["GET"]) 
def alunoPorId(nAluno):
    try:
        return model.aluno_por_id(nAluno)
    except model.AlunoNaoEncontrado:
        return ( {"erro":'aluno nao encontrado'}, 400)

@app.route("/alunos", methods=["POST"])
def cria_aluno():
    dict = request.json
    dict['id'] = int (dict['id'])
    model.adiciona_aluno(dict)
    return model.lista_alunos()

@app.route("/reseta", methods=["POST","DELETE"])
def reseta():
    model.apaga_tudo()
    return "resetado" 

if __name__ == '__main__':
        app.run(host = 'localhost', port = 5002, debug = True)