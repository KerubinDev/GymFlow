"""Script para inicializar o banco de dados com dados iniciais."""

from backend import create_app, db
from backend.models import Usuario, Professor, Plano, Exercicio

def init_db():
    """Inicializa o banco de dados com dados iniciais."""
    app = create_app()
    
    with app.app_context():
        # Recria todas as tabelas
        db.drop_all()
        db.create_all()
        
        # Cria usuário gerente padrão
        gerente = Usuario(
            nome='Administrador',
            email='admin@gymflow.com',
            tipo='gerente',
            status='ativo'
        )
        gerente.senha = 'admin123'
        db.session.add(gerente)
        
        # Cria alguns professores
        professores = [
            Professor(
                nome='João Silva',
                email='joao@gymflow.com',
                telefone='(11) 99999-1111',
                especialidades='Musculação, CrossFit',
                ativo=True
            ),
            Professor(
                nome='Maria Santos',
                email='maria@gymflow.com',
                telefone='(11) 99999-2222',
                especialidades='Pilates, Yoga',
                ativo=True
            ),
            Professor(
                nome='Pedro Oliveira',
                email='pedro@gymflow.com',
                telefone='(11) 99999-3333',
                especialidades='Funcional, Spinning',
                ativo=True
            )
        ]
        for professor in professores:
            db.session.add(professor)
        
        # Cria alguns planos
        planos = [
            Plano(
                nome='Básico',
                descricao='Acesso à academia em horário comercial',
                valor=89.90,
                duracao_meses=1,
                ativo=True
            ),
            Plano(
                nome='Premium',
                descricao='Acesso à academia em qualquer horário + 1 modalidade',
                valor=129.90,
                duracao_meses=1,
                ativo=True
            ),
            Plano(
                nome='VIP',
                descricao='Acesso total à academia e todas as modalidades',
                valor=199.90,
                duracao_meses=1,
                ativo=True
            )
        ]
        for plano in planos:
            db.session.add(plano)
        
        # Cria alguns exercícios
        exercicios = [
            Exercicio(
                nome='Supino Reto',
                descricao='Exercício para peitoral com barra',
                grupo_muscular='Peitoral',
                equipamento='Barra e banco reto',
                nivel='intermediario'
            ),
            Exercicio(
                nome='Agachamento',
                descricao='Exercício para pernas com barra',
                grupo_muscular='Pernas',
                equipamento='Barra e suporte',
                nivel='intermediario'
            ),
            Exercicio(
                nome='Puxada na Frente',
                descricao='Exercício para costas na polia alta',
                grupo_muscular='Costas',
                equipamento='Polia alta',
                nivel='iniciante'
            ),
            Exercicio(
                nome='Rosca Direta',
                descricao='Exercício para bíceps com barra',
                grupo_muscular='Bíceps',
                equipamento='Barra W',
                nivel='iniciante'
            ),
            Exercicio(
                nome='Extensão Triceps',
                descricao='Exercício para tríceps na polia alta',
                grupo_muscular='Tríceps',
                equipamento='Polia alta',
                nivel='iniciante'
            )
        ]
        for exercicio in exercicios:
            db.session.add(exercicio)
        
        # Commit das alterações
        db.session.commit()

if __name__ == '__main__':
    init_db() 