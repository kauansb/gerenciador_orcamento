from flask import Blueprint, render_template, redirect, url_for, flash
from app.forms import CategoryForm, TransactionForm, DeleteForm
# Imports diretos de services são seguros
from app.services.categoria_service import criar_categoria, atualizar_categoria, deletar_categoria
from app.services.transacao_service import criar_transacao, atualizar_transacao, deletar_transacao

main_bp = Blueprint('main', __name__)
categoria_bp = Blueprint('categoria', __name__, url_prefix='/categorias')
transacao_bp = Blueprint('transacao', __name__, url_prefix='/transacoes')

@main_bp.route('/')
def index():
    from app.models import Categoria 
    categorias = Categoria.query.all()
    total_limite = sum(c.limite for c in categorias)
    total_gasto = sum(c.gasto for c in categorias)
    total_saldo = sum(c.saldo for c in categorias)
    return render_template('index.html', categorias=categorias, 
                         total_limite=total_limite, total_gasto=total_gasto, total_saldo=total_saldo)

@categoria_bp.route('/')
def listar():
    from app.models import Categoria
    categorias = Categoria.query.all()
    delete_form = DeleteForm()
    return render_template('categorias.html', categorias=categorias, delete_form=delete_form)

@categoria_bp.route('/nova', methods=['GET', 'POST'])
def nova():
    form = CategoryForm()
    if form.validate_on_submit():
        try:
            criar_categoria(form.nome.data, float(form.limite.data))
            flash('Categoria criada!', 'success')
            return redirect(url_for('categoria.listar'))
        except Exception as e:
            flash(f'Erro: {e}', 'error')
    return render_template('nova_categoria.html', form=form)

@categoria_bp.route('/<int:id>/editar', methods=['GET', 'POST'])
def editar(id):
    from app.models import Categoria
    categoria = Categoria.query.get_or_404(id)
    form = CategoryForm(obj=categoria)
    if form.validate_on_submit():
        try:
            atualizar_categoria(id, form.nome.data, float(form.limite.data))
            flash('Atualizado com sucesso!', 'success')
            return redirect(url_for('categoria.listar'))
        except Exception as e:
            flash(f'Erro: {e}', 'error')
    return render_template('editar_categoria.html', form=form, categoria=categoria)

@categoria_bp.route('/<int:id>/deletar', methods=['POST'])
def deletar(id):
    form = DeleteForm()
    if form.validate_on_submit():
        deletar_categoria(id)
        flash('Deletada com sucesso!', 'success')
    return redirect(url_for('categoria.listar'))

@transacao_bp.route('/')
def listar():
    from app.models import Transacao
    transacoes = Transacao.query.order_by(Transacao.data.desc()).all()
    delete_form = DeleteForm()
    return render_template('transacoes.html', transacoes=transacoes, delete_form=delete_form)

@transacao_bp.route('/nova', methods=['GET', 'POST'])
def nova():
    from app.models import Categoria
    form = TransactionForm()
    categorias = Categoria.query.all()
    form.categoria_id.choices = [(c.id, c.nome) for c in categorias]
    if form.validate_on_submit():
        try:
            criar_transacao(form.descricao.data, float(form.valor.data), form.categoria_id.data, form.data.data)
            flash('Transação criada!', 'success')
            return redirect(url_for('transacao.listar'))
        except Exception as e:
            flash(f'Erro: {e}', 'error')
    return render_template('nova_transacao.html', form=form, categorias=categorias)

@transacao_bp.route('/<int:id>/editar', methods=['GET', 'POST'])
def editar(id):
    from app.models import Transacao, Categoria
    transacao = Transacao.query.get_or_404(id)
    form = TransactionForm(obj=transacao)
    categorias = Categoria.query.all()
    form.categoria_id.choices = [(c.id, c.nome) for c in categorias]
    if form.validate_on_submit():
        try:
            atualizar_transacao(id, form.descricao.data, float(form.valor.data), form.categoria_id.data, form.data.data)
            flash('Transação atualizada!', 'success')
            return redirect(url_for('transacao.listar'))
        except Exception as e:
            flash(f'Erro: {e}', 'error')
    return render_template('editar_transacao.html', form=form, transacao=transacao, categorias=categorias)

@transacao_bp.route('/<int:id>/deletar', methods=['POST'])
def deletar(id):
    form = DeleteForm()
    if form.validate_on_submit():
        deletar_transacao(id)
        flash('Deletada!', 'success')
    return redirect(url_for('transacao.listar'))