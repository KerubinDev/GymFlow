from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import jwt
from .config import Config
from typing import Dict, Any

db = SQLAlchemy()

class Usuario(db.Model):
    """Modelo para usuários do sistema."""
    __tablename__ = 'usuarios'
    
    id: int = db.Column(db.Integer, primary_key=True)
    nome: str = db.Column(db.String(100), nullable=False)
    email: str = db.Column(db.String(120), unique=True, nullable=False)
    _senha: str = db.Column('senha', db.String(255), nullable=False)
    tipo: str = db.Column(db.String(20), nullable=False)
    
    def set_senha(self, senha: str) -> None:
        """Define a senha criptografada do usuário."""
        self._senha = generate_password_hash(senha)
    
    def verificar_senha(self, senha: str) -> bool:
        """Verifica se a senha está correta."""
        return check_password_hash(self._senha, senha)
    
    def gerar_token(self) -> str:
        """Gera um token JWT para o usuário."""
        return jwt.encode(
            {'user_id': self.id, 'email': self.email},
            Config.SECRET_KEY,
            algorithm='HS256'
        )
    
    def to_dict(self) -> Dict[str, Any]:
        """Converte o objeto para dicionário."""
        return {
            'id': self.id,
            'nome': self.nome,
            'email': self.email,
            'tipo': self.tipo
        }


class Aluno(db.Model):
    """Modelo para alunos da academia."""
    __tablename__ = 'alunos'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    telefone = db.Column(db.String(20), nullable=False)
    data_nascimento = db.Column(db.Date, nullable=False)
    plano_id = db.Column(db.Integer, db.ForeignKey('planos.id'), nullable=False)
    status = db.Column(db.String(20), default='ativo')
    
    # Relacionamentos
    plano = db.relationship('Plano', backref='alunos')
    pagamentos = db.relationship('Pagamento', backref='aluno', lazy=True)
    treinos = db.relationship('Treino', backref='aluno', lazy=True)
    turmas = db.relationship('Turma', secondary='alunos_turmas', backref='alunos')
    
    def to_dict(self):
        """Converte o objeto para dicionário."""
        return {
            'id': self.id,
            'nome': self.nome,
            'telefone': self.telefone,
            'data_nascimento': self.data_nascimento.isoformat(),
            'plano_id': self.plano_id,
            'plano_nome': self.plano.nome,
            'status': self.status
        }


class Plano(db.Model):
    """Modelo para planos disponíveis."""
    __tablename__ = 'planos'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), nullable=False)
    valor = db.Column(db.Float, nullable=False)
    duracao = db.Column(db.Integer, nullable=False)  # em meses
    
    def to_dict(self):
        """Converte o objeto para dicionário."""
        return {
            'id': self.id,
            'nome': self.nome,
            'valor': self.valor,
            'duracao': self.duracao
        }


class Pagamento(db.Model):
    """Modelo para pagamentos dos alunos."""
    __tablename__ = 'pagamentos'
    
    id = db.Column(db.Integer, primary_key=True)
    aluno_id = db.Column(db.Integer, db.ForeignKey('alunos.id'), nullable=False)
    data_pagamento = db.Column(db.DateTime, default=datetime.utcnow)
    valor = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), default='pendente')
    
    def to_dict(self):
        """Converte o objeto para dicionário."""
        return {
            'id': self.id,
            'aluno_id': self.aluno_id,
            'aluno_nome': self.aluno.nome,
            'data_pagamento': self.data_pagamento.isoformat(),
            'valor': self.valor,
            'status': self.status
        }


class Professor(db.Model):
    """Modelo para professores da academia."""
    __tablename__ = 'professores'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    especialidade = db.Column(db.String(50), nullable=False)
    horario_disponivel = db.Column(db.String(200), nullable=False)
    
    # Relacionamentos
    turmas = db.relationship('Turma', backref='professor', lazy=True)
    
    def to_dict(self):
        """Converte o objeto para dicionário."""
        return {
            'id': self.id,
            'nome': self.nome,
            'especialidade': self.especialidade,
            'horario_disponivel': self.horario_disponivel
        }


class Turma(db.Model):
    """Modelo para turmas da academia."""
    __tablename__ = 'turmas'
    
    id = db.Column(db.Integer, primary_key=True)
    professor_id = db.Column(db.Integer, db.ForeignKey('professores.id'), 
                           nullable=False)
    nome = db.Column(db.String(50), nullable=False)
    horario = db.Column(db.String(50), nullable=False)
    capacidade = db.Column(db.Integer, nullable=False)
    
    def to_dict(self):
        """Converte o objeto para dicionário."""
        return {
            'id': self.id,
            'professor_id': self.professor_id,
            'professor_nome': self.professor.nome,
            'nome': self.nome,
            'horario': self.horario,
            'capacidade': self.capacidade,
            'alunos_count': len(self.alunos)
        }


# Tabela de associação entre alunos e turmas
alunos_turmas = db.Table('alunos_turmas',
    db.Column('aluno_id', db.Integer, db.ForeignKey('alunos.id'), primary_key=True),
    db.Column('turma_id', db.Integer, db.ForeignKey('turmas.id'), primary_key=True)
)


class Treino(db.Model):
    """Modelo para treinos dos alunos."""
    __tablename__ = 'treinos'
    
    id = db.Column(db.Integer, primary_key=True)
    aluno_id = db.Column(db.Integer, db.ForeignKey('alunos.id'), nullable=False)
    exercicio = db.Column(db.String(100), nullable=False)
    series = db.Column(db.Integer, nullable=False)
    repeticoes = db.Column(db.Integer, nullable=False)
    carga = db.Column(db.Float, nullable=False)
    
    def to_dict(self):
        """Converte o objeto para dicionário."""
        return {
            'id': self.id,
            'aluno_id': self.aluno_id,
            'exercicio': self.exercicio,
            'series': self.series,
            'repeticoes': self.repeticoes,
            'carga': self.carga
        }


def init_db():
    """Inicializa o banco de dados."""
    db.create_all()
    
    # Cria usuário admin se não existir
    if not Usuario.query.filter_by(email='admin@academia.com').first():
        admin = Usuario(
            nome='Administrador',
            email='admin@academia.com',
            tipo='gerente'
        )
        admin.set_senha('admin123')
        db.session.add(admin)
        
        # Cria planos básicos
        planos = [
            Plano(nome='Mensal', valor=100.0, duracao=1),
            Plano(nome='Trimestral', valor=270.0, duracao=3),
            Plano(nome='Semestral', valor=510.0, duracao=6),
            Plano(nome='Anual', valor=960.0, duracao=12)
        ]
        for plano in planos:
            db.session.add(plano)
        
        db.session.commit() 