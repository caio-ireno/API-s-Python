from flask_restx import Api

# Inicializa o objeto API do Swagger
api = Api(
    version="1.0",
    title="API de Gestão Escolar",
    description="Documentação da API para Alunos, Professores e Turmas",
    doc="/docs",
    mask_swagger=False,  # Desativa o X-Fields no Swagger,
    prefix="/api"
)
