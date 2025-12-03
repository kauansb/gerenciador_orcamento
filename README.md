# Gerenciador de Orçamento

Aplicação web em Flask para controlar categorias de orçamento e suas transações. Permite configurar limites por categoria, registrar despesas e acompanhar saldos e percentuais em um painel central.

## Visão Geral
- Camada de apresentação: templates Jinja2 em `app/templates` (layout base em `base.html`).
- Validação de formulários: `Flask-WTF` / `WTForms` (forms definidos em `app/forms.py`) com proteção CSRF habilitada.
- Lógica de negócio: camada de serviços em `app/services/` (ex.: `categoria_service.py`, `transacao_service.py`) — transações DB, validações de domínio e mensagens de erro padronizadas.
- Persistência: `Flask-SQLAlchemy` com SQLite por padrão (arquivo `instance/orcamento.db`).

## Funcionalidades
- CRUD de categorias com limite financeiro e validações de unicidade
- CRUD de transações vinculadas a categorias com validação de limite
- Dashboard com visão consolidada (limite, gasto, saldo, percentual)
- Mensagens de feedback via `flash` e validação de formulário no servidor
- Ícones via Font Awesome CDN (referência no `base.html`)

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
python run.py
```

Use `FLASK_ENV=production python run.py` em produção e assegure que `SECRET_KEY` esteja definido com um valor seguro.

### Observações sobre banco de dados
- O projeto usa SQLite por padrão (arquivo em `instance/orcamento.db`). Em provedores que reiniciam/rodam em containers (Render, Railway, Heroku), o filesystem pode ser efêmero — recomendamos migrar para Postgres (ex.: `DATABASE_URL`) para persistência.

## Estrutura do Projeto
```
app/
  __init__.py       # Factory do Flask, inicializa DB e CSRF
  models.py         # Modelos Categoria e Transacao + regras de validação
  routes.py         # Rotas (apresentação) — usam forms e services
  forms.py          # WTForms: CategoryForm e TransactionForm
  services/         # Camada de serviços: lógica de negócio e gerenciamento de transações
    __init__.py
    categoria_service.py
    transacao_service.py
  templates/        # Páginas HTML (Jinja2)
  static/           # Assets (CSS, JS)
config.py           # Configurações (dev/test/prod)
requirements.txt    # Dependências do projeto
run.py              # Script para subir o servidor Flask
```

## Fluxo Básico de Uso
1. Criar uma categoria em `/categorias/nova`, definindo nome e limite.
2. Cadastrar transações em `/transacoes/nova`, escolhendo a categoria.
3. Acompanhar o dashboard em `/` para ver limites, gastos e saldos.