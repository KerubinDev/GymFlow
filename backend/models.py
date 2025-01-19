"""Modelos do sistema GymFlow."""

from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import jwt
from .config import Config
from typing import Dict, Any
from flask_login import UserMixin

db = SQLAlchemy()

class Usuario(db.Model, UserMixin):
    """Modelo para usuários do sistema."""
    __tablename__ = 'usuarios'
    
    id: int = db.Column(db.Integer, primary_key=True)
    nome: str = db.Column(db.String(100), nullable=False)
    email: str = db.Column(db.String(120), unique=True, nullable=False)
    _senha_hash: str = db.Column(db.String(128), nullable=False)
    tipo: str = db.Column(
        db.Enum('gerente', 'professor', 'recepcionista', name='tipo_usuario'),
        nullable=False
    )
    status: str = db.Column(
        db.Enum('ativo', 'inativo', name='status_usuario'),
        default='ativo',
        nullable=False
    )
    foto_url: str = db.Column(db.String(200))
    data_criacao: datetime = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        nullable=False
    )
    ultima_atualizacao: datetime = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False
    )
    
    # Relacionamentos
    turmas = db.relationship('Turma', backref='professor', lazy=True)
    treinos = db.relationship('Treino', backref='professor', lazy=True)
    
    @property
    def senha(self) -> str:
        """Impede acesso direto à senha."""
        raise AttributeError('senha não é um atributo legível')
    
    @senha.setter
    def senha(self, senha: str) -> None:
        """Define a senha do usuário."""
        self._senha_hash = generate_password_hash(senha)
    
    def verificar_senha(self, senha: str) -> bool:
        """Verifica se a senha está correta."""
        return check_password_hash(self._senha_hash, senha)
    
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
            'tipo': self.tipo,
            'status': self.status,
            'foto_url': self.foto_url,
            'data_criacao': self.data_criacao.isoformat(),
            'ultima_atualizacao': self.ultima_atualizacao.isoformat()
        }
    
    def get_id(self):
        """Método necessário para Flask-Login"""
        return str(self.id)
    
    @property
    def is_active(self):
        """Método necessário para Flask-Login"""
        return True
    
    @property
    def is_authenticated(self):
        """Método necessário para Flask-Login"""
        return True
    
    @property
    def is_anonymous(self):
        """Método necessário para Flask-Login"""
        return False


class Aluno(db.Model):
    """Modelo para alunos da academia."""
    __tablename__ = 'alunos'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    cpf = db.Column(db.String(14), unique=True, nullable=False)
    telefone = db.Column(db.String(20))
    data_nascimento = db.Column(db.Date, nullable=False)
    endereco = db.Column(db.String(200))
    foto_url = db.Column(db.String(200))
    altura = db.Column(db.Float)  # em metros
    peso = db.Column(db.Float)    # em kg
    objetivo = db.Column(
        db.Enum(
            'hipertrofia',
            'emagrecimento',
            'condicionamento',
            'reabilitacao',
            name='objetivo_aluno'
        )
    )
    observacoes = db.Column(db.Text)
    status = db.Column(
        db.Enum('ativo', 'inativo', 'pendente', name='status_aluno'),
        default='ativo',
        nullable=False
    )
    data_matricula = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        nullable=False
    )
    ultima_atualizacao = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False
    )
    
    # Relacionamentos
    plano_id = db.Column(
        db.Integer,
        db.ForeignKey('planos.id'),
        nullable=False
    )
    treinos = db.relationship('Treino', backref='aluno', lazy=True)
    pagamentos = db.relationship('Pagamento', backref='aluno', lazy=True)
    matriculas_turmas = db.relationship(
        'MatriculaTurma',
        backref='aluno',
        lazy=True
    )


class Plano(db.Model):
    """Modelo para planos da academia."""
    __tablename__ = 'planos'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.Text)
    valor = db.Column(db.Float, nullable=False)
    duracao_meses = db.Column(db.Integer, nullable=False)
    modalidades = db.Column(db.String(200))  # Lista de modalidades separadas por vírgula
    status = db.Column(
        db.Enum('ativo', 'inativo', name='status_plano'),
        default='ativo',
        nullable=False
    )
    data_criacao = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        nullable=False
    )
    ultima_atualizacao = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False
    )
    
    # Relacionamentos
    alunos = db.relationship('Aluno', backref='plano', lazy=True)


class Treino(db.Model):
    """Modelo para treinos dos alunos."""
    __tablename__ = 'treinos'
    
    id = db.Column(db.Integer, primary_key=True)
    aluno_id = db.Column(
        db.Integer,
        db.ForeignKey('alunos.id'),
        nullable=False
    )
    professor_id = db.Column(
        db.Integer,
        db.ForeignKey('usuarios.id'),
        nullable=False
    )
    tipo = db.Column(
        db.Enum(
            'musculacao',
            'cardio',
            'funcional',
            name='tipo_treino'
        ),
        nullable=False
    )
    observacoes = db.Column(db.Text)
    status = db.Column(
        db.Enum('ativo', 'inativo', name='status_treino'),
        default='ativo',
        nullable=False
    )
    data_criacao = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        nullable=False
    )
    ultima_atualizacao = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False
    )
    
    # Relacionamentos
    exercicios = db.relationship('Exercicio', backref='treino', lazy=True)


class Exercicio(db.Model):
    """Modelo para exercícios dos treinos."""
    __tablename__ = 'exercicios'
    
    id = db.Column(db.Integer, primary_key=True)
    treino_id = db.Column(
        db.Integer,
        db.ForeignKey('treinos.id'),
        nullable=False
    )
    nome = db.Column(db.String(100), nullable=False)
    series = db.Column(db.Integer, nullable=False)
    repeticoes = db.Column(db.Integer, nullable=False)
    carga = db.Column(db.Float)  # em kg
    observacoes = db.Column(db.Text)
    ordem = db.Column(db.Integer, nullable=False)


class Turma(db.Model):
    """Modelo para turmas da academia."""
    __tablename__ = 'turmas'
    
    id = db.Column(db.Integer, primary_key=True)
    professor_id = db.Column(
        db.Integer,
        db.ForeignKey('usuarios.id'),
        nullable=False
    )
    modalidade = db.Column(
        db.Enum(
            'musculacao',
            'crossfit',
            'pilates',
            'yoga',
            'funcional',
            name='modalidade_turma'
        ),
        nullable=False
    )
    nivel = db.Column(
        db.Enum(
            'iniciante',
            'intermediario',
            'avancado',
            name='nivel_turma'
        ),
        nullable=False
    )
    dia_semana = db.Column(db.Integer, nullable=False)  # 0-6 (domingo-sábado)
    horario_inicio = db.Column(db.Time, nullable=False)
    horario_fim = db.Column(db.Time, nullable=False)
    capacidade_maxima = db.Column(db.Integer, nullable=False)
    descricao = db.Column(db.Text)
    status = db.Column(
        db.Enum('ativa', 'inativa', name='status_turma'),
        default='ativa',
        nullable=False
    )
    data_criacao = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        nullable=False
    )
    ultima_atualizacao = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False
    )
    
    # Relacionamentos
    matriculas = db.relationship(
        'MatriculaTurma',
        backref='turma',
        lazy=True
    )


class MatriculaTurma(db.Model):
    """Modelo para matrículas de alunos em turmas."""
    __tablename__ = 'matriculas_turmas'
    
    id = db.Column(db.Integer, primary_key=True)
    aluno_id = db.Column(
        db.Integer,
        db.ForeignKey('alunos.id'),
        nullable=False
    )
    turma_id = db.Column(
        db.Integer,
        db.ForeignKey('turmas.id'),
        nullable=False
    )
    data_matricula = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        nullable=False
    )
    status = db.Column(
        db.Enum('ativa', 'inativa', name='status_matricula'),
        default='ativa',
        nullable=False
    )


class Pagamento(db.Model):
    """Modelo para pagamentos dos alunos."""
    __tablename__ = 'pagamentos'
    
    id = db.Column(db.Integer, primary_key=True)
    aluno_id = db.Column(
        db.Integer,
        db.ForeignKey('alunos.id'),
        nullable=False
    )
    valor = db.Column(db.Float, nullable=False)
    data_pagamento = db.Column(db.DateTime, nullable=False)
    forma_pagamento = db.Column(
        db.Enum(
            'dinheiro',
            'cartao_credito',
            'cartao_debito',
            'pix',
            'transferencia',
            name='forma_pagamento'
        ),
        nullable=False
    )
    status = db.Column(
        db.Enum(
            'pago',
            'pendente',
            'vencido',
            'cancelado',
            name='status_pagamento'
        ),
        default='pendente',
        nullable=False
    )
    observacoes = db.Column(db.Text)
    data_criacao = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        nullable=False
    )
    ultima_atualizacao = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False
    )


class Presenca(db.Model):
    """Modelo para controle de presença dos alunos."""
    __tablename__ = 'presencas'
    
    id = db.Column(db.Integer, primary_key=True)
    aluno_id = db.Column(
        db.Integer,
        db.ForeignKey('alunos.id'),
        nullable=False
    )
    turma_id = db.Column(
        db.Integer,
        db.ForeignKey('turmas.id')
    )
    data_hora = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        nullable=False
    )
    tipo = db.Column(
        db.Enum('entrada', 'saida', name='tipo_presenca'),
        nullable=False
    )


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
            Plano(nome='Mensal', valor=100.0, duracao_meses=1),
            Plano(nome='Trimestral', valor=270.0, duracao_meses=3),
            Plano(nome='Semestral', valor=510.0, duracao_meses=6),
            Plano(nome='Anual', valor=960.0, duracao_meses=12)
        ]
        for plano in planos:
            db.session.add(plano)
        
        db.session.commit() 