"""Testes unitários para os modelos do sistema."""

import pytest
from datetime import datetime, date
from backend.models import (
    Usuario, Aluno, Plano, Treino, Exercicio,
    Turma, MatriculaTurma, Pagamento, Presenca
)


@pytest.fixture
def usuario():
    """Fixture que cria um usuário para testes."""
    usuario = Usuario(
        nome='Teste',
        email='teste@teste.com',
        tipo='gerente'
    )
    usuario.senha = 'senha123'
    return usuario


@pytest.fixture
def plano():
    """Fixture que cria um plano para testes."""
    return Plano(
        nome='Plano Teste',
        valor=100.0,
        duracao_meses=1,
        status='ativo'
    )


@pytest.fixture
def aluno(plano):
    """Fixture que cria um aluno para testes."""
    return Aluno(
        nome='Aluno Teste',
        email='aluno@teste.com',
        cpf='123.456.789-00',
        telefone='(11) 98765-4321',
        data_nascimento=date(2000, 1, 1),
        plano=plano,
        status='ativo'
    )


def test_criar_usuario(usuario):
    """Testa a criação de um usuário."""
    assert usuario.nome == 'Teste'
    assert usuario.email == 'teste@teste.com'
    assert usuario.tipo == 'gerente'
    assert usuario.verificar_senha('senha123')
    assert not usuario.verificar_senha('senha_errada')


def test_criar_plano(plano):
    """Testa a criação de um plano."""
    assert plano.nome == 'Plano Teste'
    assert plano.valor == 100.0
    assert plano.duracao_meses == 1
    assert plano.status == 'ativo'


def test_criar_aluno(aluno):
    """Testa a criação de um aluno."""
    assert aluno.nome == 'Aluno Teste'
    assert aluno.email == 'aluno@teste.com'
    assert aluno.cpf == '123.456.789-00'
    assert aluno.telefone == '(11) 98765-4321'
    assert aluno.data_nascimento == date(2000, 1, 1)
    assert aluno.status == 'ativo'


def test_criar_treino(aluno, usuario):
    """Testa a criação de um treino."""
    treino = Treino(
        aluno=aluno,
        professor=usuario,
        tipo='musculacao',
        status='ativo'
    )
    assert treino.aluno == aluno
    assert treino.professor == usuario
    assert treino.tipo == 'musculacao'
    assert treino.status == 'ativo'


def test_criar_exercicio(aluno, usuario):
    """Testa a criação de um exercício."""
    treino = Treino(
        aluno=aluno,
        professor=usuario,
        tipo='musculacao',
        status='ativo'
    )
    exercicio = Exercicio(
        treino=treino,
        nome='Supino',
        series=3,
        repeticoes=12,
        carga=20.0,
        ordem=1
    )
    assert exercicio.treino == treino
    assert exercicio.nome == 'Supino'
    assert exercicio.series == 3
    assert exercicio.repeticoes == 12
    assert exercicio.carga == 20.0
    assert exercicio.ordem == 1


def test_criar_turma(usuario):
    """Testa a criação de uma turma."""
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
    assert turma.professor == usuario
    assert turma.modalidade == 'musculacao'
    assert turma.nivel == 'iniciante'
    assert turma.dia_semana == 1
    assert turma.horario_inicio.strftime('%H:%M') == '08:00'
    assert turma.horario_fim.strftime('%H:%M') == '09:00'
    assert turma.capacidade_maxima == 20
    assert turma.status == 'ativa'


def test_criar_matricula_turma(aluno, usuario):
    """Testa a criação de uma matrícula em turma."""
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
    matricula = MatriculaTurma(
        aluno=aluno,
        turma=turma,
        status='ativa'
    )
    assert matricula.aluno == aluno
    assert matricula.turma == turma
    assert matricula.status == 'ativa'


def test_criar_pagamento(aluno):
    """Testa a criação de um pagamento."""
    pagamento = Pagamento(
        aluno=aluno,
        valor=100.0,
        data_pagamento=datetime.now(),
        forma_pagamento='dinheiro',
        status='pago'
    )
    assert pagamento.aluno == aluno
    assert pagamento.valor == 100.0
    assert pagamento.forma_pagamento == 'dinheiro'
    assert pagamento.status == 'pago'


def test_criar_presenca(aluno, usuario):
    """Testa a criação de uma presença."""
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
    presenca = Presenca(
        aluno=aluno,
        turma=turma,
        tipo='entrada'
    )
    assert presenca.aluno == aluno
    assert presenca.turma == turma
    assert presenca.tipo == 'entrada'


def test_relacionamentos():
    """Testa os relacionamentos entre os modelos."""
    # Cria usuário (professor)
    professor = Usuario(
        nome='Professor',
        email='professor@teste.com',
        tipo='professor'
    )
    professor.senha = 'senha123'
    
    # Cria plano
    plano = Plano(
        nome='Plano Teste',
        valor=100.0,
        duracao_meses=1,
        status='ativo'
    )
    
    # Cria aluno
    aluno = Aluno(
        nome='Aluno',
        email='aluno@teste.com',
        cpf='123.456.789-00',
        telefone='(11) 98765-4321',
        data_nascimento=date(2000, 1, 1),
        plano=plano,
        status='ativo'
    )
    
    # Cria turma
    turma = Turma(
        professor=professor,
        modalidade='musculacao',
        nivel='iniciante',
        dia_semana=1,
        horario_inicio=datetime.strptime('08:00', '%H:%M').time(),
        horario_fim=datetime.strptime('09:00', '%H:%M').time(),
        capacidade_maxima=20,
        status='ativa'
    )
    
    # Cria matrícula
    matricula = MatriculaTurma(
        aluno=aluno,
        turma=turma,
        status='ativa'
    )
    
    # Cria treino
    treino = Treino(
        aluno=aluno,
        professor=professor,
        tipo='musculacao',
        status='ativo'
    )
    
    # Cria exercício
    exercicio = Exercicio(
        treino=treino,
        nome='Supino',
        series=3,
        repeticoes=12,
        carga=20.0,
        ordem=1
    )
    
    # Cria pagamento
    pagamento = Pagamento(
        aluno=aluno,
        valor=100.0,
        data_pagamento=datetime.now(),
        forma_pagamento='dinheiro',
        status='pago'
    )
    
    # Cria presença
    presenca = Presenca(
        aluno=aluno,
        turma=turma,
        tipo='entrada'
    )
    
    # Testa relacionamentos
    assert aluno in plano.alunos
    assert treino in aluno.treinos
    assert pagamento in aluno.pagamentos
    assert matricula in aluno.matriculas_turmas
    assert exercicio in treino.exercicios
    assert matricula in turma.matriculas
    assert turma in professor.turmas
    assert treino in professor.treinos 