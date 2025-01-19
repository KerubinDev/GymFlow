from flask import Flask
from flask_cors import CORS
from flask_login import LoginManager
from .models import db
from .routes import rotas
from .config import Config

login_manager = LoginManager()

def create_app():
    """Cria e configura a aplicação Flask"""
    app = Flask(__name__, 
                template_folder='../templates',
                static_folder='../static')
    
    app.config.from_object(Config)
    
    # Inicializa extensões
    CORS(app)
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'rotas.login'
    
    # Registra blueprints
    app.register_blueprint(rotas)
    
    @login_manager.user_loader
    def load_user(user_id):
        from .models import Usuario
        return Usuario.query.get(int(user_id))
    
    return app 