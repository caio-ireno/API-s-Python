from swagger.swagger_config import configure_swagger
import pytest
import os
import sys
from config import app, db
from alunos.alunos_routes import alunos_blueprint
from turma.turma_routes import turmas_blueprint
from professor.professor_routes import professores_blueprint

app.register_blueprint(alunos_blueprint, url_prefix='/api')
app.register_blueprint(turmas_blueprint, url_prefix='/api')
app.register_blueprint(professores_blueprint, url_prefix='/api')

configure_swagger(app)

with app.app_context():
    db.create_all()

def run_tests():
    os.environ['FLASK_ENV'] = 'testing'
    # Executa os testes e captura o resultado
    result = pytest.main(['--maxfail=1', '--disable-warnings', '--tb=short'])
    return result

if __name__ == '__main__':
    result = run_tests()
    
    if result != 0:  # Se algum teste falhar, não inicie o servidor
        sys.exit("Testes falharam. A aplicação não será iniciada.")
    
    app.run(host=app.config["HOST"], port=app.config['PORT'], debug=app.config['DEBUG'])
