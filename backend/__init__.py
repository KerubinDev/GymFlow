"""Inicialização da aplicação Flask."""

import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_caching import Cache
from flask_talisman import Talisman

# Importa configurações
from .config import get_config

# Inicializa extensões
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
mail = Mail()
jwt = JWTManager()
cache = Cache()


def create_app(config_name=None):
    """
    Cria e configura a aplicação Flask.
    
    Args:
        config_name: Nome da configuração a ser usada
        
    Returns:
        Flask: Aplicação Flask configurada
    """
    app = Flask(__name__)
    
    # Carrega configurações
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
    
    # Registra blueprints
    from .routes import rotas
    app.register_blueprint(rotas)
    
    # Cria diretórios necessários
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    
    # Configura função de carregamento de usuário
    from .models import Usuario
    
    @login_manager.user_loader
    def load_user(user_id):
        """Carrega usuário pelo ID."""
        return Usuario.query.get(int(user_id))
    
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
    
    return app 