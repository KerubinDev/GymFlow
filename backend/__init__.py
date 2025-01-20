"""Inicialização da aplicação Flask."""

import os
from datetime import datetime, timedelta
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_caching import Cache
from flask_talisman import Talisman
from werkzeug.security import generate_password_hash

# Inicializa extensões
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
mail = Mail()
jwt = JWTManager()
cache = Cache()

def criar_dados_exemplo():
    """Cria dados de exemplo no banco de dados."""
    from .models import Usuario, Professor, Aluno, Plano, Treino, Exercicio, Turma, Pagamento
    
    # Verifica se já existem dados
    if Usuario.query.first():
        return
    
    try:
        # Criar usuário gerente
        gerente = Usuario(
            nome='Administrador',
            email='admin@gymflow.com',
            tipo='gerente',
            status='ativo'
        )
        gerente.senha = 'admin123'
        db.session.add(gerente)
        db.session.flush()
        
        # Criar usuário professor
        usuario_professor = Usuario(
            nome='João Silva',
            email='joao@gymflow.com',
            tipo='professor',
            status='ativo'
        )
        usuario_professor.senha = 'prof123'
        db.session.add(usuario_professor)
        db.session.flush()
        
        # Criar professor
        professor = Professor(
            usuario_id=usuario_professor.id,
            especialidade='Musculação, Funcional',
            horario_disponivel='Segunda a Sexta, 8h às 17h',
            status='ativo'
        )
        db.session.add(professor)
        db.session.flush()
        
        # Criar plano
        plano = Plano(
            nome='Plano Básico',
            descricao='Acesso à academia e aulas em grupo',
            valor=100.00,
            duracao_meses=1,
            ativo=True
        )
        db.session.add(plano)
        db.session.flush()
        
        # Criar aluno
        aluno = Aluno(
            nome='Maria Santos',
            email='maria@email.com',
            cpf='123.456.789-00',
            telefone='(11) 98765-4321',
            data_nascimento=datetime(1990, 1, 1).date(),
            endereco='Rua Exemplo, 123',
            altura=1.65,
            peso=65.0,
            objetivo='hipertrofia',
            plano_id=plano.id,
            status='ativo'
        )
        db.session.add(aluno)
        db.session.flush()
        
        # Criar exercícios
        exercicios = [
            Exercicio(
                nome='Supino Reto',
                descricao='Exercício para peitoral',
                grupo_muscular='Peitoral',
                equipamento='Barra e banco',
                nivel='intermediario'
            ),
            Exercicio(
                nome='Agachamento',
                descricao='Exercício para pernas',
                grupo_muscular='Quadríceps',
                equipamento='Barra',
                nivel='intermediario'
            ),
            Exercicio(
                nome='Puxada Alta',
                descricao='Exercício para costas',
                grupo_muscular='Dorsal',
                equipamento='Puxador',
                nivel='iniciante'
            )
        ]
        for exercicio in exercicios:
            db.session.add(exercicio)
        db.session.flush()
        
        # Criar treino
        treino = Treino(
            aluno_id=aluno.id,
            professor_id=professor.id,
            tipo='musculacao',
            data_inicio=datetime.now().date(),
            status='ativo',
            observacoes='Treino inicial',
            exercicios=[{
                'exercicio_id': exercicios[0].id,
                'series': '3',
                'repeticoes': '12',
                'carga': '20',
                'observacoes': 'Manter forma correta'
            }]
        )
        db.session.add(treino)
        db.session.flush()
        
        # Criar turma
        turma = Turma(
            modalidade='Musculação',
            professor_id=professor.id,
            dia_semana='Segunda',
            horario_inicio='08:00',
            horario_fim='09:00',
            capacidade_maxima=15,
            nivel='iniciante',
            descricao='Aula de musculação para iniciantes'
        )
        db.session.add(turma)
        db.session.flush()
        
        # Criar pagamento
        pagamento = Pagamento(
            aluno_id=aluno.id,
            mes_referencia=datetime.now().strftime('%Y-%m'),
            status='pago',
            data_pagamento=datetime.now(),
            observacoes='Pagamento do plano básico'
        )
        db.session.add(pagamento)
        
        # Commit das alterações
        db.session.commit()
        print("Dados de exemplo criados com sucesso!")
        
    except Exception as e:
        db.session.rollback()
        print(f"Erro ao criar dados de exemplo: {str(e)}")

def create_app(config_name=None):
    """
    Cria e configura a aplicação Flask.
    
    Args:
        config_name: Nome da configuração a ser usada
        
    Returns:
        Flask: Aplicação Flask configurada
    """
    app = Flask(__name__, 
                template_folder='../templates',  # Define o caminho para os templates
                static_folder='../static')       # Define o caminho para os arquivos estáticos
    
    # Carrega configurações
    from .config import get_config
    config = get_config()
    app.config.from_object(config)
    
    # Configura extensões
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    mail.init_app(app)
    jwt.init_app(app)
    cache.init_app(app)
    CORS(app)
    Talisman(app, content_security_policy=None)
    
    # Configura login
    login_manager.login_view = 'rotas.login'
    login_manager.login_message = 'Por favor, faça login para acessar esta página.'
    
    # Cria diretórios necessários
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    
    # Configura função de carregamento de usuário
    from .models import Usuario
    
    @login_manager.user_loader
    def load_user(user_id):
        """Carrega usuário pelo ID."""
        return Usuario.query.get(int(user_id))
    
    # Adiciona contexto global para templates
    @app.context_processor
    def utility_processor():
        return {
            'datetime': datetime,
            'str': str,
            'len': len
        }
    
    # Registra blueprints
    from .routes import rotas
    app.register_blueprint(rotas)
    
    # Configura handlers de erro
    @app.errorhandler(404)
    def not_found_error(error):
        """Handler para erro 404."""
        return {'erro': 'Recurso não encontrado'}, 404
    
    @app.errorhandler(500)
    def internal_error(error):
        """Handler para erro 500."""
        db.session.rollback()
        return {'erro': 'Erro interno do servidor'}, 500
    
    # Inicializa banco de dados
    with app.app_context():
        from .models import init_db
        init_db()
        
        # Cria dados de exemplo
        criar_dados_exemplo()
    
    return app 