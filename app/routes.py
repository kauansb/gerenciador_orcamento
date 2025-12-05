from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models import Categoria, Transacao
from app.forms import CategoryForm, TransactionForm, DeleteForm
from app.services.categoria_service import criar_categoria, atualizar_categoria, deletar_categoria
from app.services.transacao_service import criar_transacao, atualizar_transacao, deletar_transacao

main_bp = Blueprint('main', __name__)
categoria_bp = Blueprint('categoria', __name__, url_prefix='/categorias')
transacao_bp = Blueprint('transacao', __name__, url_prefix='/transacoes')


# ============================================================================
# DASHBOARD
# ============================================================================

@main_bp.route('/')
def index():
    """Dashboard principal."""
    categorias = Categoria.query.all()
    
    total_limite = sum(c.limite for c in categorias)
    total_gasto = sum(c.gasto for c in categorias)
    total_saldo = total_limite - total_gasto
    
    return render_template('index.html',
                         categorias=categorias,
                         total_limite=total_limite,
                         total_gasto=total_gasto,
                         total_saldo=total_saldo)


# ============================================================================
# CATEGORIAS
# ============================================================================

@categoria_bp.route('/')
def listar():
    """Listar todas as categorias."""
    categorias = Categoria.query.all()
    delete_form = DeleteForm()
    
    return render_template('categorias.html', categorias=categorias, delete_form=delete_form)


@categoria_bp.route('/nova', methods=['GET', 'POST'])
def nova():
    """Criar nova categoria."""
    form = CategoryForm()
    
    if form.validate_on_submit():
        try:
            criar_categoria(form.nome.data, float(form.limite.data))
            flash('Categoria criada com sucesso!', 'success')
            return redirect(url_for('categoria.listar'))
        except Exception as e:
            flash(f'Erro: {str(e)}', 'error')
    
    return render_template('nova_categoria.html', form=form)


@categoria_bp.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
    """Editar categoria."""
    categoria = Categoria.query.get_or_404(id)
    form = CategoryForm()
    
    if form.validate_on_submit():
        try:
            atualizar_categoria(id, form.nome.data, float(form.limite.data))
            flash('Categoria atualizada com sucesso!', 'success')
            return redirect(url_for('categoria.listar'))
        except Exception as e:
            flash(f'Erro: {str(e)}', 'error')
    
    elif request.method == 'GET':
        form.nome.data = categoria.nome
        form.limite.data = categoria.limite
    
    return render_template('editar_categoria.html', categoria=categoria, form=form)


@categoria_bp.route('/deletar/<int:id>', methods=['POST'])
def deletar(id):
    """Deletar categoria."""
    categoria = Categoria.query.get_or_404(id)
    try:
        deletar_categoria(id)
        flash('Categoria deletada com sucesso!', 'success')
    except Exception as e:
        flash(f'Erro: {str(e)}', 'error')
    
    return redirect(url_for('categoria.listar'))


# ============================================================================
# TRANSAÇÕES
# ============================================================================

@transacao_bp.route('/')
def listar():
    """Listar todas as transações."""
    transacoes = Transacao.query.all()
    delete_form = DeleteForm()
    
    return render_template('transacoes.html', transacoes=transacoes, delete_form=delete_form)


@transacao_bp.route('/nova', methods=['GET', 'POST'])
def nova():
    """Criar nova transação."""
    categorias = Categoria.query.all()
    form = TransactionForm()
    form.categoria_id.choices = [(c.id, c.nome) for c in categorias]
    
    if form.validate_on_submit():
        try:
            criar_transacao(form.descricao.data, float(form.valor.data), form.categoria_id.data)
            flash('Transação criada com sucesso!', 'success')
            return redirect(url_for('transacao.listar'))
        except Exception as e:
            flash(f'Erro: {str(e)}', 'error')
    
    return render_template('nova_transacao.html', form=form, categorias=categorias)


@transacao_bp.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
    """Editar transação."""
    transacao = Transacao.query.get_or_404(id)
    categorias = Categoria.query.all()
    form = TransactionForm()
    form.categoria_id.choices = [(c.id, c.nome) for c in categorias]
    
    if form.validate_on_submit():
        try:
            atualizar_transacao(id, form.descricao.data, float(form.valor.data), form.categoria_id.data)
            flash('Transação atualizada com sucesso!', 'success')
            return redirect(url_for('transacao.listar'))
        except Exception as e:
            flash(f'Erro: {str(e)}', 'error')
    
    elif request.method == 'GET':
        form.descricao.data = transacao.descricao
        form.valor.data = transacao.valor
        form.categoria_id.data = transacao.categoria_id
    
    return render_template('editar_transacao.html', transacao=transacao, form=form, categorias=categorias)


@transacao_bp.route('/deletar/<int:id>', methods=['POST'])
def deletar(id):
    """Deletar transação."""
    transacao = Transacao.query.get_or_404(id)
    try:
        deletar_transacao(id)
        flash('Transação deletada com sucesso!', 'success')
    except Exception as e:
        flash(f'Erro: {str(e)}', 'error')
    
    return redirect(url_for('transacao.listar'))
