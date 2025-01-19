"""Funções utilitárias para o sistema GymFlow."""

import os
import re
from datetime import datetime, date
from typing import Optional, List, Dict, Any, Union
from werkzeug.utils import secure_filename
from PIL import Image
from flask import current_app
import jwt
from functools import wraps
from flask import jsonify, request
from flask_login import current_user


def validar_cpf(cpf: str) -> bool:
    """
    Valida um CPF.
    
    Args:
        cpf: String contendo o CPF a ser validado
        
    Returns:
        bool: True se o CPF é válido, False caso contrário
    """
    # Remove caracteres não numéricos
    cpf = re.sub(r'[^0-9]', '', cpf)
    
    if len(cpf) != 11:
        return False
    
    # Verifica se todos os dígitos são iguais
    if len(set(cpf)) == 1:
        return False
    
    # Calcula primeiro dígito verificador
    soma = sum(int(cpf[i]) * (10 - i) for i in range(9))
    resto = (soma * 10) % 11
    if resto == 10:
        resto = 0
    if resto != int(cpf[9]):
        return False
    
    # Calcula segundo dígito verificador
    soma = sum(int(cpf[i]) * (11 - i) for i in range(10))
    resto = (soma * 10) % 11
    if resto == 10:
        resto = 0
    if resto != int(cpf[10]):
        return False
    
    return True


def validar_email(email: str) -> bool:
    """
    Valida um endereço de email.
    
    Args:
        email: String contendo o email a ser validado
        
    Returns:
        bool: True se o email é válido, False caso contrário
    """
    padrao = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(padrao, email))


def calcular_idade(data_nascimento: date) -> int:
    """
    Calcula a idade a partir da data de nascimento.
    
    Args:
        data_nascimento: Data de nascimento
        
    Returns:
        int: Idade em anos
    """
    hoje = date.today()
    idade = hoje.year - data_nascimento.year
    if hoje.month < data_nascimento.month or (
        hoje.month == data_nascimento.month and 
        hoje.day < data_nascimento.day
    ):
        idade -= 1
    return idade


def formatar_cpf(cpf: str) -> str:
    """
    Formata um CPF para exibição (XXX.XXX.XXX-XX).
    
    Args:
        cpf: String contendo o CPF a ser formatado
        
    Returns:
        str: CPF formatado
    """
    cpf = re.sub(r'[^0-9]', '', cpf)
    return f'{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}'


def formatar_telefone(telefone: str) -> str:
    """
    Formata um telefone para exibição ((XX) XXXXX-XXXX).
    
    Args:
        telefone: String contendo o telefone a ser formatado
        
    Returns:
        str: Telefone formatado
    """
    telefone = re.sub(r'[^0-9]', '', telefone)
    if len(telefone) == 11:
        return f'({telefone[:2]}) {telefone[2:7]}-{telefone[7:]}'
    return telefone


def formatar_moeda(valor: float) -> str:
    """
    Formata um valor monetário para exibição (R$ X.XXX,XX).
    
    Args:
        valor: Valor a ser formatado
        
    Returns:
        str: Valor formatado
    """
    return f'R$ {valor:,.2f}'.replace(',', '_').replace('.', ',').replace('_', '.')


def salvar_foto(arquivo, pasta: str) -> Optional[str]:
    """
    Salva uma foto no sistema de arquivos.
    
    Args:
        arquivo: Arquivo de imagem enviado
        pasta: Nome da pasta onde salvar o arquivo
        
    Returns:
        Optional[str]: Caminho do arquivo salvo ou None se houver erro
    """
    if not arquivo:
        return None
    
    # Verifica extensão
    extensoes_permitidas = {'png', 'jpg', 'jpeg', 'gif'}
    if not arquivo.filename.lower().endswith(tuple(extensoes_permitidas)):
        return None
    
    try:
        # Gera nome seguro
        nome_arquivo = secure_filename(arquivo.filename)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        nome_final = f'{timestamp}_{nome_arquivo}'
        
        # Cria pasta se não existir
        caminho_pasta = os.path.join(current_app.config['UPLOAD_FOLDER'], pasta)
        os.makedirs(caminho_pasta, exist_ok=True)
        
        # Salva arquivo
        caminho_arquivo = os.path.join(caminho_pasta, nome_final)
        arquivo.save(caminho_arquivo)
        
        # Redimensiona imagem
        with Image.open(caminho_arquivo) as img:
            # Mantém proporção e redimensiona para no máximo 800x800
            img.thumbnail((800, 800))
            img.save(caminho_arquivo, optimize=True, quality=85)
        
        return os.path.join(pasta, nome_final)
    
    except Exception as e:
        print(f'Erro ao salvar foto: {e}')
        return None


def excluir_foto(caminho: str) -> bool:
    """
    Exclui uma foto do sistema de arquivos.
    
    Args:
        caminho: Caminho do arquivo a ser excluído
        
    Returns:
        bool: True se excluiu com sucesso, False caso contrário
    """
    if not caminho:
        return False
    
    try:
        caminho_completo = os.path.join(current_app.config['UPLOAD_FOLDER'], caminho)
        if os.path.exists(caminho_completo):
            os.remove(caminho_completo)
            return True
        return False
    except Exception as e:
        print(f'Erro ao excluir foto: {e}')
        return False


def requer_permissao(*tipos: str):
    """
    Decorador para verificar permissões de acesso.
    
    Args:
        *tipos: Tipos de usuário permitidos
        
    Returns:
        function: Decorador que verifica permissões
    """
    def decorador(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            if not current_user.is_authenticated:
                return jsonify({'erro': 'Não autorizado'}), 401
            if current_user.tipo not in tipos:
                return jsonify({'erro': 'Acesso negado'}), 403
            return f(*args, **kwargs)
        return wrapper
    return decorador


def verificar_token(token: str) -> Optional[Dict[str, Any]]:
    """
    Verifica e decodifica um token JWT.
    
    Args:
        token: Token JWT a ser verificado
        
    Returns:
        Optional[Dict[str, Any]]: Dados do token ou None se inválido
    """
    try:
        return jwt.decode(
            token,
            current_app.config['SECRET_KEY'],
            algorithms=['HS256']
        )
    except jwt.InvalidTokenError:
        return None


def paginar_resultados(
    query,
    pagina: int = 1,
    por_pagina: int = 10
) -> Dict[str, Any]:
    """
    Pagina resultados de uma query.
    
    Args:
        query: Query do SQLAlchemy
        pagina: Número da página
        por_pagina: Itens por página
        
    Returns:
        Dict[str, Any]: Dicionário com resultados paginados
    """
    paginacao = query.paginate(
        page=pagina,
        per_page=por_pagina,
        error_out=False
    )
    
    return {
        'items': [item.to_dict() for item in paginacao.items],
        'total': paginacao.total,
        'paginas': paginacao.pages,
        'pagina_atual': paginacao.page
    }


def filtrar_query(
    query,
    filtros: Dict[str, Any],
    mapeamento_campos: Dict[str, str]
) -> Any:
    """
    Aplica filtros em uma query do SQLAlchemy.
    
    Args:
        query: Query base
        filtros: Dicionário com filtros a serem aplicados
        mapeamento_campos: Mapeamento entre nomes dos filtros e campos do modelo
        
    Returns:
        Any: Query com filtros aplicados
    """
    for campo, valor in filtros.items():
        if valor and campo in mapeamento_campos:
            campo_modelo = mapeamento_campos[campo]
            if isinstance(valor, str) and '%' in valor:
                query = query.filter(campo_modelo.ilike(valor))
            else:
                query = query.filter(campo_modelo == valor)
    return query


def validar_horario(horario: str) -> bool:
    """
    Valida um horário no formato HH:MM.
    
    Args:
        horario: String contendo o horário a ser validado
        
    Returns:
        bool: True se o horário é válido, False caso contrário
    """
    try:
        hora, minuto = map(int, horario.split(':'))
        return 0 <= hora <= 23 and 0 <= minuto <= 59
    except:
        return False


def calcular_imc(peso: float, altura: float) -> Dict[str, Union[float, str]]:
    """
    Calcula o IMC e retorna classificação.
    
    Args:
        peso: Peso em kg
        altura: Altura em metros
        
    Returns:
        Dict[str, Union[float, str]]: IMC e classificação
    """
    imc = peso / (altura ** 2)
    
    if imc < 18.5:
        classificacao = 'Abaixo do peso'
    elif imc < 25:
        classificacao = 'Peso normal'
    elif imc < 30:
        classificacao = 'Sobrepeso'
    elif imc < 35:
        classificacao = 'Obesidade grau 1'
    elif imc < 40:
        classificacao = 'Obesidade grau 2'
    else:
        classificacao = 'Obesidade grau 3'
    
    return {
        'imc': round(imc, 2),
        'classificacao': classificacao
    }


def gerar_codigo_verificacao() -> str:
    """
    Gera um código de verificação aleatório.
    
    Returns:
        str: Código de verificação de 6 dígitos
    """
    from random import randint
    return str(randint(100000, 999999))


def enviar_email_verificacao(email: str, codigo: str) -> bool:
    """
    Envia email com código de verificação.
    
    Args:
        email: Email do destinatário
        codigo: Código de verificação
        
    Returns:
        bool: True se enviou com sucesso, False caso contrário
    """
    try:
        # Implementar envio de email aqui
        return True
    except Exception as e:
        print(f'Erro ao enviar email: {e}')
        return False 