"""Testes unitários para as funções utilitárias do sistema."""

import pytest
from datetime import datetime, date
from backend.utils import (
    validar_cpf, validar_email, calcular_idade,
    formatar_cpf, formatar_telefone, formatar_moeda,
    salvar_foto, excluir_foto, verificar_permissao,
    verificar_token, paginar_query, aplicar_filtros,
    validar_horario, calcular_imc, gerar_codigo_verificacao,
    enviar_email_verificacao
)


def test_validar_cpf():
    """Testa a validação de CPF."""
    assert validar_cpf('123.456.789-09') is True
    assert validar_cpf('123.456.789-10') is False
    assert validar_cpf('123.456.789') is False
    assert validar_cpf('') is False
    assert validar_cpf('111.111.111-11') is False


def test_validar_email():
    """Testa a validação de email."""
    assert validar_email('teste@teste.com') is True
    assert validar_email('teste@teste') is False
    assert validar_email('teste.com') is False
    assert validar_email('') is False
    assert validar_email('@teste.com') is False


def test_calcular_idade():
    """Testa o cálculo de idade."""
    hoje = date.today()
    data_nascimento = date(hoje.year - 20, hoje.month, hoje.day)
    assert calcular_idade(data_nascimento) == 20
    
    data_nascimento = date(hoje.year - 30, hoje.month, hoje.day)
    assert calcular_idade(data_nascimento) == 30


def test_formatar_cpf():
    """Testa a formatação de CPF."""
    assert formatar_cpf('12345678909') == '123.456.789-09'
    assert formatar_cpf('123.456.789-09') == '123.456.789-09'
    assert formatar_cpf('') == ''
    assert formatar_cpf('123') == '123'


def test_formatar_telefone():
    """Testa a formatação de telefone."""
    assert formatar_telefone('11987654321') == '(11) 98765-4321'
    assert formatar_telefone('(11) 98765-4321') == '(11) 98765-4321'
    assert formatar_telefone('') == ''
    assert formatar_telefone('123') == '123'


def test_formatar_moeda():
    """Testa a formatação de valores monetários."""
    assert formatar_moeda(100.0) == 'R$ 100,00'
    assert formatar_moeda(1234.56) == 'R$ 1.234,56'
    assert formatar_moeda(0) == 'R$ 0,00'
    assert formatar_moeda(-100.0) == '-R$ 100,00'


def test_salvar_foto(tmp_path):
    """Testa o salvamento de fotos."""
    arquivo = tmp_path / 'test.jpg'
    arquivo.write_bytes(b'test')
    
    nome_arquivo = salvar_foto(arquivo, 'usuarios')
    assert nome_arquivo.startswith('usuarios/')
    assert nome_arquivo.endswith('.jpg')


def test_excluir_foto(tmp_path):
    """Testa a exclusão de fotos."""
    arquivo = tmp_path / 'test.jpg'
    arquivo.write_bytes(b'test')
    
    nome_arquivo = salvar_foto(arquivo, 'usuarios')
    assert excluir_foto(nome_arquivo) is True
    assert excluir_foto('arquivo_inexistente.jpg') is False


def test_verificar_permissao():
    """Testa a verificação de permissões."""
    class Usuario:
        def __init__(self, tipo):
            self.tipo = tipo
    
    @verificar_permissao(['gerente'])
    def funcao_gerente(usuario):
        return True
    
    gerente = Usuario('gerente')
    professor = Usuario('professor')
    
    assert funcao_gerente(gerente) is True
    with pytest.raises(Exception):
        funcao_gerente(professor)


def test_verificar_token():
    """Testa a verificação de tokens JWT."""
    token_valido = 'token_valido'
    token_invalido = 'token_invalido'
    
    assert verificar_token(token_valido) is True
    assert verificar_token(token_invalido) is False
    assert verificar_token('') is False


def test_paginar_query():
    """Testa a paginação de queries."""
    class MockQuery:
        def __init__(self, items):
            self.items = items
            
        def offset(self, offset):
            return self
            
        def limit(self, limit):
            return self
            
        def all(self):
            return self.items[:10]
            
        def count(self):
            return len(self.items)
    
    items = list(range(100))
    query = MockQuery(items)
    
    resultado = paginar_query(query, pagina=1, por_pagina=10)
    assert len(resultado.items) == 10
    assert resultado.total == 100
    assert resultado.paginas == 10
    assert resultado.tem_proxima is True
    assert resultado.tem_anterior is False


def test_aplicar_filtros():
    """Testa a aplicação de filtros em queries."""
    class MockQuery:
        def __init__(self):
            self.filtros = []
            
        def filter(self, filtro):
            self.filtros.append(filtro)
            return self
    
    query = MockQuery()
    filtros = {
        'nome': 'Teste',
        'status': 'ativo'
    }
    
    query_filtrada = aplicar_filtros(query, filtros)
    assert len(query_filtrada.filtros) == 2


def test_validar_horario():
    """Testa a validação de horários."""
    assert validar_horario('08:00') is True
    assert validar_horario('25:00') is False
    assert validar_horario('08:60') is False
    assert validar_horario('') is False
    assert validar_horario('8:00') is False


def test_calcular_imc():
    """Testa o cálculo de IMC."""
    assert calcular_imc(70.0, 1.75) == 22.86
    assert calcular_imc(0, 1.75) == 0
    assert calcular_imc(70.0, 0) == 0
    with pytest.raises(ValueError):
        calcular_imc(-70.0, 1.75)
    with pytest.raises(ValueError):
        calcular_imc(70.0, -1.75)


def test_gerar_codigo_verificacao():
    """Testa a geração de códigos de verificação."""
    codigo = gerar_codigo_verificacao()
    assert len(codigo) == 6
    assert codigo.isdigit()
    
    codigo2 = gerar_codigo_verificacao()
    assert codigo != codigo2  # Verifica aleatoriedade


def test_enviar_email_verificacao(mocker):
    """Testa o envio de email de verificação."""
    mock_enviar = mocker.patch('backend.utils.enviar_email')
    
    email = 'teste@teste.com'
    codigo = '123456'
    
    enviar_email_verificacao(email, codigo)
    
    mock_enviar.assert_called_once()
    args = mock_enviar.call_args[0]
    assert args[0] == email
    assert 'Código de Verificação' in args[1]
    assert codigo in args[2] 