# Gerenciador de Orçamento

Aplicação web em Flask para controlar categorias de orçamento e suas transações. Permite configurar limites para cada categoria, registrar despesas e acompanhar o saldo restante em um painel centralizado.

## Funcionalidades
- Cadastro, edição e exclusão de categorias com limite financeiro e validação de valores duplicados
- Registro de transações vinculadas a categorias com bloqueio automático quando o limite seria excedido
- Dashboard com visão consolidada de limite, gasto, saldo e percentual consumido por categoria
- Listagens dedicadas para categorias e transações com filtros básicos e feedback amigável via mensagens flash
- Persistência local em SQLite criada automaticamente na pasta `instance/`

## Tecnologias
- Python 3.11+
- Flask 3 e Blueprint Architecture
- Flask-SQLAlchemy / SQLAlchemy 2 / Flask-WTF
- HTML + Jinja2 + Bootstrap (templates em `app/templates`)

## Pré-requisitos
- Python 3.11 ou superior instalado
- Pip atualizado (`python -m pip install --upgrade pip`)

## Configuração do Ambiente
```powershell
# 1. Criar ambiente virtual (opcional, mas recomendado)
python -m venv .venv

# 2. Ativar o virtualenv (PowerShell)
.\.venv\Scripts\Activate.ps1

# 3. Instalar dependências
pip install -r requirements.txt
```

## Variáveis de Ambiente
| Variável | Descrição | Valor padrão |
| --- | --- | --- |
| `FLASK_ENV` | Define o perfil (`development`, `production`, `testing`) | `development` |
| `FLASK_HOST` | Host utilizado pelo servidor | `0.0.0.0` |
| `FLASK_PORT` | Porta utilizada pelo servidor | `5000` |
| `SECRET_KEY` | Chave para sessões Flask | `dev-secret-key-change-in-production` |

## Executando a Aplicação
```powershell
# Com ambiente ativado
python run.py
```

Use `FLASK_ENV=production python run.py` em ambientes de produção e configure `SECRET_KEY` com um valor seguro antes do deploy. O banco `instance/orcamento.db` será criado automaticamente se não existir.

## Estrutura do Projeto
```
app/
  __init__.py       # Factory do Flask e registro dos blueprints
  models.py         # Modelos Categoria e Transacao + regras de validação
  routes.py         # Rotas principais, categorias e transações
  forms.py          # Validações de formulário
  templates/        # Páginas HTML baseadas em Jinja2
config.py           # Configurações (dev/test/prod)
requirements.txt    # Dependências do projeto
run.py              # Script para subir o servidor Flask
```

## Fluxo Básico de Uso
1. Criar uma categoria em `/categorias/nova`, definindo nome e limite.
2. Cadastrar transações em `/transacoes/nova`, escolhendo a categoria.
3. Acompanhar o dashboard em `/` para ver limites, gastos e saldos.