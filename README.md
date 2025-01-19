# GymFlow - Sistema de Gestão para Academias

O GymFlow é um sistema web completo para gestão de academias, desenvolvido com Python/Flask no backend e Bootstrap/JavaScript no frontend.

## Funcionalidades

- **Gestão de Alunos**
  - Cadastro e edição de alunos
  - Controle de mensalidades
  - Acompanhamento de medidas e objetivos
  - Upload de fotos

- **Gestão de Treinos**
  - Criação e personalização de treinos
  - Acompanhamento de evolução
  - Diferentes modalidades (musculação, cardio, etc.)

- **Gestão de Turmas**
  - Grade de horários
  - Controle de capacidade
  - Reserva de vagas

- **Gestão Financeira**
  - Controle de pagamentos
  - Relatórios de receitas
  - Controle de inadimplência

- **Gestão de Usuários**
  - Diferentes níveis de acesso (gerente, professor, recepcionista)
  - Controle de permissões
  - Perfis personalizados

## Tecnologias Utilizadas

- **Backend**
  - Python 3.8+
  - Flask
  - SQLAlchemy
  - Flask-Login
  - Flask-JWT-Extended
  - Pillow (para processamento de imagens)

- **Frontend**
  - HTML5
  - CSS3
  - JavaScript
  - Bootstrap 5
  - Chart.js (para gráficos)

- **Banco de Dados**
  - SQLite (desenvolvimento)
  - PostgreSQL (produção)

## Instalação

1. Clone o repositório:
```bash
git clone https://github.com/seu-usuario/gymflow.git
cd gymflow
```

2. Crie um ambiente virtual e ative-o:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

4. Configure as variáveis de ambiente:
```bash
cp .env.example .env
# Edite o arquivo .env com suas configurações
```

5. Inicialize o banco de dados:
```bash
flask db upgrade
```

6. Execute o servidor de desenvolvimento:
```bash
flask run
```

## Estrutura do Projeto

```
gymflow/
├── backend/
│   ├── __init__.py
│   ├── models.py
│   ├── routes.py
│   └── utils.py
├── templates/
│   ├── base.html
│   ├── login.html
│   ├── dashboard.html
│   ├── treinos.html
│   ├── cadastro_alunos.html
│   ├── gestao_pagamentos.html
│   ├── horarios_turmas.html
│   └── cadastro_usuarios.html
├── static/
│   ├── css/
│   ├── js/
│   └── img/
├── migrations/
├── tests/
├── .env
├── .gitignore
├── config.py
├── requirements.txt
└── run.py
```

## Configuração

O arquivo `.env` deve conter as seguintes variáveis:

```env
FLASK_APP=run.py
FLASK_ENV=development
SECRET_KEY=sua-chave-secreta
DATABASE_URL=sqlite:///gymflow.db
UPLOAD_FOLDER=uploads
```

## Uso

1. Acesse `http://localhost:5000` no navegador
2. Faça login com as credenciais padrão:
   - Email: admin@gymflow.com
   - Senha: admin123

## Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## Licença

Este projeto está licenciado sob a licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

## Contato

Seu Nome - [@seutwitter](https://twitter.com/seutwitter) - email@exemplo.com

Link do Projeto: [https://github.com/seu-usuario/gymflow](https://github.com/seu-usuario/gymflow)

## Agradecimentos

- [Bootstrap](https://getbootstrap.com)
- [Flask](https://flask.palletsprojects.com)
- [Chart.js](https://www.chartjs.org)
- [Font Awesome](https://fontawesome.com)