# GymFlow - Sistema de Gestão para Academias

Sistema completo para gestão de academias desenvolvido em Python/Flask, oferecendo funcionalidades para gerenciamento de alunos, professores, treinos, turmas e pagamentos.

## Funcionalidades

- **Gestão de Usuários**
  - Cadastro de gerentes, professores e recepcionistas
  - Controle de acesso baseado em perfis
  - Autenticação segura

- **Gestão de Alunos**
  - Cadastro completo com dados pessoais
  - Histórico de treinos
  - Controle de pagamentos
  - Matrícula em turmas

- **Gestão de Treinos**
  - Criação de treinos personalizados
  - Biblioteca de exercícios
  - Acompanhamento de evolução
  - Histórico de treinos

- **Gestão de Turmas**
  - Agendamento de aulas
  - Controle de capacidade
  - Diferentes modalidades
  - Lista de presença

- **Gestão Financeira**
  - Controle de mensalidades
  - Histórico de pagamentos
  - Relatórios financeiros
  - Status de inadimplência

## Tecnologias Utilizadas

- Python 3.8+
- Flask (Framework Web)
- SQLAlchemy (ORM)
- Flask-Login (Autenticação)
- Bootstrap 5 (Frontend)
- Chart.js (Gráficos)
- SQLite (Banco de Dados)

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
venv\\Scripts\\activate   # Windows
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
python run.py
```

## Uso

1. Acesse o sistema através do navegador: `http://localhost:5000`
2. Faça login com as credenciais padrão:
   - Email: admin@gymflow.com
   - Senha: admin123

## Estrutura do Projeto

```
gymflow/
├── backend/
│   ├── __init__.py
│   ├── models.py
│   └── routes.py
├── migrations/
├── static/
│   ├── css/
│   └── js/
├── templates/
├── instance/
├── .env
├── .gitignore
├── requirements.txt
└── run.py
```

## Contribuição

1. Faça um Fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## Licença

Este projeto está licenciado sob a GNU General Public License v3.0 - veja o arquivo [LICENSE](LICENSE) para detalhes.

## Autor

**Kelvin Moraes (Kerubin)**
- Email: kelvin.moraes117@gmail.com
- GitHub: [@KerubinDev](https://github.com/KerubinDev)
- Projeto: [GymFlow](https://github.com/KerubinDev/GymFlow)

## Agradecimentos

- [Bootstrap](https://getbootstrap.com)
- [Chart.js](https://www.chartjs.org)
- [Flask](https://flask.palletsprojects.com)
- [Font Awesome](https://fontawesome.com)