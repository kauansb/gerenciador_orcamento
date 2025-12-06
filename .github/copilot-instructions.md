# Copilot Instructions for Gerenciador de Orçamento

## Architecture Overview

**Gerenciador de Orçamento** is a Flask budget management web application with a three-layer architecture:

```
routes.py (3 blueprints) → services/ (business logic) → models.py (SQLAlchemy ORM)
                                                    ↓
                                              SQLite database
```

- **Routes**: Flask blueprints organize CRUD operations into three modules: `main_bp` (dashboard), `categoria_bp` (budget categories), `transacao_bp` (transactions/expenses)
- **Services**: Simple layer in `app/services/` handles persistence directly using models and `db.session` (no complex business logic)
- **Models**: SQLAlchemy models with computed properties (`@property`) for derived values like `gasto`, `saldo`, `percentual`

## Key Design Patterns

### Model Computed Properties
Models in `app/models.py` use `@property` decorators for real-time calculations instead of database columns:
```python
@property
def saldo(self):
    """Saldo restante do orçamento."""
    return self.limite - self.gasto

@property
def percentual(self):
    """Percentual de orçamento gasto."""
    if self.limite == 0:
        return 0
    return (self.gasto / self.limite) * 100
```
These properties are accessed directly in templates and views without requiring database queries.

### Blueprint Organization
Each functional domain uses a separate blueprint with consistent patterns:
- **Main blueprint**: Single route for dashboard (`/`)
- **Categoria blueprint**: CRUD routes under `/categorias` prefix
- **Transacao blueprint**: CRUD routes under `/transacoes` prefix

All routes follow the pattern: `listar()`, `nova()`, `editar(id)`, `deletar(id)`.

### Form Validation
WTForms with custom validators in `app/forms.py`:
- CSRF protection enabled globally via `CSRFProtect(app)` in `__init__.py`
- All forms include `DeleteForm` with CSRF token only
- Custom validators like `validate_nome()` handle edge cases (empty strings after strip)

### Service Layer Pattern
Services in `app/services/` wrap model operations:
- Accept simple types (not SQLAlchemy objects)
- Directly manipulate `db.session`
- Return model instances
- Example: `criar_categoria(nome, limite)` → `criar_transacao(descricao, valor, categoria_id)`

## Critical Workflows

### Running the Application

#### Development
```powershell
# 1. Activate virtual environment
.\venv\Scripts\Activate.ps1

# 2. Run development server
flask run
```
Server listens on `http://127.0.0.1:5000`. Database auto-creates tables on startup via `db.create_all()` in `create_app()`.

#### Production (Gunicorn)
```bash
gunicorn --bind 0.0.0.0:5000 --workers 2 wsgi:app
```
Use `wsgi.py` as entry point (not `run.py` or `app.run()` in production).

### Database
- **Location**: `instance/orcamento.db` (SQLite, auto-created)
- **Relationships**: One-to-many from `Categoria` → `Transacao` with cascading deletes (`cascade='all, delete-orphan'`)
- **Configuration**: See `config.py` for database URI and Flask settings
- **Production**: Support for PostgreSQL/MySQL via `DATABASE_URL` environment variable

### Environment Variables
All configuration uses environment variables for production safety:
- `SECRET_KEY`: Cryptographic key for sessions/CSRF (required in production, use `secrets.token_urlsafe(32)`)
- `FLASK_ENV`: Set to `'production'` for deployed instances
- `FLASK_DEBUG`: Must be `'False'` in production
- `DATABASE_URL`: Optional PostgreSQL/MySQL connection string (defaults to SQLite)
- `SESSION_COOKIE_SECURE`: Set to `'True'` when using HTTPS

**Setup**: Copy `.env.example` to `.env` and configure variables. Use `python setup_deploy.py` helper script.

## Project-Specific Conventions

### Flash Messages Pattern
All CRUD operations use flash messaging for user feedback:
```python
try:
    criar_categoria(form.nome.data, float(form.limite.data))
    flash('Categoria criada com sucesso!', 'success')
    return redirect(url_for('categoria.listar'))
except Exception as e:
    flash(f'Erro: {str(e)}', 'error')
```
Always redirect after success; return same template on GET or validation failure.

### Template Context
Templates inherit from `base.html` and receive context with:
- **Categories view**: Individual categories + `total_limite`, `total_gasto`, `total_saldo`
- **Transactions view**: Individual transactions
- **Forms**: Flash messages automatically rendered by base template

### Field Casting
Route handlers explicitly cast form data to types (e.g., `float(form.limite.data)`) before passing to services—not done in service layer.

## Directory Structure
```
app/
├── __init__.py          # Flask app factory (create_app)
├── models.py            # SQLAlchemy models: Categoria, Transacao
├── routes.py            # Flask blueprints with CRUD endpoints
├── forms.py             # WTForms: CategoryForm, TransactionForm, DeleteForm
├── services/            # Persistence layer
│   ├── categoria_service.py
│   └── transacao_service.py
├── static/
│   ├── css/site.css
│   └── js/site.js       # Real-time balance updates (if needed)
└── templates/
    ├── base.html        # Jinja2 base with flash messaging
    ├── index.html       # Dashboard
    ├── categorias.html, nova_categoria.html, editar_categoria.html
    └── transacoes.html, nova_transacao.html, editar_transacao.html
```

## Editing Guidelines

- **Adding fields to models**: Update `models.py`, then create Flask migration or delete `instance/orcamento.db` to regenerate
- **Adding routes**: Use existing blueprint in `routes.py`; add service methods to `app/services/`
- **Modifying forms**: Edit `app/forms.py` and update corresponding template
- **Form data flow**: Route → Service layer (simple types) → Models → Database
- **Type conversions**: Always happen in routes before service layer calls

## Technology Stack
- **Framework**: Flask + Flask-SQLAlchemy + Flask-WTF
- **ORM**: SQLAlchemy with computed properties
- **Forms**: WTForms with CSRF protection
- **Database**: SQLite
- **Templating**: Jinja2
