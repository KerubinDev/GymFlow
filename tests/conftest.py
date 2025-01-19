"""Configurações para os testes."""

import os
import tempfile
import pytest
from backend import create_app
from backend.models import db


@pytest.fixture(scope='session')
def app():
    """Fixture que cria uma instância do app para testes."""
    # Cria um arquivo temporário para o banco de dados
    db_fd, db_path = tempfile.mkstemp()
    
    # Configura o app para testes
    app = create_app('testing')
    app.config.update({
        'SQLALCHEMY_DATABASE_URI': f'sqlite:///{db_path}',
        'TESTING': True,
        'WTF_CSRF_ENABLED': False,
        'UPLOAD_FOLDER': tempfile.mkdtemp(),
        'JWT_SECRET_KEY': 'chave-secreta-teste',
        'MAIL_SUPPRESS_SEND': True
    })
    
    # Cria o contexto do app e o banco de dados
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()
    
    # Limpa os arquivos temporários
    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture(scope='session')
def client(app):
    """Fixture que cria um cliente de teste."""
    return app.test_client()


@pytest.fixture(scope='session')
def runner(app):
    """Fixture que cria um runner de comandos CLI."""
    return app.test_cli_runner()


@pytest.fixture(scope='function')
def session(app):
    """Fixture que cria uma sessão de banco de dados para testes."""
    with app.app_context():
        connection = db.engine.connect()
        transaction = connection.begin()
        
        options = dict(bind=connection, binds={})
        session = db.create_scoped_session(options=options)
        
        db.session = session
        
        yield session
        
        transaction.rollback()
        connection.close()
        session.remove()


@pytest.fixture(scope='function')
def auth_headers(app, client):
    """Fixture que cria headers de autenticação para testes."""
    from backend.models import Usuario
    
    with app.app_context():
        # Cria um usuário gerente
        gerente = Usuario(
            nome='Gerente Teste',
            email='gerente@teste.com',
            tipo='gerente'
        )
        gerente.senha = 'senha123'
        db.session.add(gerente)
        
        # Cria um usuário professor
        professor = Usuario(
            nome='Professor Teste',
            email='professor@teste.com',
            tipo='professor'
        )
        professor.senha = 'senha123'
        db.session.add(professor)
        
        # Cria um usuário recepcionista
        recepcionista = Usuario(
            nome='Recepcionista Teste',
            email='recepcionista@teste.com',
            tipo='recepcionista'
        )
        recepcionista.senha = 'senha123'
        db.session.add(recepcionista)
        
        db.session.commit()
        
        # Obtém tokens para cada tipo de usuário
        tokens = {}
        for email in ['gerente@teste.com', 'professor@teste.com', 'recepcionista@teste.com']:
            response = client.post('/api/login', json={
                'email': email,
                'senha': 'senha123'
            })
            token = response.json['token']
            tipo = email.split('@')[0]
            tokens[tipo] = {'Authorization': f'Bearer {token}'}
        
        return tokens 