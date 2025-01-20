"""Arquivo principal para executar a aplicação Flask."""

import os
from pathlib import Path
from dotenv import load_dotenv
from flask import Flask
from backend import create_app, db
from backend.models import Usuario, Aluno, Professor, Plano, Treino, Exercicio, Turma, MatriculaTurma, Pagamento
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
            'email': 'admin@academia.com',
            'senha': 'admin123',
            'nome': 'Administrador',
            'tipo': 'gerente'
        },
        {
            'email': 'professor@academia.com',
            'senha': 'prof123',
            'nome': 'Professor Principal',
            'tipo': 'professor'
        },
        {
            'email': 'recepcao@academia.com',
            'senha': 'rec123',
            'nome': 'Recepcionista',
            'tipo': 'recepcionista'
        }
    ]
    
    for dados in usuarios:
        usuario = Usuario.query.filter_by(email=dados['email']).first()
        if not usuario:
            novo_usuario = Usuario(
                email=dados['email'],
                nome=dados['nome'],
                tipo=dados['tipo']
            )
            novo_usuario.senha = dados['senha']  # Usando o property setter
            db.session.add(novo_usuario)
            
            # Se for professor, cria o registro de professor
            if dados['tipo'] == 'professor':
                professor = Professor(
                    usuario=novo_usuario,
                    especialidade='Musculação',
                    horario_disponivel='08:00-18:00'
                )
                db.session.add(professor)
            
            print(f"Usuário {dados['nome']} criado com sucesso!")
            print(f"Email: {dados['email']}")
            print(f"Senha: {dados['senha']}")
            print("---")
    
    db.session.commit()

def criar_planos_iniciais():
    """Cria planos básicos da academia"""
    planos = [
        {
            'nome': 'Mensal',
            'valor': 100.0,
            'duracao_meses': 1,
            'descricao': 'Plano mensal com acesso a todas as modalidades'
        },
        {
            'nome': 'Trimestral',
            'valor': 270.0,
            'duracao_meses': 3,
            'descricao': 'Plano trimestral com 10% de desconto'
        },
        {
            'nome': 'Semestral',
            'valor': 510.0,
            'duracao_meses': 6,
            'descricao': 'Plano semestral com 15% de desconto'
        },
        {
            'nome': 'Anual',
            'valor': 960.0,
            'duracao_meses': 12,
            'descricao': 'Plano anual com 20% de desconto'
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
    with app.app_context():
        # Verifica se já existem dados
        if Usuario.query.count() > 1:  # Ignora o admin padrão
            return
        
        # Criar planos
        plano_basic = Plano(
            nome='Plano Basic',
            descricao='Acesso à academia em horário comercial',
            valor=89.90,
            duracao_meses=1,
            ativo=True
        )
        
        plano_premium = Plano(
            nome='Plano Premium',
            descricao='Acesso total à academia + aulas',
            valor=129.90,
            duracao_meses=1,
            ativo=True
        )
        
        db.session.add_all([plano_basic, plano_premium])
        db.session.commit()
        
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
        
        # Criar alunos
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
            plano_id=plano_premium.id,
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
            plano_id=plano_basic.id,
            status='ativo'
        )
        
        db.session.add_all([aluno1, aluno2])
        db.session.commit()
        
        # Criar exercícios
        exercicios = [
            Exercicio(
                nome='Supino Reto',
                descricao='Exercício para peitoral com barra',
                grupo_muscular='Peitoral',
                equipamento='Barra e banco',
                nivel='intermediario'
            ),
            Exercicio(
                nome='Agachamento',
                descricao='Exercício para pernas',
                grupo_muscular='Pernas',
                equipamento='Barra e suporte',
                nivel='intermediario'
            ),
            Exercicio(
                nome='Puxada Alta',
                descricao='Exercício para costas',
                grupo_muscular='Costas',
                equipamento='Máquina',
                nivel='iniciante'
            )
        ]
        
        db.session.add_all(exercicios)
        db.session.commit()
        
        # Criar treinos
        treino1 = Treino(
            aluno_id=aluno1.id,
            professor_id=professor1.id,
            tipo='musculacao',
            data_inicio=datetime.now().date(),
            status='ativo',
            observacoes='Treino focado em hipertrofia',
            exercicios=[{
                'exercicio_id': exercicios[0].id,
                'series': 4,
                'repeticoes': 12,
                'carga': 40,
                'observacoes': 'Descanso de 1 minuto entre séries'
            }, {
                'exercicio_id': exercicios[1].id,
                'series': 4,
                'repeticoes': 10,
                'carga': 60,
                'observacoes': 'Fazer aquecimento'
            }]
        )
        
        db.session.add(treino1)
        db.session.commit()
        
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
        db.create_all()
        print("Banco de dados inicializado.")
        
        # Criar dados iniciais
        criar_usuarios_iniciais()
        criar_planos_iniciais()
        criar_dados_exemplo()
    
    print("\nSistema inicializado com sucesso!")
    print("\nAcesse o sistema usando uma das seguintes contas:")
    print("Gerente: admin@academia.com / admin123")
    print("Professor: professor@academia.com / prof123")
    print("Recepção: recepcao@academia.com / rec123")

if __name__ == '__main__':
    inicializar_sistema()
    app.run(debug=True) 