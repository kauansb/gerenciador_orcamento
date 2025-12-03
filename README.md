# Gerenciador de Orçamento

Aplicação web em Flask para controlar categorias de orçamento e suas transações. Permite configurar limites por categoria, registrar despesas e acompanhar saldos e percentuais em um painel central.

## Visão Geral
- **Camada de apresentação:** templates Jinja2 em `app/templates` (layout base em `base.html`).
- **Validação de formulários:** `Flask-WTF` / `WTForms` (forms definidos em `app/forms.py`) com proteção CSRF habilitada.
- **Lógica de negócio:** camada de serviços em `app/services/` com transações DB, validações de domínio e mensagens de erro padronizadas.
- **Roteamento simplificado:** decoradores (`app/decorators.py`) para tratamento automático de erros; helpers (`app/helpers.py`) para formatação de dados.
- **Persistência:** `Flask-SQLAlchemy` com SQLite por padrão (arquivo `instance/orcamento.db`).

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
flask run
```

Use `FLASK_ENV=production flask run` em produção e assegure que `SECRET_KEY` esteja definido com um valor seguro.

### Observações sobre banco de dados
- O projeto usa SQLite por padrão (arquivo em `instance/orcamento.db`). Em provedores que reiniciam/rodam em containers (Render, Railway, Heroku), o filesystem pode ser efêmero — recomendamos migrar para Postgres (ex.: `DATABASE_URL`) para persistência.

## Estrutura do Projeto
```
app/
  __init__.py           # Factory do Flask, inicializa DB e CSRF
  models.py             # Modelos Categoria e Transacao com métodos de cálculo
  routes.py             # Rotas (apresentação) — simplificadas com decoradores
  forms.py              # WTForms: CategoryForm e TransactionForm com validações
  decorators.py         # Decoradores para tratamento automático de erros
  helpers.py            # Funções para formatação de dados para templates
  services/             # Camada de serviços (lógica de negócio)
    __init__.py         # Exceções: BusinessRuleError, NotFoundError
    categoria_service.py
    transacao_service.py
  templates/            # Páginas HTML (Jinja2)
  static/               # Assets (CSS, JS)
config.py               # Configurações (development/testing/production)
requirements.txt        # Dependências do projeto
run.py                  # Script para subir o servidor Flask
```

## Fluxo Básico de Uso
1. Criar uma categoria em `/categorias/nova`, definindo nome e limite.
2. Cadastrar transações em `/transacoes/nova`, escolhendo a categoria.
3. Acompanhar o dashboard em `/` para ver limites, gastos e saldos.

## Arquitetura: Camadas e Separação de Responsabilidades

### 1. **Forms** (`app/forms.py`)
Valida entrada do usuário:
- Tipo de campo (string, decimal, etc)
- Presença (obrigatório)
- Tamanho (max length)
- Unicidade simples (verifica no BD)

```python
class CategoryForm(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired(), Length(max=100)])
    limite = DecimalField('Limite', places=2, validators=[DataRequired(), NumberRange(min=0.01)])
```

### 2. **Services** (`app/services/`)
Encapsula lógica de negócio:
- Validações de regra de negócio (limite > gasto?)
- Gerenciamento de transações DB (commit/rollback)
- Exceções específicas (BusinessRuleError, NotFoundError)

```python
def create_category(nome: str, limite: float) -> Categoria:
    if limite <= 0:
        raise BusinessRuleError('Limite deve ser um valor positivo.')
    # ... lógica de criação
```

### 3. **Decoradores** (`app/decorators.py`) — **Novo**
Simplifica tratamento de erros nas rotas:
- Captura exceções de serviço automaticamente
- Exibe mensagens amigáveis ao usuário
- Redireciona para endpoint correto

```python
@categoria_bp.route('/nova', methods=['GET', 'POST'])
@handle_service_errors('categoria.nova_categoria')  # Trata erros automaticamente
def nova_categoria():
    # Código limpo, sem try/except
    pass
```

### 4. **Helpers** (`app/helpers.py`) — **Novo**
Formata dados para templates:
- Reutiliza lógica de transformação
- Evita duplicação em routes
- Facilita manutenção

```python
dados_categorias = format_categorias(categorias)  # Retorna lista pronta
```

### 5. **Routes** (`app/routes.py`)
Orquestra requisições HTTP:
- Recebe e valida formulário
- Chama service com dados validados
- Formata resposta (redirect, render template)

```python
@categoria_bp.route('/nova', methods=['GET', 'POST'])
@handle_service_errors('categoria.nova_categoria')
def nova_categoria():
    form = CategoryForm()
    if form.validate_on_submit():
        create_category(form.nome.data.strip(), float(form.limite.data))
        flash_success('Categoria criada com sucesso!')
        return redirect(url_for('categoria.listar_categorias'))
    return render_template('nova_categoria.html', form=form)
```

## Exemplos de Uso

### Criar Categoria (Simplificado com Decorador)
```python
@categoria_bp.route('/nova', methods=['GET', 'POST'])
@handle_service_errors('categoria.nova_categoria')  # ← Trata erro automaticamente
def nova_categoria():
    form = CategoryForm()
    if form.validate_on_submit():
        create_category(form.nome.data.strip(), float(form.limite.data))
        flash_success('Categoria criada!')
        return redirect(url_for('categoria.listar_categorias'))
    return render_template('nova_categoria.html', form=form)
```

### Formatar Dados (Reutilizável com Helpers)
```python
@categoria_bp.route('/')
def listar_categorias():
    categorias = Categoria.query.all()
    return render_template('categorias.html', categorias=format_categorias(categorias))
```