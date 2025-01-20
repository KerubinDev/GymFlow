"""Arquivo principal para executar a aplicação Flask."""

import os
from pathlib import Path
from dotenv import load_dotenv
from flask import Flask
from backend import create_app, db
from backend.models import Usuario, Aluno, Professor, Plano, Treino, Exercicio, Turma, MatriculaTurma, Pagamento, TreinoExercicio
from werkzeug.security import generate_password_hash
from datetime import datetime, timedelta

# Carregar variáveis de ambiente
load_dotenv()

# Criar a aplicação Flask
app = create_app()

def criar_usuarios_iniciais():
    """Cria usuários iniciais do sistema"""
    usuarios = [
        {
            'nome': 'Administrador',
            'email': 'admin@academia.com',
            'senha': 'admin123',
            'tipo': 'gerente'
        },
        {
            'nome': 'Professor',
            'email': 'professor@academia.com',
            'senha': 'prof123',
            'tipo': 'professor'
        },
        {
            'nome': 'Recepção',
            'email': 'recepcao@academia.com',
            'senha': 'rec123',
            'tipo': 'recepcionista'
        }
    ]
    
    for dados in usuarios:
        usuario = Usuario.query.filter_by(email=dados['email']).first()
        if not usuario:
            novo_usuario = Usuario(
                nome=dados['nome'],
                email=dados['email'],
                tipo=dados['tipo'],
                status='ativo'
            )
            novo_usuario.senha = dados['senha']
            db.session.add(novo_usuario)
            print(f"Usuário {dados['nome']} criado com sucesso!")
    
    db.session.commit()

def criar_planos_iniciais():
    """Cria planos básicos da academia"""
    planos = [
        {
            'nome': 'Mensal',
            'valor': 100.0,
            'duracao_meses': 1,
            'descricao': 'Plano mensal com acesso a todas as modalidades',
            'ativo': True
        },
        {
            'nome': 'Trimestral',
            'valor': 270.0,
            'duracao_meses': 3,
            'descricao': 'Plano trimestral com 10% de desconto',
            'ativo': True
        },
        {
            'nome': 'Semestral',
            'valor': 510.0,
            'duracao_meses': 6,
            'descricao': 'Plano semestral com 15% de desconto',
            'ativo': True
        },
        {
            'nome': 'Anual',
            'valor': 960.0,
            'duracao_meses': 12,
            'descricao': 'Plano anual com 20% de desconto',
            'ativo': True
        }
    ]
    
    for dados in planos:
        plano = Plano.query.filter_by(nome=dados['nome']).first()
        if not plano:
            novo_plano = Plano(**dados)
            db.session.add(novo_plano)
            print(f"Plano {dados['nome']} criado com sucesso!")
    
    db.session.commit()

def criar_dados_exemplo():
    """Cria dados de exemplo para o sistema."""
    print("Criando dados de exemplo...")
    
    try:
        # Verifica se já existem dados de exemplo (usando alunos como referência)
        if Aluno.query.count() > 0:
            print("Dados de exemplo já existem.")
            return
        
        # Criar professores
        usuario_prof1 = Usuario(
            nome='João Silva',
            email='joao@gymflow.com',
            tipo='professor',
            status='ativo'
        )
        usuario_prof1.senha = 'senha123'
        
        usuario_prof2 = Usuario(
            nome='Maria Santos',
            email='maria@gymflow.com',
            tipo='professor',
            status='ativo'
        )
        usuario_prof2.senha = 'senha123'
        
        db.session.add_all([usuario_prof1, usuario_prof2])
        db.session.commit()
        print("Professores criados com sucesso!")
        
        professor1 = Professor(
            usuario_id=usuario_prof1.id,
            especialidade='Musculação',
            horario_disponivel='Segunda a Sexta, 6h às 15h',
            status='ativo'
        )
        
        professor2 = Professor(
            usuario_id=usuario_prof2.id,
            especialidade='Pilates, Yoga',
            horario_disponivel='Segunda a Sexta, 14h às 22h',
            status='ativo'
        )
        
        db.session.add_all([professor1, professor2])
        db.session.commit()
        print("Dados dos professores adicionados com sucesso!")
        
        # Criar recepcionista
        usuario_recep = Usuario(
            nome='Ana Oliveira',
            email='ana@gymflow.com',
            tipo='recepcionista',
            status='ativo'
        )
        usuario_recep.senha = 'senha123'
        db.session.add(usuario_recep)
        db.session.commit()
        print("Recepcionista criada com sucesso!")
        
        # Criar alunos
        plano_mensal = Plano.query.filter_by(nome='Mensal').first()
        if not plano_mensal:
            raise Exception("Plano Mensal não encontrado. Execute criar_planos_iniciais() primeiro.")
            
        plano_trimestral = Plano.query.filter_by(nome='Trimestral').first()
        if not plano_trimestral:
            raise Exception("Plano Trimestral não encontrado. Execute criar_planos_iniciais() primeiro.")
        
        aluno1 = Aluno(
            nome='Pedro Souza',
            email='pedro@email.com',
            cpf='123.456.789-00',
            telefone='(11) 98765-4321',
            data_nascimento=datetime(1990, 5, 15).date(),
            endereco='Rua A, 123',
            altura=1.75,
            peso=75.0,
            objetivo='Hipertrofia',
            plano_id=plano_mensal.id,
            status='ativo'
        )
        
        aluno2 = Aluno(
            nome='Carla Lima',
            email='carla@email.com',
            cpf='987.654.321-00',
            telefone='(11) 91234-5678',
            data_nascimento=datetime(1995, 8, 20).date(),
            endereco='Rua B, 456',
            altura=1.65,
            peso=60.0,
            objetivo='Emagrecimento',
            plano_id=plano_trimestral.id,
            status='ativo'
        )
        
        db.session.add_all([aluno1, aluno2])
        db.session.commit()
        print("Alunos criados com sucesso!")
        
        # Criar exercícios
        exercicios = [
            Exercicio(
                nome='Supino Reto',
                detalhes='Exercício para peitoral com barra',
                grupo_muscular='Peitoral',
                equipamento='Barra e banco',
                nivel='intermediario'
            ),
            Exercicio(
                nome='Agachamento',
                detalhes='Exercício para pernas',
                grupo_muscular='Pernas',
                equipamento='Barra e suporte',
                nivel='intermediario'
            ),
            Exercicio(
                nome='Puxada Alta',
                detalhes='Exercício para costas',
                grupo_muscular='Costas',
                equipamento='Máquina',
                nivel='iniciante'
            )
        ]
        
        db.session.add_all(exercicios)
        db.session.commit()
        print("Exercícios criados com sucesso!")
        
        # Criar treinos
        treino1 = Treino(
            aluno_id=aluno1.id,
            professor_id=professor1.id,
            tipo='musculacao',
            status='ativo',
            observacoes='Treino focado em hipertrofia'
        )
        
        db.session.add(treino1)
        db.session.commit()
        
        # Adicionar exercícios ao treino
        treino_exercicio1 = TreinoExercicio(
            treino_id=treino1.id,
            exercicio_id=exercicios[0].id,  # Supino Reto
            series=4,
            repeticoes=12,
            carga=40,
            observacoes='Descanso de 1 minuto entre séries',
            ordem=1
        )
        
        treino_exercicio2 = TreinoExercicio(
            treino_id=treino1.id,
            exercicio_id=exercicios[1].id,  # Agachamento
            series=4,
            repeticoes=10,
            carga=60,
            observacoes='Fazer aquecimento',
            ordem=2
        )
        
        db.session.add_all([treino_exercicio1, treino_exercicio2])
        db.session.commit()
        print("Treinos e exercícios criados com sucesso!")
        
        # Criar turmas
        turma1 = Turma(
            modalidade='musculacao',
            professor_id=professor1.id,
            dia_semana=1,  # Segunda-feira
            horario_inicio='07:00',
            horario_fim='08:00',
            capacidade_maxima=15,
            nivel='intermediario',
            descricao='Turma de musculação matinal'
        )
        
        turma2 = Turma(
            modalidade='pilates',
            professor_id=professor2.id,
            dia_semana=2,  # Terça-feira
            horario_inicio='18:00',
            horario_fim='19:00',
            capacidade_maxima=10,
            nivel='iniciante',
            descricao='Turma de pilates noturna'
        )
        
        db.session.add_all([turma1, turma2])
        db.session.commit()
        print("Turmas criadas com sucesso!")
        
        # Matricular alunos nas turmas
        matricula1 = MatriculaTurma(
            aluno_id=aluno1.id,
            turma_id=turma1.id,
            data_inicio=datetime.now().date(),
            status='ativa'
        )
        
        matricula2 = MatriculaTurma(
            aluno_id=aluno2.id,
            turma_id=turma2.id,
            data_inicio=datetime.now().date(),
            status='ativa'
        )
        
        db.session.add_all([matricula1, matricula2])
        db.session.commit()
        print("Matrículas criadas com sucesso!")
        
        # Criar pagamentos
        mes_atual = datetime.now().strftime('%Y-%m')
        mes_anterior = (datetime.now() - timedelta(days=30)).strftime('%Y-%m')
        
        pagamento1 = Pagamento(
            aluno_id=aluno1.id,
            mes_referencia=mes_atual,
            status='pago',
            data_pagamento=datetime.now().date(),
            observacoes='Pagamento via PIX'
        )
        
        pagamento2 = Pagamento(
            aluno_id=aluno2.id,
            mes_referencia=mes_atual,
            status='pendente',
            observacoes='Aguardando pagamento'
        )
        
        pagamento3 = Pagamento(
            aluno_id=aluno1.id,
            mes_referencia=mes_anterior,
            status='pago',
            data_pagamento=(datetime.now() - timedelta(days=30)).date(),
            observacoes='Pagamento em cartão'
        )
        
        db.session.add_all([pagamento1, pagamento2, pagamento3])
        db.session.commit()
        print("Pagamentos criados com sucesso!")
        
        print("Todos os dados de exemplo foram criados com sucesso!")
        
    except Exception as e:
        db.session.rollback()
        print(f"Erro ao criar dados de exemplo: {str(e)}")
        raise

def inicializar_sistema():
    """Inicializa o sistema com as configurações necessárias"""
    print("Inicializando o sistema...")
    
    # Criar diretórios necessários
    diretorios = ['uploads', 'logs', 'static']
    for diretorio in diretorios:
        if not os.path.exists(diretorio):
            os.makedirs(diretorio)
            print(f"Diretório '{diretorio}' criado.")
    
    # Criar banco de dados e tabelas
    with app.app_context():
        # Apaga o banco de dados se existir
        if os.path.exists('instance/database.db'):
            os.remove('instance/database.db')
            print("Banco de dados antigo removido.")
        
        db.create_all()
        print("Banco de dados inicializado.")
        
        # Criar dados iniciais
        criar_usuarios_iniciais()
        print("Usuários iniciais criados.")
        
        criar_planos_iniciais()
        print("Planos iniciais criados.")
        
        criar_dados_exemplo()
        print("Dados de exemplo criados.")
    
    print("\nSistema inicializado com sucesso!")
    print("\nAcesse o sistema usando uma das seguintes contas:")
    print("Gerente: admin@academia.com / admin123")
    print("Professor: professor@academia.com / prof123")
    print("Recepção: recepcao@academia.com / rec123")

if __name__ == '__main__':
    inicializar_sistema()
    app.run(debug=True) 