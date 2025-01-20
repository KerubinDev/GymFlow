"""Rotas da aplicação."""

import os
from datetime import datetime, timedelta
from functools import wraps
from flask import (
    Blueprint, render_template, redirect, url_for,
    request, jsonify, current_app, send_from_directory
)
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.utils import secure_filename
from .models import db, Usuario, Aluno, Professor, Plano, Treino, Turma, Pagamento, Exercicio, MatriculaTurma

rotas = Blueprint('rotas', __name__)

def gerente_required(f):
    """Decorador para verificar se o usuário é gerente."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.tipo != 'gerente':
            return redirect(url_for('rotas.index'))
        return f(*args, **kwargs)
    return decorated_function


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
    Rota para o dashboard principal
    """
    if current_user.tipo not in ['gerente', 'recepcionista']:
        return redirect(url_for('rotas.index'))
    
    hoje = datetime.now().date()
    mes_atual = hoje.strftime('%Y-%m')
    
    # Métricas para o dashboard
    metricas = {
        # Total de alunos ativos
        'total_alunos': Aluno.query.filter_by(status='ativo').count(),
        
        # Total de alunos novos no mês
        'alunos_novos': Aluno.query.filter(
            Aluno.status == 'ativo',
            Aluno.data_matricula >= hoje.replace(day=1),
            Aluno.data_matricula <= hoje
        ).count(),
        
        # Total de pagamentos do mês
        'pagamentos_mes': Pagamento.query.filter(
            Pagamento.mes_referencia == mes_atual,
            Pagamento.status == 'pago'
        ).count(),
        
        # Total de pagamentos pendentes
        'pagamentos_pendentes': Pagamento.query.filter(
            Pagamento.mes_referencia == mes_atual,
            Pagamento.status == 'pendente'
        ).count(),
        
        # Dados para o gráfico de receita mensal (últimos 6 meses)
        'labels_meses': [],
        'dados_pagamentos': []
    }
    
    # Prepara dados para o gráfico de receita mensal
    for i in range(5, -1, -1):
        data = hoje - timedelta(days=hoje.day-1) - timedelta(days=30*i)
        mes = data.strftime('%Y-%m')
        metricas['labels_meses'].append(data.strftime('%b/%Y'))
        
        total_pagos = Pagamento.query.filter(
            Pagamento.mes_referencia == mes,
            Pagamento.status == 'pago'
        ).count()
        
        metricas['dados_pagamentos'].append(total_pagos)
    
    return render_template('dashboard.html', metricas=metricas)


@rotas.route('/alunos')
@login_required
def alunos():
    """
    Gerenciamento de alunos
    """
    if current_user.tipo not in ['gerente', 'recepcionista']:
        return redirect(url_for('rotas.index'))
    
    # Busca apenas planos ativos
    planos_disponiveis = Plano.query.filter_by(ativo=True).all()
    return render_template('cadastro_alunos.html', planos=planos_disponiveis)


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


@rotas.route('/api/usuarios', methods=['GET'])
@login_required
@gerente_required
def listar_usuarios():
    """Lista todos os usuários."""
    usuarios = Usuario.query.all()
    return jsonify([{
        'id': usuario.id,
        'nome': usuario.nome,
        'email': usuario.email,
        'tipo': usuario.tipo,
        'status': usuario.status
    } for usuario in usuarios])


@rotas.route('/api/usuarios', methods=['POST'])
@login_required
@gerente_required
def criar_usuario():
    """Cria um novo usuário."""
    dados = request.get_json()
    
    try:
        # Verifica se já existe usuário com este email
        if Usuario.query.filter_by(email=dados['email']).first():
            return jsonify({'erro': 'Email já cadastrado'}), 400
        
        # Cria o usuário
        usuario = Usuario(
            nome=dados['nome'],
            email=dados['email'],
            tipo=dados['tipo'],
            status='ativo'
        )
        usuario.senha = dados['senha']
        
        db.session.add(usuario)
        db.session.commit()
        
        return jsonify({
            'mensagem': 'Usuário cadastrado com sucesso',
            'id': usuario.id
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'erro': str(e)}), 400


@rotas.route('/api/usuarios/<int:usuario_id>', methods=['GET'])
@login_required
@gerente_required
def obter_usuario(usuario_id):
    """Obtém os detalhes de um usuário específico."""
    usuario = Usuario.query.get_or_404(usuario_id)
    return jsonify({
        'id': usuario.id,
        'nome': usuario.nome,
        'email': usuario.email,
        'tipo': usuario.tipo,
        'status': usuario.status
    })


@rotas.route('/api/usuarios/<int:usuario_id>', methods=['PUT'])
@login_required
@gerente_required
def atualizar_usuario(usuario_id):
    """Atualiza os dados de um usuário."""
    usuario = Usuario.query.get_or_404(usuario_id)
    dados = request.get_json()
    
    try:
        # Verifica se o email já está em uso por outro usuário
        if 'email' in dados and dados['email'] != usuario.email:
            if Usuario.query.filter_by(email=dados['email']).first():
                return jsonify({'erro': 'Email já cadastrado'}), 400
        
        # Atualiza os dados do usuário
        if 'nome' in dados:
            usuario.nome = dados['nome']
        if 'email' in dados:
            usuario.email = dados['email']
        if 'tipo' in dados:
            usuario.tipo = dados['tipo']
        if 'senha' in dados and dados['senha']:
            usuario.senha = dados['senha']
        if 'status' in dados:
            usuario.status = dados['status']
        
        db.session.commit()
        return jsonify({'mensagem': 'Usuário atualizado com sucesso'})
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'erro': str(e)}), 400


@rotas.route('/api/usuarios/<int:usuario_id>', methods=['DELETE'])
@login_required
@gerente_required
def deletar_usuario(usuario_id):
    """Inativa um usuário."""
    usuario = Usuario.query.get_or_404(usuario_id)
    
    try:
        # Não permite inativar o próprio usuário
        if usuario.id == current_user.id:
            return jsonify({'erro': 'Não é possível inativar seu próprio usuário'}), 400
        
        usuario.status = 'inativo'
        db.session.commit()
        return jsonify({'mensagem': 'Usuário inativado com sucesso'})
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'erro': str(e)}), 400


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


@rotas.route('/api/planos/disponiveis', methods=['GET'])
@login_required
def listar_planos_disponiveis():
    """API para listar planos disponíveis."""
    planos = Plano.query.filter_by(ativo=True).all()
    return jsonify([plano.to_dict() for plano in planos])


@rotas.route('/api/alunos', methods=['GET'])
@login_required
def listar_alunos():
    """API para listar alunos."""
    alunos = Aluno.query.all()
    return jsonify([aluno.to_dict() for aluno in alunos])


@rotas.route('/api/alunos', methods=['POST'])
@login_required
def criar_aluno():
    """API para criar um novo aluno."""
    dados = request.get_json()
    
    try:
        # Converte a data de string para objeto date
        data_nascimento = datetime.strptime(dados['data_nascimento'], '%Y-%m-%d').date()
        
        aluno = Aluno(
            nome=dados['nome'],
            email=dados['email'],
            cpf=dados['cpf'],
            telefone=dados['telefone'],
            data_nascimento=data_nascimento,
            endereco=dados.get('endereco'),
            altura=float(dados.get('altura', 0)) if dados.get('altura') else None,
            peso=float(dados.get('peso', 0)) if dados.get('peso') else None,
            objetivo=dados.get('objetivo'),
            observacoes=dados.get('observacoes'),
            plano_id=int(dados['plano_id']) if dados.get('plano_id') else None,
            status='ativo'
        )
        
        db.session.add(aluno)
        db.session.commit()
        
        return jsonify(aluno.to_dict()), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'erro': str(e)}), 400


@rotas.route('/api/alunos/<int:aluno_id>', methods=['PUT'])
@login_required
def atualizar_aluno(aluno_id):
    """API para atualizar um aluno existente."""
    aluno = Aluno.query.get_or_404(aluno_id)
    dados = request.get_json()
    
    try:
        if 'nome' in dados:
            aluno.nome = dados['nome']
        if 'email' in dados:
            aluno.email = dados['email']
        if 'cpf' in dados:
            aluno.cpf = dados['cpf']
        if 'telefone' in dados:
            aluno.telefone = dados['telefone']
        if 'data_nascimento' in dados:
            aluno.data_nascimento = datetime.strptime(dados['data_nascimento'], '%Y-%m-%d').date()
        if 'endereco' in dados:
            aluno.endereco = dados['endereco']
        if 'altura' in dados:
            aluno.altura = float(dados['altura']) if dados['altura'] else None
        if 'peso' in dados:
            aluno.peso = float(dados['peso']) if dados['peso'] else None
        if 'objetivo' in dados:
            aluno.objetivo = dados['objetivo']
        if 'observacoes' in dados:
            aluno.observacoes = dados['observacoes']
        if 'plano_id' in dados:
            aluno.plano_id = int(dados['plano_id']) if dados['plano_id'] else None
        if 'status' in dados:
            aluno.status = dados['status']
        
        db.session.commit()
        return jsonify(aluno.to_dict())
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'erro': str(e)}), 400


@rotas.route('/api/alunos/<int:aluno_id>', methods=['DELETE'])
@login_required
def deletar_aluno(aluno_id):
    """API para deletar um aluno."""
    aluno = Aluno.query.get_or_404(aluno_id)
    
    try:
        db.session.delete(aluno)
        db.session.commit()
        return '', 204
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'erro': str(e)}), 400


@rotas.route('/api/alunos/<int:aluno_id>', methods=['GET'])
@login_required
def obter_aluno(aluno_id):
    """API para obter detalhes de um aluno específico."""
    aluno = Aluno.query.get_or_404(aluno_id)
    return jsonify(aluno.to_dict())


@rotas.route('/api/pagamentos', methods=['GET'])
@login_required
def listar_pagamentos():
    """Lista pagamentos com filtros opcionais."""
    # Obtém parâmetros da query
    aluno_id = request.args.get('aluno_id', type=int)
    mes_referencia = request.args.get('mes_referencia')
    status = request.args.get('status')
    
    # Inicia a query base
    query = Pagamento.query
    
    # Aplica filtros se fornecidos
    if aluno_id:
        query = query.filter(Pagamento.aluno_id == aluno_id)
    if mes_referencia:
        query = query.filter(Pagamento.mes_referencia == mes_referencia)
    if status:
        query = query.filter(Pagamento.status == status)
        
    # Executa a query
    pagamentos = query.all()
    
    # Formata o resultado
    resultado = []
    for pagamento in pagamentos:
        aluno = pagamento.aluno
        resultado.append({
            'id': pagamento.id,
            'aluno': {
                'id': aluno.id,
                'nome': aluno.nome,
                'plano': aluno.plano.nome if aluno.plano else None
            },
            'mes_referencia': pagamento.mes_referencia,
            'status': pagamento.status,
            'data_pagamento': pagamento.data_pagamento.strftime('%Y-%m-%d') if pagamento.data_pagamento else None,
            'observacoes': pagamento.observacoes
        })
    
    return jsonify(resultado)


@rotas.route('/api/pagamentos', methods=['POST'])
@login_required
def criar_pagamento():
    """Cria um novo registro de pagamento."""
    dados = request.get_json()
    
    # Verifica se já existe pagamento para este aluno/mês
    pagamento_existente = Pagamento.query.filter_by(
        aluno_id=dados['aluno_id'],
        mes_referencia=dados['mes_referencia']
    ).first()
    
    if pagamento_existente:
        return jsonify({
            'erro': 'Já existe um pagamento registrado para este aluno neste mês'
        }), 400
    
    # Cria o novo pagamento
    pagamento = Pagamento(
        aluno_id=dados['aluno_id'],
        mes_referencia=dados['mes_referencia'],
        status=dados['status'],
        data_pagamento=datetime.strptime(dados['data_pagamento'], '%Y-%m-%d') if dados.get('data_pagamento') else None,
        observacoes=dados.get('observacoes')
    )
    
    try:
        db.session.add(pagamento)
        db.session.commit()
        return jsonify({'mensagem': 'Pagamento registrado com sucesso'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'erro': str(e)}), 500


@rotas.route('/api/pagamentos/<int:pagamento_id>', methods=['PUT'])
@login_required
def atualizar_pagamento(pagamento_id):
    """Atualiza um registro de pagamento existente."""
    pagamento = Pagamento.query.get_or_404(pagamento_id)
    dados = request.get_json()
    
    try:
        # Atualiza os campos
        if 'status' in dados:
            pagamento.status = dados['status']
        if 'data_pagamento' in dados:
            pagamento.data_pagamento = datetime.strptime(dados['data_pagamento'], '%Y-%m-%d') if dados['data_pagamento'] else None
        if 'observacoes' in dados:
            pagamento.observacoes = dados['observacoes']
        
        db.session.commit()
        return jsonify({'mensagem': 'Pagamento atualizado com sucesso'})
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'erro': str(e)}), 500


@rotas.route('/api/pagamentos/<int:pagamento_id>', methods=['DELETE'])
@login_required
def deletar_pagamento(pagamento_id):
    """Deleta um registro de pagamento."""
    pagamento = Pagamento.query.get_or_404(pagamento_id)
    
    try:
        db.session.delete(pagamento)
        db.session.commit()
        return jsonify({'mensagem': 'Pagamento deletado com sucesso'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'erro': str(e)}), 500


@rotas.route('/api/pagamentos/<int:pagamento_id>', methods=['GET'])
@login_required
def obter_pagamento(pagamento_id):
    """Obtém os detalhes de um pagamento específico."""
    pagamento = Pagamento.query.get_or_404(pagamento_id)
    return jsonify({
        'id': pagamento.id,
        'aluno_id': pagamento.aluno_id,
        'mes_referencia': pagamento.mes_referencia,
        'data_pagamento': pagamento.data_pagamento.strftime('%Y-%m-%d') if pagamento.data_pagamento else None,
        'status': pagamento.status,
        'observacoes': pagamento.observacoes
    })


@rotas.route('/api/pagamentos/resumo', methods=['GET'])
@login_required
def obter_resumo_pagamentos():
    """API para obter resumo dos pagamentos."""
    hoje = datetime.now().date()
    mes_atual = hoje.strftime('%Y-%m')
    
    # Total de pagamentos do mês
    total_pagos = Pagamento.query.filter(
        Pagamento.mes_referencia == mes_atual,
        Pagamento.status == 'pago'
    ).count()
    
    # Total de pagamentos pendentes
    total_pendentes = Pagamento.query.filter(
        Pagamento.mes_referencia == mes_atual,
        Pagamento.status == 'pendente'
    ).count()
    
    # Total de pagamentos atrasados (meses anteriores)
    total_atrasados = Pagamento.query.filter(
        Pagamento.mes_referencia < mes_atual,
        Pagamento.status == 'pendente'
    ).count()
    
    # Taxa de inadimplência
    total_pagamentos = total_pagos + total_pendentes
    taxa_inadimplencia = (total_pendentes / total_pagamentos * 100) if total_pagamentos > 0 else 0
    
    return jsonify({
        'total_pagos': total_pagos,
        'total_pendentes': total_pendentes,
        'total_atrasados': total_atrasados,
        'taxa_inadimplencia': float(taxa_inadimplencia)
    })


@rotas.route('/api/treinos', methods=['GET'])
@login_required
def listar_treinos():
    """API para listar treinos."""
    treinos = Treino.query.all()
    return jsonify([treino.to_dict() for treino in treinos])


@rotas.route('/api/treinos', methods=['POST'])
@login_required
def criar_treino():
    """API para criar um novo treino."""
    dados = request.get_json()
    
    try:
        treino = Treino(
            aluno_id=dados['aluno_id'],
            professor_id=dados['professor_id'],
            tipo=dados['tipo'],
            data_inicio=datetime.strptime(dados['data_inicio'], '%Y-%m-%d').date(),
            status=dados['status'],
            observacoes=dados.get('observacoes'),
            exercicios=dados.get('exercicios', [])
        )
        
        db.session.add(treino)
        db.session.commit()
        
        return jsonify(treino.to_dict()), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'erro': str(e)}), 400


@rotas.route('/api/treinos/<int:treino_id>', methods=['PUT'])
@login_required
def atualizar_treino(treino_id):
    """API para atualizar um treino existente."""
    treino = Treino.query.get_or_404(treino_id)
    dados = request.get_json()
    
    try:
        if 'aluno_id' in dados:
            treino.aluno_id = dados['aluno_id']
        if 'professor_id' in dados:
            treino.professor_id = dados['professor_id']
        if 'tipo' in dados:
            treino.tipo = dados['tipo']
        if 'data_inicio' in dados:
            treino.data_inicio = datetime.strptime(dados['data_inicio'], '%Y-%m-%d').date()
        if 'status' in dados:
            treino.status = dados['status']
        if 'observacoes' in dados:
            treino.observacoes = dados['observacoes']
        if 'exercicios' in dados:
            treino.exercicios = dados['exercicios']
        
        db.session.commit()
        return jsonify(treino.to_dict())
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'erro': str(e)}), 400


@rotas.route('/api/treinos/<int:treino_id>', methods=['DELETE'])
@login_required
def deletar_treino(treino_id):
    """API para deletar um treino."""
    treino = Treino.query.get_or_404(treino_id)
    
    try:
        db.session.delete(treino)
        db.session.commit()
        return '', 204
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'erro': str(e)}), 400


@rotas.route('/api/treinos/<int:treino_id>', methods=['GET'])
@login_required
def obter_treino(treino_id):
    """API para obter detalhes de um treino específico."""
    treino = Treino.query.get_or_404(treino_id)
    return jsonify(treino.to_dict())


@rotas.route('/api/exercicios', methods=['GET'])
@login_required
def listar_exercicios():
    """API para listar exercícios."""
    exercicios = Exercicio.query.all()
    return jsonify([exercicio.to_dict() for exercicio in exercicios])


@rotas.route('/api/exercicios', methods=['POST'])
@login_required
def criar_exercicio():
    """API para criar um novo exercício."""
    dados = request.get_json()
    
    try:
        exercicio = Exercicio(
            nome=dados['nome'],
            detalhes=dados.get('detalhes'),
            grupo_muscular=dados['grupo_muscular'],
            equipamento=dados.get('equipamento'),
            nivel=dados.get('nivel', 'iniciante')
        )
        
        db.session.add(exercicio)
        db.session.commit()
        
        return jsonify(exercicio.to_dict()), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'erro': str(e)}), 400


@rotas.route('/professores')
@login_required
@gerente_required
def professores():
    """Rota para a página de cadastro de professores."""
    return render_template('cadastro_professores.html')


@rotas.route('/api/professores', methods=['GET'])
@login_required
def listar_professores():
    """Lista todos os professores ativos."""
    try:
        professores = Professor.query.join(Professor.usuario).filter(
            Professor.status == 'ativo',
            Usuario.status == 'ativo'
        ).all()
        
        return jsonify([{
            'id': professor.id,
            'nome': professor.usuario.nome,
            'email': professor.usuario.email,
            'telefone': professor.horario_disponivel,
            'especialidades': professor.especialidade,
            'ativo': True
        } for professor in professores if professor.usuario])
    except Exception as e:
        print(f"Erro ao listar professores: {str(e)}")  # Log do erro
        return jsonify({'erro': str(e)}), 500


@rotas.route('/api/professores', methods=['POST'])
@login_required
@gerente_required
def criar_professor():
    """Cria um novo professor."""
    dados = request.get_json()
    
    try:
        # Cria o usuário primeiro
        usuario = Usuario(
            nome=dados['nome'],
            email=dados['email'],
            tipo='professor',
            status='ativo'
        )
        usuario.senha = dados['senha']
        db.session.add(usuario)
        db.session.flush()  # Gera o ID do usuário
        
        # Cria o professor associado ao usuário
        professor = Professor(
            usuario_id=usuario.id,
            telefone=dados['telefone'],
            especialidades=dados['especialidades'],
            status='ativo'
        )
        db.session.add(professor)
        db.session.commit()
        
        return jsonify({
            'mensagem': 'Professor cadastrado com sucesso',
            'id': professor.id
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'erro': str(e)}), 400


@rotas.route('/api/professores/<int:professor_id>', methods=['GET'])
@login_required
def obter_professor(professor_id):
    """Obtém os detalhes de um professor específico."""
    professor = Professor.query.get_or_404(professor_id)
    return jsonify({
        'id': professor.id,
        'nome': professor.usuario.nome,
        'email': professor.usuario.email,
        'telefone': professor.telefone,
        'especialidades': professor.especialidades,
        'ativo': professor.status == 'ativo'
    })


@rotas.route('/api/professores/<int:professor_id>', methods=['PUT'])
@login_required
@gerente_required
def atualizar_professor(professor_id):
    """Atualiza os dados de um professor."""
    professor = Professor.query.get_or_404(professor_id)
    dados = request.get_json()
    
    try:
        # Atualiza os dados do usuário
        professor.usuario.nome = dados['nome']
        professor.usuario.email = dados['email']
        if dados.get('senha'):
            professor.usuario.senha = dados['senha']
        
        # Atualiza os dados do professor
        professor.telefone = dados['telefone']
        professor.especialidades = dados['especialidades']
        
        db.session.commit()
        return jsonify({'mensagem': 'Professor atualizado com sucesso'})
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'erro': str(e)}), 400


@rotas.route('/api/professores/<int:professor_id>', methods=['DELETE'])
@login_required
@gerente_required
def deletar_professor(professor_id):
    """Inativa um professor."""
    professor = Professor.query.get_or_404(professor_id)
    
    try:
        # Verifica se o professor tem turmas ativas
        if any(turma.status == 'ativa' for turma in professor.turmas):
            return jsonify({
                'erro': 'Não é possível excluir um professor com turmas ativas'
            }), 400
        
        # Inativa o professor e seu usuário
        professor.status = 'inativo'
        professor.usuario.status = 'inativo'
        
        db.session.commit()
        return jsonify({'mensagem': 'Professor inativado com sucesso'})
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'erro': str(e)}), 400


@rotas.route('/api/turmas', methods=['GET'])
@login_required
def listar_turmas():
    """Lista todas as turmas cadastradas."""
    turmas = Turma.query.all()
    return jsonify([{
        'id': turma.id,
        'modalidade': turma.modalidade,
        'professor_id': turma.professor_id,
        'professor': {
            'id': turma.professor.id,
            'nome': turma.professor.nome
        },
        'dia_semana': turma.dia_semana,
        'horario_inicio': turma.horario_inicio,
        'horario_fim': turma.horario_fim,
        'capacidade_maxima': turma.capacidade_maxima,
        'nivel': turma.nivel,
        'descricao': turma.descricao,
        'matriculas': [{
            'id': matricula.id,
            'aluno': {
                'id': matricula.aluno.id,
                'nome': matricula.aluno.nome
            }
        } for matricula in turma.matriculas]
    } for turma in turmas])


@rotas.route('/api/turmas/<int:turma_id>', methods=['GET'])
@login_required
def obter_turma(turma_id):
    """Obtém os detalhes de uma turma específica."""
    turma = Turma.query.get_or_404(turma_id)
    return jsonify({
        'id': turma.id,
        'modalidade': turma.modalidade,
        'professor_id': turma.professor_id,
        'professor': {
            'id': turma.professor.id,
            'nome': turma.professor.nome
        },
        'dia_semana': turma.dia_semana,
        'horario_inicio': turma.horario_inicio,
        'horario_fim': turma.horario_fim,
        'capacidade_maxima': turma.capacidade_maxima,
        'nivel': turma.nivel,
        'descricao': turma.descricao,
        'matriculas': [{
            'id': matricula.id,
            'aluno': {
                'id': matricula.aluno.id,
                'nome': matricula.aluno.nome
            }
        } for matricula in turma.matriculas]
    })


@rotas.route('/api/turmas', methods=['POST'])
@login_required
@gerente_required
def criar_turma():
    """Cria uma nova turma."""
    dados = request.get_json()
    
    # Validação dos dados
    campos_obrigatorios = [
        'modalidade', 'professor_id', 'dia_semana', 
        'horario_inicio', 'horario_fim', 'capacidade_maxima', 'nivel'
    ]
    for campo in campos_obrigatorios:
        if campo not in dados:
            return jsonify({'erro': f'Campo {campo} é obrigatório'}), 400
    
    # Verifica se o professor existe
    professor = Professor.query.get(dados['professor_id'])
    if not professor:
        return jsonify({'erro': 'Professor não encontrado'}), 404
