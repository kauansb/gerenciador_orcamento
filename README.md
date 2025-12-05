# Gerenciador de Orçamento

Aplicação web em Flask para controlar categorias de orçamento e suas transações. Permite configurar limites por categoria, registrar despesas e acompanhar saldos e percentuais em um painel central.

## Visão Geral
- **Apresentação:** Templates Jinja2 em `app/templates` com layout reutilizável (`base.html`)
- **Formulários:** WTForms com proteção CSRF habilitada
- **Lógica de negócio:** Serviços simples em `app/services/`
- **Models:** SQLAlchemy com métodos de cálculo
- **Persistência:** SQLite por padrão

## Funcionalidades
- CRUD de categorias com limite financeiro
- CRUD de transações vinculadas a categorias
- Dashboard com visão consolidada (limite, gasto, saldo, percentual)
- Feedback via mensagens flash
- Validação de formulários no servidor
- Atualização de saldo em tempo real (JavaScript)

## Tecnologias
- Python 3.11+ (recomenda-se 3.11 ou 3.12; ver nota sobre SQLAlchemy/Python 3.13)
- Flask 3.x, Flask-WTF, Flask-SQLAlchemy
- SQLAlchemy 2.x
- WTForms

## Pré-requisitos
- Python 3.11 ou 3.12 (recomendado)
- Pip atualizado (`python -m pip install --upgrade pip`)

## Configuração do Ambiente
```powershell
# 1. Criar ambiente virtual (recomendado)
python -m venv .venv

# 2. Ativar o virtualenv (PowerShell)
.\.venv\Scripts\Activate.ps1

# 3. Instalar dependências
pip install -r requirements.txt
```

## Variáveis de Ambiente
| Variável | Descrição | Valor padrão |
| --- | --- | --- |
| `FLASK_ENV` | Perfil (`development`, `production`, `testing`) | `development` |
| `FLASK_HOST` | Host utilizado pelo servidor | `0.0.0.0` |
| `FLASK_PORT` | Porta utilizada pelo servidor | `5000` |
| `SECRET_KEY` | Chave para sessões e CSRF | `dev-secret-key-change-in-production` |

## Executando a Aplicação
```powershell
# Com ambiente ativado
flask run
```

Use `FLASK_ENV=production flask run` em produção e assegure que `SECRET_KEY` esteja definido com um valor seguro.

### Observações sobre banco de dados
- O projeto usa SQLite por padrão (arquivo em `instance/orcamento.db`). Em provedores que reiniciam/rodam em containers (Render, Railway, Heroku), o filesystem pode ser efêmero — recomendamos migrar para Postgres (ex.: `DATABASE_URL`) para persistência.

## Estrutura do Projeto
```
app/
  __init__.py           # Factory do Flask
  models.py             # Categoria e Transacao com métodos de cálculo
  routes.py             # Rotas HTTP (CRUD)
  forms.py              # Formulários WTForms com validações
  services/
    categoria_service.py    # Lógica para Categoria
    transacao_service.py    # Lógica para Transacao
  templates/            # Páginas HTML (Jinja2)
  static/               # CSS e JavaScript
instance/               # Banco de dados local (SQLite)
config.py               # Configurações
requirements.txt        # Dependências
run.py                  # Iniciar servidor
```

## Fluxo Básico de Uso
1. Criar uma categoria em `/categorias/nova`, definindo nome e limite.
2. Cadastrar transações em `/transacoes/nova`, escolhendo a categoria.
3. Acompanhar o dashboard em `/` para ver limites, gastos e saldos.