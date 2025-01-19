import os
from datetime import timedelta

# Carrega variáveis de ambiente do arquivo .env
from dotenv import load_dotenv
load_dotenv()

class Config:
    """Configurações base do projeto."""
    
    # Configurações do Flask
    SECRET_KEY = os.getenv('SECRET_KEY', 'chave-secreta-padrao')
    FLASK_APP = os.getenv('FLASK_APP', 'run.py')
    FLASK_ENV = os.getenv('FLASK_ENV', 'development')
    
    # Configurações do Banco de Dados
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///gymflow.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Configurações de Upload
    UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER', 'uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max-limit
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    
    # Configurações do JWT
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'jwt-chave-secreta-padrao')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
    
    # Configurações de Email
    MAIL_SERVER = os.getenv('MAIL_SERVER', 'smtp.gmail.com')
    MAIL_PORT = int(os.getenv('MAIL_PORT', 587))
    MAIL_USE_TLS = os.getenv('MAIL_USE_TLS', 'true').lower() == 'true'
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.getenv('MAIL_DEFAULT_SENDER', 'noreply@gymflow.com')
    
    # Configurações de Paginação
    ITEMS_PER_PAGE = 10
    
    # Configurações de Cache
    CACHE_TYPE = 'simple'
    CACHE_DEFAULT_TIMEOUT = 300  # 5 minutos
    
    # Configurações de Sessão
    SESSION_TYPE = 'filesystem'
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)
    
    # Configurações de Segurança
    SECURITY_PASSWORD_SALT = os.getenv('SECURITY_PASSWORD_SALT', 'salt-padrao')
    SECURITY_PASSWORD_HASH = 'pbkdf2_sha512'
    SECURITY_PASSWORD_LENGTH_MIN = 8
    
    # Configurações de CORS
    CORS_ORIGINS = ['http://localhost:5000']
    CORS_SUPPORTS_CREDENTIALS = True


class DevelopmentConfig(Config):
    """Configurações para ambiente de desenvolvimento."""
    
    DEBUG = True
    TESTING = False
    
    # Configurações específicas para desenvolvimento
    SQLALCHEMY_ECHO = True
    TEMPLATES_AUTO_RELOAD = True
    SEND_FILE_MAX_AGE_DEFAULT = 0


class TestingConfig(Config):
    """Configurações para ambiente de testes."""
    
    DEBUG = False
    TESTING = True
    
    # Usa banco de dados em memória para testes
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    
    # Desativa proteção CSRF para testes
    WTF_CSRF_ENABLED = False


class ProductionConfig(Config):
    """Configurações para ambiente de produção."""
    
    DEBUG = False
    TESTING = False
    
    # Configurações específicas para produção
    SQLALCHEMY_ECHO = False
    PREFERRED_URL_SCHEME = 'https'
    
    # Configurações de segurança para produção
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_SECURE = True
    REMEMBER_COOKIE_HTTPONLY = True


# Dicionário com as configurações disponíveis
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}

# Função para obter a configuração atual
def get_config():
    """Retorna a configuração baseada no ambiente."""
    env = os.getenv('FLASK_ENV', 'development')
    return config.get(env, config['default']) 