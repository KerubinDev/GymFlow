from flask import Blueprint, jsonify, request, render_template, redirect, url_for
from .models import (Usuario, Aluno, Plano, Pagamento, Professor, 
                   Turma, Treino, db)
from flask_login import login_required, current_user, login_user, logout_user
from datetime import datetime, timedelta

# Criação do Blueprint para organizar as rotas
rotas = Blueprint('rotas', __name__)


@rotas.route('/')
def index():
    """
    Rota principal que redireciona baseado no status de login
    """
    if current_user.is_authenticated:
        # Redireciona baseado no tipo de usuário
        if current_user.tipo == 'gerente':
            return redirect(url_for('rotas.dashboard'))
        elif current_user.tipo == 'professor':
            return redirect(url_for('rotas.treinos'))
        elif current_user.tipo == 'recepcionista':
            return redirect(url_for('rotas.alunos'))
    return redirect(url_for('rotas.login'))


@rotas.route('/login', methods=['GET', 'POST'])
def login():
    """
    Gerencia o login de usuários.
    GET: Exibe página de login
    POST: Processa o login
    """
    if current_user.is_authenticated:
        return redirect(url_for('rotas.index'))
    
    if request.method == 'GET':
        return render_template('login.html')
    
    dados = request.get_json()
    usuario = Usuario.query.filter_by(email=dados['email']).first()
    
    if usuario and usuario.verificar_senha(dados['senha']):
        login_user(usuario)
        return jsonify({
            'token': usuario.gerar_token(),
            'usuario': usuario.to_dict(),
            'redirect': url_for('rotas.index')
        })
    
    return jsonify({'erro': 'Credenciais inválidas'}), 401


@rotas.route('/logout')
@login_required
def logout():
    """
    Realiza o logout do usuário
    """
    logout_user()
    return redirect(url_for('rotas.login'))


@rotas.route('/dashboard')
@login_required
def dashboard():
    """
    Exibe o dashboard administrativo
    """
    if current_user.tipo != 'gerente':
        return redirect(url_for('rotas.index'))
    
    # Calcula o primeiro dia do mês atual
    hoje = datetime.now()
    primeiro_dia_mes = datetime(hoje.year, hoje.month, 1)
    
    # Calcula métricas
    metricas = {
        'total_alunos': Aluno.query.filter_by(status='ativo').count(),
        'receita_mensal': db.session.query(db.func.sum(Pagamento.valor)).\
            filter(Pagamento.data_pagamento >= primeiro_dia_mes).\
            scalar() or 0,
        'novas_matriculas': Aluno.query.filter(
            Aluno.data_matricula >= (hoje - timedelta(days=30))
        ).count(),
        'presenca_diaria': 0,  # Implementar contagem de presenças
        
        # Dados para os gráficos
        'labels_meses': [
            'Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun',
            'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez'
        ],
        'valores_mensais': [0] * 12  # Inicializa com zeros
    }
    
    # Calcula valores mensais
    ano_atual = hoje.year
    for mes in range(12):
        inicio_mes = datetime(ano_atual, mes + 1, 1)
        if mes < 11:
            fim_mes = datetime(ano_atual, mes + 2, 1)
        else:
            fim_mes = datetime(ano_atual + 1, 1, 1)
            
        valor = db.session.query(db.func.sum(Pagamento.valor)).\
            filter(
                Pagamento.data_pagamento >= inicio_mes,
                Pagamento.data_pagamento < fim_mes
            ).scalar()
        metricas['valores_mensais'][mes] = float(valor or 0)
    
    return render_template('dashboard.html', metricas=metricas, datetime=datetime)


@rotas.route('/alunos')
@login_required
def alunos():
    """
    Gerenciamento de alunos
    """
    if current_user.tipo not in ['gerente', 'recepcionista']:
        return redirect(url_for('rotas.index'))
    return render_template('cadastro_alunos.html')


@rotas.route('/treinos')
@login_required
def treinos():
    """
    Gerenciamento de treinos
    """
    if current_user.tipo not in ['gerente', 'professor']:
        return redirect(url_for('rotas.index'))
    return render_template('treinos.html')


@rotas.route('/turmas')
@login_required
def turmas():
    """
    Gerenciamento de turmas
    """
    if current_user.tipo not in ['gerente', 'professor']:
        return redirect(url_for('rotas.index'))
    return render_template('horarios_turmas.html')


@rotas.route('/pagamentos')
@login_required
def pagamentos():
    """
    Gerenciamento de pagamentos
    """
    if current_user.tipo not in ['gerente', 'recepcionista']:
        return redirect(url_for('rotas.index'))
    return render_template('gestao_pagamentos.html')


@rotas.route('/usuarios')
@login_required
def usuarios():
    """
    Gerenciamento de usuários
    """
    if current_user.tipo != 'gerente':
        return redirect(url_for('rotas.index'))
    return render_template('cadastro_usuarios.html')


@rotas.route('/planos')
@login_required
@gerente_required
def planos():
    """Rota para listar e gerenciar planos."""
    planos = Plano.query.all()
    return render_template('planos.html', planos=planos)


@rotas.route('/api/login', methods=['POST'])
def api_login():
    """
    API para login
    """
    dados = request.get_json()
    usuario = Usuario.query.filter_by(email=dados['email']).first()
    
    if usuario and usuario.verificar_senha(dados['senha']):
        login_user(usuario, remember=dados.get('lembrar', False))
        return jsonify({
            'token': usuario.gerar_token(),
            'redirect': url_for('rotas.index')
        })
    
    return jsonify({'mensagem': 'Email ou senha inválidos'}), 401


@rotas.route('/api/usuarios', methods=['GET', 'POST'])
@login_required
def api_usuarios():
    """
    API para gerenciamento de usuários
    """
    if current_user.tipo != 'gerente':
        return jsonify({'mensagem': 'Acesso negado'}), 403
    
    if request.method == 'GET':
        usuarios = Usuario.query.all()
        return jsonify([usuario.to_dict() for usuario in usuarios])
    
    dados = request.form.to_dict()
    
    try:
        novo_usuario = Usuario(
            nome=dados['nome'],
            email=dados['email'],
            tipo=dados['tipo'],
            status=dados['status']
        )
        novo_usuario.senha = dados['senha']
        
        if 'foto' in request.files:
            foto = request.files['foto']
            if foto.filename:
                # Implementar upload de foto
                pass
        
        db.session.add(novo_usuario)
        
        # Se for professor, cria registro na tabela de professores
        if dados['tipo'] == 'professor':
            professor = Professor(
                usuario=novo_usuario,
                especialidade=dados['especialidade'],
                horario_disponivel=dados['horarioDisponivel']
            )
            db.session.add(professor)
        
        db.session.commit()
        return jsonify({'mensagem': 'Usuário criado com sucesso'})
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'mensagem': str(e)}), 400


@rotas.route('/api/usuarios/<int:id>', methods=['GET', 'PUT', 'DELETE'])
@login_required
def api_usuario(id):
    """
    API para gerenciar um usuário específico
    """
    if current_user.tipo != 'gerente':
        return jsonify({'mensagem': 'Acesso negado'}), 403
    
    usuario = Usuario.query.get_or_404(id)
    
    if request.method == 'GET':
        return jsonify(usuario.to_dict())
    
    elif request.method == 'PUT':
        dados = request.form.to_dict()
        
        try:
            usuario.nome = dados.get('nome', usuario.nome)
            usuario.email = dados.get('email', usuario.email)
            usuario.tipo = dados.get('tipo', usuario.tipo)
            usuario.status = dados.get('status', usuario.status)
            
            if 'senha' in dados:
                usuario.senha = dados['senha']
            
            if 'foto' in request.files:
                foto = request.files['foto']
                if foto.filename:
                    # Implementar upload de foto
                    pass
            
            # Atualiza dados do professor se aplicável
            if usuario.tipo == 'professor':
                professor = usuario.professor or Professor(usuario=usuario)
                professor.especialidade = dados.get('especialidade', professor.especialidade)
                professor.horario_disponivel = dados.get('horarioDisponivel', professor.horario_disponivel)
                if not usuario.professor:
                    db.session.add(professor)
            
            db.session.commit()
            return jsonify({'mensagem': 'Usuário atualizado com sucesso'})
        
        except Exception as e:
            db.session.rollback()
            return jsonify({'mensagem': str(e)}), 400
    
    elif request.method == 'DELETE':
        try:
            db.session.delete(usuario)
            db.session.commit()
            return jsonify({'mensagem': 'Usuário excluído com sucesso'})
        except Exception as e:
            db.session.rollback()
            return jsonify({'mensagem': str(e)}), 400


@rotas.route('/api/usuarios/<int:id>/resetar-senha', methods=['PUT'])
@login_required
def api_resetar_senha(id):
    """
    API para resetar a senha de um usuário
    """
    if current_user.tipo != 'gerente':
        return jsonify({'mensagem': 'Acesso negado'}), 403
    
    usuario = Usuario.query.get_or_404(id)
    nova_senha = usuario.gerar_senha_aleatoria()
    usuario.senha = nova_senha
    
    try:
        db.session.commit()
        return jsonify({'senha': nova_senha})
    except Exception as e:
        db.session.rollback()
        return jsonify({'mensagem': str(e)}), 400


@rotas.route('/api/usuarios/<int:id>/inativar', methods=['PUT'])
@login_required
def api_inativar_usuario(id):
    """
    API para inativar um usuário
    """
    if current_user.tipo != 'gerente':
        return jsonify({'mensagem': 'Acesso negado'}), 403
    
    usuario = Usuario.query.get_or_404(id)
    usuario.status = 'inativo'
    
    try:
        db.session.commit()
        return jsonify({'mensagem': 'Usuário inativado com sucesso'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'mensagem': str(e)}), 400


@rotas.route('/api/planos', methods=['POST'])
@login_required
@gerente_required
def criar_plano():
    """API para criar um novo plano."""
    dados = request.get_json()
    
    try:
        plano = Plano(
            nome=dados['nome'],
            descricao=dados.get('descricao'),
            valor=float(dados['valor']),
            duracao_meses=int(dados['duracao_meses']),
            ativo=True
        )
        
        db.session.add(plano)
        db.session.commit()
        
        return jsonify(plano.to_dict()), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'erro': str(e)}), 400


@rotas.route('/api/planos/<int:plano_id>', methods=['PUT'])
@login_required
@gerente_required
def atualizar_plano(plano_id):
    """API para atualizar um plano existente."""
    plano = Plano.query.get_or_404(plano_id)
    dados = request.get_json()
    
    try:
        plano.nome = dados.get('nome', plano.nome)
        plano.descricao = dados.get('descricao', plano.descricao)
        plano.valor = float(dados.get('valor', plano.valor))
        plano.duracao_meses = int(dados.get('duracao_meses', plano.duracao_meses))
        plano.ativo = dados.get('ativo', plano.ativo)
        
        db.session.commit()
        return jsonify(plano.to_dict())
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'erro': str(e)}), 400


@rotas.route('/api/planos/<int:plano_id>', methods=['DELETE'])
@login_required
@gerente_required
def deletar_plano(plano_id):
    """API para deletar um plano."""
    plano = Plano.query.get_or_404(plano_id)
    
    try:
        db.session.delete(plano)
        db.session.commit()
        return '', 204
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'erro': str(e)}), 400


@rotas.route('/api/planos/<int:plano_id>', methods=['GET'])
@login_required
@gerente_required
def obter_plano(plano_id):
    """API para obter detalhes de um plano específico."""
    plano = Plano.query.get_or_404(plano_id)
    return jsonify(plano.to_dict())
