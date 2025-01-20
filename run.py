"""Arquivo principal para executar a aplicação Flask."""

import os
from pathlib import Path
from dotenv import load_dotenv
from flask import Flask
from backend import create_app, db
from backend.models import Usuario, Aluno, Professor, Plano, Treino, Exercicio, Turma, MatriculaTurma, Pagamento
from werkzeug.security import generate_password_hash

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
    
    print("\nSistema inicializado com sucesso!")
    print("\nAcesse o sistema usando uma das seguintes contas:")
    print("Gerente: admin@academia.com / admin123")
    print("Professor: professor@academia.com / prof123")
    print("Recepção: recepcao@academia.com / rec123")

if __name__ == '__main__':
    inicializar_sistema()
    app.run(debug=True) 