from flask import Blueprint, request, jsonify,render_template,redirect, url_for
from datetime import datetime
from .alunos_model import AlunoNaoEncontrado, listar_alunos, aluno_por_id, adicionar_aluno, atualizar_aluno, excluir_aluno
from turma.turma_model import Turma, listar_turmas
from config import db

alunos_blueprint = Blueprint('alunos', __name__)

@alunos_blueprint.route('/alunos', methods=['GET'])
def get_alunos():
    aluno = listar_alunos()
    return jsonify(aluno)
    
@alunos_blueprint.route('/alunos/<int:id_aluno>', methods=['GET'])
def get_aluno(id_aluno):
    try:
        aluno = aluno_por_id(id_aluno)
        turma = Turma.query.get(aluno['turma_id'])
        if(turma is None):
            return jsonify({'message':'Turma não encontrada'}),404
        return jsonify({"aluno":aluno,"turma":turma.to_dict()})
    except AlunoNaoEncontrado:
        return jsonify({'message': 'Aluno não encontrado'}), 404


@alunos_blueprint.route('/alunos', methods=['POST'])
def create_aluno():
    try:
        data = request.json
        print(f"Dados recebidos: {data}")
        response, status_code = adicionar_aluno(data)
        return jsonify(response), status_code

    except Exception as e:
        print(f"Erro na rota /alunos: {str(e)}")
        return jsonify({"error": "Erro interno no servidor"}), 500

@alunos_blueprint.route('/alunos/<int:id_aluno>', methods=['PUT'])
def update_aluno(id_aluno):
        data = request.json
        try:
            aluno = aluno_por_id(id_aluno)
            if not aluno:
                return jsonify({'message': 'Aluno não encontrado'}), 404
            atualizar_aluno(id_aluno, data)
            
            return jsonify(data),200
        except AlunoNaoEncontrado:
            return jsonify({'message': 'Aluno não encontrado'}), 404
   
@alunos_blueprint.route('/alunos/<int:id_aluno>', methods=['DELETE'])
def delete_aluno(id_aluno):
        try:
            excluir_aluno(id_aluno)
            return jsonify({'message': 'Aluno excluído com sucesso '}),200
        except AlunoNaoEncontrado:
            return jsonify({'message': 'Aluno não encontrado'}), 404