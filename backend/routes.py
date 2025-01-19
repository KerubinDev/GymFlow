from flask import Blueprint, jsonify, request
from models import (Usuario, Aluno, Plano, Pagamento, Professor, 
                   Turma, Treino, db)
from flask_login import login_required, current_user
from datetime import datetime

# Criação do Blueprint para organizar as rotas
rotas = Blueprint('rotas', __name__)


@rotas.route('/usuarios', methods=['GET', 'POST'])
@login_required
def gerenciar_usuarios():
    """
    Gerencia operações relacionadas aos usuários do sistema.
    GET: Lista todos os usuários
    POST: Cria novo usuário
    """
    if request.method == 'GET':
        usuarios = Usuario.query.all()
        return jsonify([u.to_dict() for u in usuarios])
    
    dados = request.get_json()
    novo_usuario = Usuario(
        nome=dados['nome'],
        email=dados['email'],
        tipo=dados['tipo']
    )
    novo_usuario.set_senha(dados['senha'])
    db.session.add(novo_usuario)
    db.session.commit()
    return jsonify(novo_usuario.to_dict()), 201


@rotas.route('/alunos', methods=['GET', 'POST'])
@login_required
def gerenciar_alunos():
    """
    Gerencia operações relacionadas aos alunos.
    GET: Lista todos os alunos
    POST: Cadastra novo aluno
    """
    if request.method == 'GET':
        alunos = Aluno.query.all()
        return jsonify([a.to_dict() for a in alunos])
    
    dados = request.get_json()
    novo_aluno = Aluno(
        nome=dados['nome'],
        telefone=dados['telefone'],
        data_nascimento=datetime.strptime(dados['data_nascimento'], 
                                        '%Y-%m-%d'),
        plano_id=dados['plano_id'],
        status='ativo'
    )
    db.session.add(novo_aluno)
    db.session.commit()
    return jsonify(novo_aluno.to_dict()), 201


@rotas.route('/planos', methods=['GET', 'POST'])
@login_required
def gerenciar_planos():
    """
    Gerencia operações relacionadas aos planos.
    GET: Lista todos os planos
    POST: Cria novo plano
    """
    if request.method == 'GET':
        planos = Plano.query.all()
        return jsonify([p.to_dict() for p in planos])
    
    dados = request.get_json()
    novo_plano = Plano(
        nome=dados['nome'],
        valor=dados['valor'],
        duracao=dados['duracao']
    )
    db.session.add(novo_plano)
    db.session.commit()
    return jsonify(novo_plano.to_dict()), 201


@rotas.route('/pagamentos', methods=['GET', 'POST'])
@login_required
def gerenciar_pagamentos():
    """
    Gerencia operações relacionadas aos pagamentos.
    GET: Lista todos os pagamentos
    POST: Registra novo pagamento
    """
    if request.method == 'GET':
        pagamentos = Pagamento.query.all()
        return jsonify([p.to_dict() for p in pagamentos])
    
    dados = request.get_json()
    novo_pagamento = Pagamento(
        aluno_id=dados['aluno_id'],
        data_pagamento=datetime.now(),
        valor=dados['valor'],
        status='pago'
    )
    db.session.add(novo_pagamento)
    db.session.commit()
    return jsonify(novo_pagamento.to_dict()), 201


@rotas.route('/professores', methods=['GET', 'POST'])
@login_required
def gerenciar_professores():
    """
    Gerencia operações relacionadas aos professores.
    GET: Lista todos os professores
    POST: Cadastra novo professor
    """
    if request.method == 'GET':
        professores = Professor.query.all()
        return jsonify([p.to_dict() for p in professores])
    
    dados = request.get_json()
    novo_professor = Professor(
        nome=dados['nome'],
        especialidade=dados['especialidade'],
        horario_disponivel=dados['horario_disponivel']
    )
    db.session.add(novo_professor)
    db.session.commit()
    return jsonify(novo_professor.to_dict()), 201


@rotas.route('/turmas', methods=['GET', 'POST'])
@login_required
def gerenciar_turmas():
    """
    Gerencia operações relacionadas às turmas.
    GET: Lista todas as turmas
    POST: Cria nova turma
    """
    if request.method == 'GET':
        turmas = Turma.query.all()
        return jsonify([t.to_dict() for t in turmas])
    
    dados = request.get_json()
    nova_turma = Turma(
        professor_id=dados['professor_id'],
        nome=dados['nome'],
        horario=dados['horario'],
        capacidade=dados['capacidade']
    )
    db.session.add(nova_turma)
    db.session.commit()
    return jsonify(nova_turma.to_dict()), 201


@rotas.route('/treinos', methods=['GET', 'POST'])
@login_required
def gerenciar_treinos():
    """
    Gerencia operações relacionadas aos treinos.
    GET: Lista todos os treinos
    POST: Cria novo treino
    """
    if request.method == 'GET':
        treinos = Treino.query.all()
        return jsonify([t.to_dict() for t in treinos])
    
    dados = request.get_json()
    novo_treino = Treino(
        aluno_id=dados['aluno_id'],
        exercicio=dados['exercicio'],
        series=dados['series'],
        repeticoes=dados['repeticoes'],
        carga=dados['carga']
    )
    db.session.add(novo_treino)
    db.session.commit()
    return jsonify(novo_treino.to_dict()), 201


# Rotas para operações específicas de cada entidade
@rotas.route('/alunos/<int:id>', methods=['GET', 'PUT', 'DELETE'])
@login_required
def gerenciar_aluno(id):
    """
    Gerencia operações em um aluno específico.
    GET: Obtém detalhes do aluno
    PUT: Atualiza dados do aluno
    DELETE: Remove aluno
    """
    aluno = Aluno.query.get_or_404(id)
    
    if request.method == 'GET':
        return jsonify(aluno.to_dict())
    
    elif request.method == 'PUT':
        dados = request.get_json()
        aluno.nome = dados.get('nome', aluno.nome)
        aluno.telefone = dados.get('telefone', aluno.telefone)
        aluno.status = dados.get('status', aluno.status)
        db.session.commit()
        return jsonify(aluno.to_dict())
    
    db.session.delete(aluno)
    db.session.commit()
    return '', 204


@rotas.route('/login', methods=['POST'])
def login():
    """
    Realiza o login do usuário no sistema.
    POST: Autentica usuário e retorna token de acesso
    """
    dados = request.get_json()
    usuario = Usuario.query.filter_by(email=dados['email']).first()
    
    if usuario and usuario.verificar_senha(dados['senha']):
        return jsonify({
            'token': usuario.gerar_token(),
            'usuario': usuario.to_dict()
        })
    
    return jsonify({'erro': 'Credenciais inválidas'}), 401


@rotas.route('/recuperar-senha', methods=['POST'])
def recuperar_senha():
    """
    Inicia o processo de recuperação de senha.
    POST: Envia email com link de recuperação
    """
    dados = request.get_json()
    usuario = Usuario.query.filter_by(email=dados['email']).first()
    
    if usuario:
        token = usuario.gerar_token_recuperacao()
        # Implementar envio de email aqui
        return jsonify({'mensagem': 'Email de recuperação enviado'})
    
    return jsonify({'erro': 'Email não encontrado'}), 404


@rotas.route('/pagamentos/filtrar', methods=['GET'])
@login_required
def filtrar_pagamentos():
    """
    Filtra pagamentos por aluno e período.
    """
    aluno_id = request.args.get('aluno_id')
    data_inicio = request.args.get('data_inicio')
    data_fim = request.args.get('data_fim')
    
    query = Pagamento.query
    
    if aluno_id:
        query = query.filter_by(aluno_id=aluno_id)
    if data_inicio and data_fim:
        query = query.filter(
            Pagamento.data_pagamento.between(
                datetime.strptime(data_inicio, '%Y-%m-%d'),
                datetime.strptime(data_fim, '%Y-%m-%d')
            )
        )
    
    return jsonify([p.to_dict() for p in query.all()])


@rotas.route('/turmas/<int:id>/reservar', methods=['POST'])
@login_required
def reservar_vaga(id):
    """
    Reserva vaga em uma turma para um aluno.
    """
    turma = Turma.query.get_or_404(id)
    dados = request.get_json()
    
    if turma.alunos.count() >= turma.capacidade:
        return jsonify({'erro': 'Turma lotada'}), 400
    
    aluno = Aluno.query.get_or_404(dados['aluno_id'])
    turma.alunos.append(aluno)
    db.session.commit()
    
    return jsonify(turma.to_dict())


@rotas.route('/dashboard', methods=['GET'])
@login_required
def obter_dashboard():
    """
    Retorna dados para o painel de gerenciamento.
    """
    total_alunos = Aluno.query.count()
    total_receitas = db.session.query(
        db.func.sum(Pagamento.valor)
    ).filter_by(status='pago').scalar() or 0
    
    ocupacao_turmas = []
    for turma in Turma.query.all():
        ocupacao = {
            'turma': turma.nome,
            'ocupacao': (turma.alunos.count() / turma.capacidade) * 100
        }
        ocupacao_turmas.append(ocupacao)
    
    # Calcula inadimplência
    alunos_inadimplentes = Aluno.query.filter_by(status='inadimplente').count()
    taxa_inadimplencia = (alunos_inadimplentes / total_alunos * 100) if total_alunos > 0 else 0
    
    return jsonify({
        'total_alunos': total_alunos,
        'total_receitas': float(total_receitas),
        'ocupacao_turmas': ocupacao_turmas,
        'taxa_inadimplencia': taxa_inadimplencia
    })


@rotas.route('/treinos/<int:aluno_id>/personalizar', methods=['PUT'])
@login_required
def personalizar_treino(aluno_id):
    """
    Personaliza treino de um aluno específico.
    """
    dados = request.get_json()
    treinos = dados.get('treinos', [])
    
    # Remove treinos antigos
    Treino.query.filter_by(aluno_id=aluno_id).delete()
    
    # Adiciona novos treinos
    for treino in treinos:
        novo_treino = Treino(
            aluno_id=aluno_id,
            exercicio=treino['exercicio'],
            series=treino['series'],
            repeticoes=treino['repeticoes'],
            carga=treino['carga']
        )
        db.session.add(novo_treino)
    
    db.session.commit()
    return jsonify({'mensagem': 'Treino atualizado com sucesso'})
