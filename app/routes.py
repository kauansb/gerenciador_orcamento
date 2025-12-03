from flask import Blueprint, render_template, request, redirect, url_for
from app.models import Categoria, Transacao
from app.forms import CategoryForm, TransactionForm
from app.decorators import handle_service_errors, flash_success
from app.helpers import format_categorias, format_transacoes
from app.services.categoria_service import create_category, update_category, delete_category
from app.services.transacao_service import create_transaction, update_transaction, delete_transaction


# Criar blueprints
main_bp = Blueprint('main', __name__)
categoria_bp = Blueprint('categoria', __name__, url_prefix='/categorias')
transacao_bp = Blueprint('transacao', __name__, url_prefix='/transacoes')


# ============================================================================
# ROTAS PRINCIPAIS
# ============================================================================

@main_bp.route('/')
def index():
    """Dashboard principal mostrando resumo de categorias."""
    categorias = Categoria.query.all()
    dados_categorias = format_categorias(categorias)
    
    total_limite = sum(c['limite'] for c in dados_categorias)
    total_gasto = sum(c['gasto'] for c in dados_categorias)
    total_saldo = total_limite - total_gasto
    
    return render_template('index.html',
                         categorias=dados_categorias,
                         total_limite=total_limite,
                         total_gasto=total_gasto,
                         total_saldo=total_saldo)


# ============================================================================
# ROTAS DE CATEGORIA (ORÇAMENTO)
# ============================================================================

@categoria_bp.route('/')
def listar_categorias():
    """Listar todas as categorias."""
    categorias = Categoria.query.all()
    return render_template('categorias.html', categorias=format_categorias(categorias))


@categoria_bp.route('/nova', methods=['GET', 'POST'])
@handle_service_errors('categoria.nova_categoria')
def nova_categoria():
    """Criar nova categoria."""
    form = CategoryForm()
    if form.validate_on_submit():
        create_category(form.nome.data.strip(), float(form.limite.data))
        flash_success(f'Categoria "{form.nome.data}" criada com sucesso!')
        return redirect(url_for('categoria.listar_categorias'))
    return render_template('nova_categoria.html', form=form)


@categoria_bp.route('/editar/<int:id>', methods=['GET', 'POST'])
@handle_service_errors('categoria.editar_categoria')
def editar_categoria(id):
    """Editar categoria existente."""
    categoria = Categoria.query.get_or_404(id)
    form = CategoryForm(original_id=id, obj=categoria)
    
    if form.validate_on_submit():
        update_category(id, form.nome.data.strip(), float(form.limite.data))
        flash_success(f'Categoria "{form.nome.data}" atualizada com sucesso!')
        return redirect(url_for('categoria.listar_categorias'))
    
    return render_template('editar_categoria.html', categoria=categoria, form=form)


@categoria_bp.route('/deletar/<int:id>', methods=['POST'])
@handle_service_errors('categoria.listar_categorias')
def deletar_categoria(id):
    """Deletar categoria."""
    categoria = Categoria.query.get_or_404(id)
    delete_category(id)
    flash_success(f'Categoria "{categoria.nome}" deletada com sucesso!')
    return redirect(url_for('categoria.listar_categorias'))


# ============================================================================
# ROTAS DE TRANSAÇÃO (DESPESA)
# ============================================================================

@transacao_bp.route('/')
def listar_transacoes():
    """Listar todas as transações."""
    transacoes = Transacao.query.order_by(Transacao.criado_em.desc()).all()
    return render_template('transacoes.html', transacoes=format_transacoes(transacoes))


@transacao_bp.route('/nova', methods=['GET', 'POST'])
@handle_service_errors('transacao.nova_transacao')
def nova_transacao():
    """Criar nova transação."""
    categorias = Categoria.query.all()
    form = TransactionForm()
    form.categoria_id.choices = [(c.id, c.nome) for c in categorias]

    if form.validate_on_submit():
        create_transaction(form.descricao.data.strip(), float(form.valor.data), form.categoria_id.data)
        flash_success(f'Transação "{form.descricao.data}" adicionada com sucesso!')
        return redirect(url_for('transacao.listar_transacoes'))

    return render_template('nova_transacao.html', categorias=categorias, form=form)


@transacao_bp.route('/editar/<int:id>', methods=['GET', 'POST'])
@handle_service_errors('transacao.editar_transacao')
def editar_transacao(id):
    """Editar transação existente."""
    transacao = Transacao.query.get_or_404(id)
    categorias = Categoria.query.all()
    form = TransactionForm(obj=transacao)
    form.categoria_id.choices = [(c.id, c.nome) for c in categorias]
    
    if request.method == 'GET':
        form.categoria_id.data = transacao.categoria_id

    if form.validate_on_submit():
        update_transaction(id, form.descricao.data.strip(), float(form.valor.data), form.categoria_id.data)
        flash_success(f'Transação "{form.descricao.data}" atualizada com sucesso!')
        return redirect(url_for('transacao.listar_transacoes'))

    return render_template('editar_transacao.html', transacao=transacao, categorias=categorias, form=form)


@transacao_bp.route('/deletar/<int:id>', methods=['POST'])
@handle_service_errors('transacao.listar_transacoes')
def deletar_transacao(id):
    """Deletar transação."""
    transacao = Transacao.query.get_or_404(id)
    delete_transaction(id)
    flash_success(f'Transação "{transacao.descricao}" deletada com sucesso!')
    return redirect(url_for('transacao.listar_transacoes'))
