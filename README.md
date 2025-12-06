# Gerenciador de Orçamento

Aplicação web em Flask para controlar categorias de orçamento e suas transações. Permite configurar limites por categoria, registrar despesas e acompanhar saldos e percentuais em um painel central.

## Visão Geral
- **Apresentação:** Templates Jinja2 em `app/templates` com layout reutilizável (`base.html`)
- **Formulários:** WTForms com proteção CSRF habilitada
- **Lógica de negócio:** Serviços simples em `app/services/`
- **Models:** SQLAlchemy com `@property` para cálculos automáticos (gasto, saldo, percentual)
- **Persistência:** SQLite por padrão

## Funcionalidades
- CRUD de categorias com limite financeiro
- CRUD de transações vinculadas a categorias
- Dashboard com visão consolidada (limite, gasto, saldo, percentual)
- Feedback via mensagens flash
- Validação de formulários no servidor
- Atualização de saldo em tempo real (JavaScript)

## Tecnologias
- Python 3.8+
- Flask
- Flask-WTF
- Flask-SQLAlchemy
- SQLAlchemy
- WTForms

## Pré-requisitos
- Python 3.8 ou superior
- Pip atualizado (`python -m pip install --upgrade pip`)

## Configuração do Ambiente
```powershell
# 1. Criar ambiente virtual
python -m venv venv

# 2. Ativar o virtualenv (PowerShell)
.\venv\Scripts\Activate.ps1

# 3. Instalar dependências
pip install -r requirements.txt
```

## Executando a Aplicação

### Desenvolvimento
```powershell
# Com ambiente ativado
flask run
```

A aplicação estará disponível em `http://127.0.0.1:5000`

## Estrutura do Projeto
```
gerenciador_orcamento/
├── app/
│   ├── __init__.py         # Factory do Flask (create_app)
│   ├── models.py           # Categoria e Transacao com @property
│   ├── forms.py            # Formulários WTForms com validações
│   ├── routes.py           # Rotas HTTP (Blueprints)
│   ├── services/
│   │   ├── __init__.py
│   │   ├── categoria_service.py
│   │   └── transacao_service.py
│   ├── templates/          # Páginas HTML (Jinja2)
│   └── static/             # CSS e JavaScript
├── instance/               # Banco de dados SQLite
├── config.py               # Configurações
├── requirements.txt        # Dependências
└── run.py                  # Ponto de entrada
```

## Fluxo Básico de Uso
1. Criar uma categoria em `/categorias/nova`, definindo nome e limite
2. Cadastrar transações em `/transacoes/nova`, escolhendo a categoria
3. Acompanhar o dashboard em `/` para ver limites, gastos e saldos

## Rotas Disponíveis
| Rota | Método | Descrição |
|------|--------|-----------|
| `/` | GET | Dashboard principal |
| `/categorias/` | GET | Listar categorias |
| `/categorias/nova` | GET/POST | Criar categoria |
| `/categorias/editar/<id>` | GET/POST | Editar categoria |
| `/categorias/deletar/<id>` | POST | Deletar categoria |
| `/transacoes/` | GET | Listar transações |
| `/transacoes/nova` | GET/POST | Criar transação |
| `/transacoes/editar/<id>` | GET/POST | Editar transação |
| `/transacoes/deletar/<id>` | POST | Deletar transação |