<div align="center">

```
 ▄████  ▄██   ▄   ▄▄▄▄███▄▄▄▄      ▄████████  ▄█        ▄██████▄   ▄█     █▄  
███    ███   ██▄ ▄██▀▀▀███▀▀▀██▄   ███    ███ ███       ███    ███ ███     ███ 
███    ███▄   ███▄███   ███   ███   ███    █▀  ███       ███    ███ ███     ███ 
███    ▀▀▀▀   ███▀███   ███   ███  ▄███▄▄▄     ███       ███    ███ ███     ███ 
███        ▄███▀███   ███   ███ ▀▀███▀▀▀     ███       ███    ███ ███     ███ 
███    █▄  ███   ███   ███   ███   ███    █▄  ███       ███    ███ ███     ███ 
███    ███ ███   ███   ███   ███   ███    ███ ███▌    ▄ ███    ███ ███ ▄█▄ ███ 
████████▀  ███   ███   ███   █▀    ██████████ █████▄▄██  ▀██████▀   ▀███▀███▀  
```

<h3>🏋️‍♂️ Sistema Inteligente de Gestão para Academias</h3>

[![Tech Stack](https://img.shields.io/badge/Tech%20Stack-Python%20%7C%20Flask-4B8BBE?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Framework](https://img.shields.io/badge/Framework-Bootstrap%205-7952B3?style=for-the-badge&logo=bootstrap&logoColor=white)](https://getbootstrap.com/)
[![Database](https://img.shields.io/badge/Database-SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white)](https://www.sqlite.org/)
[![License](https://img.shields.io/badge/License-GPL%20v3-blue.svg?style=for-the-badge&logo=gnu&logoColor=white)](LICENSE)

[📋 Sobre](#-sobre) • 
[💪 Recursos](#-recursos) • 
[🛠️ Tecnologias](#️-tecnologias) • 
[🚀 Instalação](#-instalação) • 
[📱 Demo](#-demo)

</div>

## 📋 Sobre

<div align="center">

```mermaid
graph TD
    A[GymFlow] --> B[Gestão de Usuários]
    A --> C[Gestão de Alunos]
    A --> D[Gestão de Treinos]
    A --> E[Gestão de Turmas]
    A --> F[Gestão Financeira]
    
    B --> B1[Perfis]
    B --> B2[Autenticação]
    
    C --> C1[Matrículas]
    C --> C2[Histórico]
    
    D --> D1[Exercícios]
    D --> D2[Evolução]
    
    E --> E1[Aulas]
    E --> E2[Presença]
    
    F --> F1[Pagamentos]
    F --> F2[Relatórios]

    style A fill:#ff9900,stroke:#fff,stroke-width:2px
    style B fill:#4B8BBE,stroke:#fff,stroke-width:2px
    style C fill:#4B8BBE,stroke:#fff,stroke-width:2px
    style D fill:#4B8BBE,stroke:#fff,stroke-width:2px
    style E fill:#4B8BBE,stroke:#fff,stroke-width:2px
    style F fill:#4B8BBE,stroke:#fff,stroke-width:2px
```

</div>

## 💪 Recursos

<table align="center">
  <tr>
    <td align="center" width="33%">
      <img width="64" src="https://raw.githubusercontent.com/tandpfun/skill-icons/main/icons/PersonalTrainer.svg" alt="Gestão de Alunos"/>
      <br/><strong>Gestão de Alunos</strong>
      <br/>Sistema completo de cadastro e acompanhamento
      <br/>
      <sub>• Fichas completas<br/>• Evolução física<br/>• Histórico de treinos</sub>
    </td>
    <td align="center" width="33%">
      <img width="64" src="https://raw.githubusercontent.com/tandpfun/skill-icons/main/icons/Workout.svg" alt="Gestão de Treinos"/>
      <br/><strong>Gestão de Treinos</strong>
      <br/>Planejamento e acompanhamento de treinos
      <br/>
      <sub>• Exercícios personalizados<br/>• Séries adaptativas<br/>• Métricas de progresso</sub>
    </td>
    <td align="center" width="33%">
      <img width="64" src="https://raw.githubusercontent.com/tandpfun/skill-icons/main/icons/Money.svg" alt="Gestão Financeira"/>
      <br/><strong>Gestão Financeira</strong>
      <br/>Controle completo de pagamentos
      <br/>
      <sub>• Mensalidades<br/>• Relatórios detalhados<br/>• Controle de inadimplência</sub>
    </td>
  </tr>
</table>

## 🛠️ Stack Tecnológica

<div align="center">

| Back-end | Front-end | Database | DevOps |
|----------|-----------|----------|---------|
| ![Python](https://raw.githubusercontent.com/tandpfun/skill-icons/main/icons/Python-Dark.svg) | ![Bootstrap](https://raw.githubusercontent.com/tandpfun/skill-icons/main/icons/Bootstrap.svg) | ![SQLite](https://raw.githubusercontent.com/tandpfun/skill-icons/main/icons/SQLite.svg) | ![Git](https://raw.githubusercontent.com/tandpfun/skill-icons/main/icons/Git.svg) |
| ![Flask](https://raw.githubusercontent.com/tandpfun/skill-icons/main/icons/Flask-Dark.svg) | ![JavaScript](https://raw.githubusercontent.com/tandpfun/skill-icons/main/icons/JavaScript.svg) | ![SQLAlchemy](https://raw.githubusercontent.com/tandpfun/skill-icons/main/icons/MySQL-Dark.svg) | ![Docker](https://raw.githubusercontent.com/tandpfun/skill-icons/main/icons/Docker.svg) |

</div>

## 🚀 Instalação

<details>
<summary>💻 Instalação Local</summary>

```bash
# Clone o repositório
git clone https://github.com/seu-usuario/gymflow.git && cd gymflow

# Configure o ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Instale as dependências
pip install -r requirements.txt

# Configure o ambiente
cp .env.example .env

# Inicialize o banco
flask db upgrade
```
</details>

<details>
<summary>☁️ GitHub Codespaces</summary>

```bash
# Inicie diretamente com
python run.py
```
</details>

## 🔐 Acessos

<div align="center">

| Perfil | Credenciais | Permissões |
|--------|-------------|------------|
| 🎖️ **Admin** | admin@gymflow.com<br>admin123 | Acesso total |
| 💪 **Professor** | prof@gymflow.com<br>prof123 | Treinos e alunos |
| 📋 **Recepção** | recepcao@gymflow.com<br>recepcao123 | Cadastros e pagamentos |

</div>

## 📂 Estrutura

```plaintext
🏋️ GymFlow/
├── 🎯 backend/
│   ├── 📊 models/
│   ├── 🛣️ routes/
│   └── ⚙️ utils/
├── 🎨 frontend/
│   ├── 📱 assets/
│   └── 📄 templates/
├── 🔒 config/
└── 📚 docs/
```

## 🤝 Contribuição

```mermaid
gitGraph
   commit
   commit
   branch feature
   checkout feature
   commit
   commit
   checkout main
   merge feature
   commit
```

1. Fork
2. Branch (`git checkout -b feature/NewFeature`)
3. Commit (`git commit -m 'Add: nova feature'`)
4. Push (`git push origin feature/NewFeature`)
5. PR

## 👨‍💻 Autor

<div align="center">
  <img width="200" height="200" src="https://raw.githubusercontent.com/tandpfun/skill-icons/main/icons/Github-Dark.svg">
  <h3>Kelvin Moraes</h3>
  <p>Full Stack Developer | Fitness Enthusiast</p>
  
[![GitHub](https://img.shields.io/badge/GitHub-KerubinDev-181717?style=for-the-badge&logo=github)](https://github.com/KerubinDev)
[![Email](https://img.shields.io/badge/Email-kelvin.moraes117@gmail.com-EA4335?style=for-the-badge&logo=gmail)](mailto:kelvin.moraes117@gmail.com)
</div>

---

<div align="center">
  
  **[⬆ Voltar ao topo](#gymflow---sistema-de-gestão-para-academias)**
  
  <sub>Desenvolvido com 💪 por Kelvin Moraes</sub>
  
[![Stack](https://img.shields.io/badge/Stack-Python%20%7C%20Flask%20%7C%20Bootstrap-000000?style=for-the-badge)](https://github.com/KerubinDev/GymFlow)
</div>
