"""Testes unitários para as rotas da API."""

import pytest
import json
from datetime import datetime, date
from backend import create_app
from backend.models import (
    Usuario, Aluno, Plano, Treino, Exercicio,
    Turma, MatriculaTurma, Pagamento, Presenca,
    db
)


@pytest.fixture
def app():
    """Fixture que cria uma instância do app para testes."""
    app = create_app('testing')
    
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    """Fixture que cria um cliente de teste."""
    return app.test_client()


@pytest.fixture
def token_gerente(app, client):
    """Fixture que cria um token de gerente para testes."""
    with app.app_context():
        usuario = Usuario(
            nome='Gerente Teste',
            email='gerente@teste.com',
            tipo='gerente'
        )
        usuario.senha = 'senha123'
        db.session.add(usuario)
        db.session.commit()
        
        response = client.post('/api/login', json={
            'email': 'gerente@teste.com',
            'senha': 'senha123'
        })
        return json.loads(response.data)['token']


@pytest.fixture
def token_professor(app, client):
    """Fixture que cria um token de professor para testes."""
    with app.app_context():
        usuario = Usuario(
            nome='Professor Teste',
            email='professor@teste.com',
            tipo='professor'
        )
        usuario.senha = 'senha123'
        db.session.add(usuario)
        db.session.commit()
        
        response = client.post('/api/login', json={
            'email': 'professor@teste.com',
            'senha': 'senha123'
        })
        return json.loads(response.data)['token']


def test_login(client):
    """Testa o login de usuários."""
    # Testa login com credenciais inválidas
    response = client.post('/api/login', json={
        'email': 'invalido@teste.com',
        'senha': 'senha123'
    })
    assert response.status_code == 401
    
    # Testa login com senha incorreta
    response = client.post('/api/login', json={
        'email': 'gerente@teste.com',
        'senha': 'senha_errada'
    })
    assert response.status_code == 401
    
    # Testa login com sucesso
    response = client.post('/api/login', json={
        'email': 'gerente@teste.com',
        'senha': 'senha123'
    })
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'token' in data


def test_criar_usuario(client, token_gerente):
    """Testa a criação de usuários."""
    # Testa criação sem autenticação
    response = client.post('/api/usuarios', json={
        'nome': 'Novo Usuario',
        'email': 'novo@teste.com',
        'senha': 'senha123',
        'tipo': 'professor'
    })
    assert response.status_code == 401
    
    # Testa criação com sucesso
    response = client.post(
        '/api/usuarios',
        json={
            'nome': 'Novo Usuario',
            'email': 'novo@teste.com',
            'senha': 'senha123',
            'tipo': 'professor'
        },
        headers={'Authorization': f'Bearer {token_gerente}'}
    )
    assert response.status_code == 201
    data = json.loads(response.data)
    assert data['nome'] == 'Novo Usuario'
    assert data['email'] == 'novo@teste.com'
    assert data['tipo'] == 'professor'


def test_criar_aluno(client, token_gerente, app):
    """Testa a criação de alunos."""
    with app.app_context():
        # Cria um plano para o teste
        plano = Plano(
            nome='Plano Teste',
            valor=100.0,
            duracao_meses=1,
            status='ativo'
        )
        db.session.add(plano)
        db.session.commit()
        
        # Testa criação sem autenticação
        response = client.post('/api/alunos', json={
            'nome': 'Novo Aluno',
            'email': 'aluno@teste.com',
            'cpf': '123.456.789-09',
            'telefone': '(11) 98765-4321',
            'data_nascimento': '2000-01-01',
            'plano_id': plano.id
        })
        assert response.status_code == 401
        
        # Testa criação com sucesso
        response = client.post(
            '/api/alunos',
            json={
                'nome': 'Novo Aluno',
                'email': 'aluno@teste.com',
                'cpf': '123.456.789-09',
                'telefone': '(11) 98765-4321',
                'data_nascimento': '2000-01-01',
                'plano_id': plano.id
            },
            headers={'Authorization': f'Bearer {token_gerente}'}
        )
        assert response.status_code == 201
        data = json.loads(response.data)
        assert data['nome'] == 'Novo Aluno'
        assert data['email'] == 'aluno@teste.com'
        assert data['cpf'] == '123.456.789-09'


def test_criar_treino(client, token_professor, app):
    """Testa a criação de treinos."""
    with app.app_context():
        # Cria um aluno para o teste
        plano = Plano(
            nome='Plano Teste',
            valor=100.0,
            duracao_meses=1,
            status='ativo'
        )
        db.session.add(plano)
        
        aluno = Aluno(
            nome='Aluno Teste',
            email='aluno@teste.com',
            cpf='123.456.789-09',
            telefone='(11) 98765-4321',
            data_nascimento=date(2000, 1, 1),
            plano=plano,
            status='ativo'
        )
        db.session.add(aluno)
        db.session.commit()
        
        # Testa criação sem autenticação
        response = client.post('/api/treinos', json={
            'aluno_id': aluno.id,
            'tipo': 'musculacao',
            'exercicios': [
                {
                    'nome': 'Supino',
                    'series': 3,
                    'repeticoes': 12,
                    'carga': 20.0,
                    'ordem': 1
                }
            ]
        })
        assert response.status_code == 401
        
        # Testa criação com sucesso
        response = client.post(
            '/api/treinos',
            json={
                'aluno_id': aluno.id,
                'tipo': 'musculacao',
                'exercicios': [
                    {
                        'nome': 'Supino',
                        'series': 3,
                        'repeticoes': 12,
                        'carga': 20.0,
                        'ordem': 1
                    }
                ]
            },
            headers={'Authorization': f'Bearer {token_professor}'}
        )
        assert response.status_code == 201
        data = json.loads(response.data)
        assert data['tipo'] == 'musculacao'
        assert len(data['exercicios']) == 1


def test_criar_turma(client, token_professor, app):
    """Testa a criação de turmas."""
    # Testa criação sem autenticação
    response = client.post('/api/turmas', json={
        'modalidade': 'musculacao',
        'nivel': 'iniciante',
        'dia_semana': 1,
        'horario_inicio': '08:00',
        'horario_fim': '09:00',
        'capacidade_maxima': 20
    })
    assert response.status_code == 401
    
    # Testa criação com sucesso
    response = client.post(
        '/api/turmas',
        json={
            'modalidade': 'musculacao',
            'nivel': 'iniciante',
            'dia_semana': 1,
            'horario_inicio': '08:00',
            'horario_fim': '09:00',
            'capacidade_maxima': 20
        },
        headers={'Authorization': f'Bearer {token_professor}'}
    )
    assert response.status_code == 201
    data = json.loads(response.data)
    assert data['modalidade'] == 'musculacao'
    assert data['nivel'] == 'iniciante'
    assert data['capacidade_maxima'] == 20


def test_registrar_pagamento(client, token_gerente, app):
    """Testa o registro de pagamentos."""
    with app.app_context():
        # Cria um aluno para o teste
        plano = Plano(
            nome='Plano Teste',
            valor=100.0,
            duracao_meses=1,
            status='ativo'
        )
        db.session.add(plano)
        
        aluno = Aluno(
            nome='Aluno Teste',
            email='aluno@teste.com',
            cpf='123.456.789-09',
            telefone='(11) 98765-4321',
            data_nascimento=date(2000, 1, 1),
            plano=plano,
            status='ativo'
        )
        db.session.add(aluno)
        db.session.commit()
        
        # Testa registro sem autenticação
        response = client.post('/api/pagamentos', json={
            'aluno_id': aluno.id,
            'valor': 100.0,
            'forma_pagamento': 'dinheiro'
        })
        assert response.status_code == 401
        
        # Testa registro com sucesso
        response = client.post(
            '/api/pagamentos',
            json={
                'aluno_id': aluno.id,
                'valor': 100.0,
                'forma_pagamento': 'dinheiro'
            },
            headers={'Authorization': f'Bearer {token_gerente}'}
        )
        assert response.status_code == 201
        data = json.loads(response.data)
        assert data['valor'] == 100.0
        assert data['forma_pagamento'] == 'dinheiro'
        assert data['status'] == 'pago'


def test_registrar_presenca(client, token_professor, app):
    """Testa o registro de presenças."""
    with app.app_context():
        # Cria aluno e turma para o teste
        plano = Plano(
            nome='Plano Teste',
            valor=100.0,
            duracao_meses=1,
            status='ativo'
        )
        db.session.add(plano)
        
        aluno = Aluno(
            nome='Aluno Teste',
            email='aluno@teste.com',
            cpf='123.456.789-09',
            telefone='(11) 98765-4321',
            data_nascimento=date(2000, 1, 1),
            plano=plano,
            status='ativo'
        )
        db.session.add(aluno)
        
        usuario = Usuario.query.filter_by(email='professor@teste.com').first()
        turma = Turma(
            professor=usuario,
            modalidade='musculacao',
            nivel='iniciante',
            dia_semana=1,
            horario_inicio=datetime.strptime('08:00', '%H:%M').time(),
            horario_fim=datetime.strptime('09:00', '%H:%M').time(),
            capacidade_maxima=20,
            status='ativa'
        )
        db.session.add(turma)
        
        matricula = MatriculaTurma(
            aluno=aluno,
            turma=turma,
            status='ativa'
        )
        db.session.add(matricula)
        db.session.commit()
        
        # Testa registro sem autenticação
        response = client.post('/api/presencas', json={
            'aluno_id': aluno.id,
            'turma_id': turma.id,
            'tipo': 'entrada'
        })
        assert response.status_code == 401
        
        # Testa registro com sucesso
        response = client.post(
            '/api/presencas',
            json={
                'aluno_id': aluno.id,
                'turma_id': turma.id,
                'tipo': 'entrada'
            },
            headers={'Authorization': f'Bearer {token_professor}'}
        )
        assert response.status_code == 201
        data = json.loads(response.data)
        assert data['tipo'] == 'entrada' 