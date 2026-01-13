from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.forms import CategoryForm, TransactionForm, DeleteForm
from app.services.categoria_service import criar_categoria, atualizar_categoria, deletar_categoria
from app.services.transacao_service import criar_transacao, atualizar_transacao, deletar_transacao

main_bp = Blueprint('main', __name__)
categoria_bp = Blueprint('categoria', __name__, url_prefix='/categorias')
transacao_bp = Blueprint('transacao', __name__, url_prefix='/transacoes')

# ========== ROTAS PRINCIPAIS (Dashboard) ==========
@main_bp.route('/')
def index():
    """Dashboard com resumo de todas as categorias"""
    from app.models import Categoria
    
    categorias = Categoria.query.all()
    
    # Calcular totais
    total_limite = sum(c.limite for c in categorias)
    total_gasto = sum(c.gasto for c in categorias)
    total_saldo = sum(c.saldo for c in categorias)
    
    return render_template('index.html',
                         categorias=categorias,
                         total_limite=total_limite,
                         total_gasto=total_gasto,
                         total_saldo=total_saldo)

# ========== ROTAS DE CATEGORIAS ==========
@categoria_bp.route('/')
def listar():
    """Lista todas as categorias"""
    from app.models import Categoria
    categorias = Categoria.query.all()
    return render_template('categorias.html', categorias=categorias)

@categoria_bp.route('/nova', methods=['GET', 'POST'])
def nova():
    """Formulário para criar nova categoria"""
    form = CategoryForm()
    if form.validate_on_submit():
        try:
            criar_categoria(form.nome.data, float(form.limite.data))
            flash('Categoria criada com sucesso!', 'success')
            return redirect(url_for('categoria.listar'))
        except Exception as e:
            flash(f'Erro ao criar categoria: {str(e)}', 'error')
    
    return render_template('nova_categoria.html', form=form)

@categoria_bp.route('/<int:id>/editar', methods=['GET', 'POST'])
def editar(id):
    """Formulário para editar categoria existente"""
    from app.models import Categoria
    categoria = Categoria.query.get_or_404(id)
    form = CategoryForm(obj=categoria)
    
    if form.validate_on_submit():
        try:
            atualizar_categoria(id, form.nome.data, float(form.limite.data))
            flash('Categoria atualizada com sucesso!', 'success')
            return redirect(url_for('categoria.listar'))
        except Exception as e:
            flash(f'Erro ao atualizar categoria: {str(e)}', 'error')
    
    return render_template('editar_categoria.html', form=form, categoria=categoria)

@categoria_bp.route('/<int:id>/deletar', methods=['POST'])
def deletar(id):
    """Deleta uma categoria"""
    form = DeleteForm()
    if form.validate_on_submit():
        try:
            deletar_categoria(id)
            flash('Categoria deletada com sucesso!', 'success')
        except Exception as e:
            flash(f'Erro ao deletar categoria: {str(e)}', 'error')
    
    return redirect(url_for('categoria.listar'))

# ========== ROTAS DE TRANSAÇÕES ==========
@transacao_bp.route('/')
def listar():
    """Lista todas as transações"""
    from app.models import Transacao
    transacoes = Transacao.query.order_by(Transacao.data.desc()).all()
    return render_template('transacoes.html', transacoes=transacoes)

@transacao_bp.route('/nova', methods=['GET', 'POST'])
def nova():
    """Formulário para criar nova transação"""
    from app.models import Categoria
    form = TransactionForm()
    form.categoria_id.choices = [(c.id, c.nome) for c in Categoria.query.all()]
    
    if form.validate_on_submit():
        try:
            criar_transacao(
                form.descricao.data,
                float(form.valor.data),
                form.categoria_id.data,
                form.data.data
            )
            flash('Transação criada com sucesso!', 'success')
            return redirect(url_for('transacao.listar'))
        except Exception as e:
            flash(f'Erro ao criar transação: {str(e)}', 'error')
    
    return render_template('nova_transacao.html', form=form)

@transacao_bp.route('/<int:id>/editar', methods=['GET', 'POST'])
def editar(id):
    """Formulário para editar transação existente"""
    from app.models import Transacao, Categoria
    transacao = Transacao.query.get_or_404(id)
    form = TransactionForm(obj=transacao)
    form.categoria_id.choices = [(c.id, c.nome) for c in Categoria.query.all()]
    
    if form.validate_on_submit():
        try:
            atualizar_transacao(
                id,
                form.descricao.data,
                float(form.valor.data),
                form.categoria_id.data,
                form.data.data
            )
            flash('Transação atualizada com sucesso!', 'success')
            return redirect(url_for('transacao.listar'))
        except Exception as e:
            flash(f'Erro ao atualizar transação: {str(e)}', 'error')
    
    return render_template('editar_transacao.html', form=form, transacao=transacao)

@transacao_bp.route('/<int:id>/deletar', methods=['POST'])
def deletar(id):
    """Deleta uma transação"""
    form = DeleteForm()
    if form.validate_on_submit():
        try:
            deletar_transacao(id)
            flash('Transação deletada com sucesso!', 'success')
        except Exception as e:
            flash(f'Erro ao deletar transação: {str(e)}', 'error')
    
    return redirect(url_for('transacao.listar'))