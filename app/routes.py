from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models import Categoria, Transacao
from app.forms import CategoryForm, TransactionForm
from app.services import BusinessRuleError, NotFoundError
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
    """
    Dashboard principal mostrando resumo de todas as categorias.
    Exibe: limite, gasto, saldo e percentual para cada categoria.
    """
    categorias = Categoria.query.all()
    
    # Calcular totais gerais
    total_limite = sum(c.limite for c in categorias)
    total_gasto = sum(c.obter_total_gasto() for c in categorias)
    total_saldo = total_limite - total_gasto
    
    dados_categorias = []
    for categoria in categorias:
        dados_categorias.append({
            'id': categoria.id,
            'nome': categoria.nome,
            'limite': categoria.limite,
            'gasto': categoria.obter_total_gasto(),
            'saldo': categoria.obter_saldo_restante(),
            'percentual': categoria.obter_percentual_gasto(),
            'transacoes_count': categoria.transacoes.count()
        })
    
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
    """
    READ: Listar todas as categorias com agregação de transações.
    Mostra: nome, limite, total gasto, saldo restante e percentual.
    """
    categorias = Categoria.query.all()
    
    dados_categorias = []
    for categoria in categorias:
        dados_categorias.append({
            'id': categoria.id,
            'nome': categoria.nome,
            'limite': categoria.limite,
            'gasto': categoria.obter_total_gasto(),
            'saldo': categoria.obter_saldo_restante(),
            'percentual': categoria.obter_percentual_gasto(),
            'transacoes_count': categoria.transacoes.count()
        })
    
    return render_template('categorias.html', categorias=dados_categorias)


@categoria_bp.route('/nova', methods=['GET', 'POST'])
def nova_categoria():
    """
    CREATE: Formulário para adicionar nova categoria com limite orçamentário.
    """
    form = CategoryForm()
    if form.validate_on_submit():
        nome = form.nome.data.strip()
        limite = float(form.limite.data)
        try:
            create_category(nome, limite)
            flash(f'Categoria "{nome}" criada com sucesso!', 'success')
            return redirect(url_for('categoria.listar_categorias'))
        except BusinessRuleError as e:
            flash(str(e), 'error')
            return redirect(url_for('categoria.nova_categoria'))
        except Exception as e:
            flash(f'Erro ao criar categoria: {str(e)}', 'error')
            return redirect(url_for('categoria.nova_categoria'))

    return render_template('nova_categoria.html', form=form)


@categoria_bp.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar_categoria(id):
    """
    UPDATE: Formulário para modificar nome ou limite de categoria existente.
    """
    categoria = Categoria.query.get_or_404(id)
    
    form = CategoryForm(original_id=id, obj=categoria)
    if form.validate_on_submit():
        nome = form.nome.data.strip()
        limite = float(form.limite.data)
        try:
            update_category(id, nome, limite)
            flash(f'Categoria "{nome}" atualizada com sucesso!', 'success')
            return redirect(url_for('categoria.listar_categorias'))
        except BusinessRuleError as e:
            flash(str(e), 'error')
            return redirect(url_for('categoria.editar_categoria', id=id))
        except NotFoundError as e:
            flash(str(e), 'error')
            return redirect(url_for('categoria.listar_categorias'))
        except Exception as e:
            flash(f'Erro ao atualizar categoria: {str(e)}', 'error')
            return redirect(url_for('categoria.editar_categoria', id=id))

    return render_template('editar_categoria.html', categoria=categoria, form=form)


@categoria_bp.route('/deletar/<int:id>', methods=['POST'])
def deletar_categoria(id):
    """
    DELETE: Remover categoria.
    Inclui validação para garantir que não existem transações relacionadas,
    ou deleta-as em cascata (configurado no model com cascade='all, delete-orphan').
    """
    categoria = Categoria.query.get_or_404(id)
    nome = categoria.nome
    
    try:
        delete_category(id)
        flash(f'Categoria "{nome}" deletada com sucesso!', 'success')
    except NotFoundError as e:
        flash(str(e), 'error')
    except Exception as e:
        flash(f'Erro ao deletar categoria: {str(e)}', 'error')

    return redirect(url_for('categoria.listar_categorias'))


# ============================================================================
# ROTAS DE TRANSAÇÃO (DESPESA)
# ============================================================================

@transacao_bp.route('/')
def listar_transacoes():
    """
    READ: Listar todas as transações com nome da categoria.
    Usa a relação definida no model para acessar dados da categoria.
    """
    transacoes = Transacao.query.order_by(Transacao.criado_em.desc()).all()
    
    dados_transacoes = []
    for transacao in transacoes:
        dados_transacoes.append({
            'id': transacao.id,
            'descricao': transacao.descricao,
            'valor': transacao.valor,
            'categoria_nome': transacao.categoria.nome,
            'categoria_id': transacao.categoria_id,
            'criado_em': transacao.criado_em.strftime('%d/%m/%Y %H:%M:%S'),
            'atualizado_em': transacao.atualizado_em.strftime('%d/%m/%Y %H:%M:%S')
        })
    
    return render_template('transacoes.html', transacoes=dados_transacoes)


@transacao_bp.route('/nova', methods=['GET', 'POST'])
def nova_transacao():
    """
    CREATE: Formulário para adicionar nova transação.
    
    Lógica de Validação Crucial:
    - Calcula saldo restante da categoria (limite - soma_das_transacoes_existentes)
    - Se nova transação exceder o limite, exibe erro e não salva no BD
    - Dropdown é populado dinamicamente com categorias do BD
    """
    categorias = Categoria.query.all()
    form = TransactionForm()
    form.categoria_id.choices = [(c.id, c.nome) for c in categorias]

    if form.validate_on_submit():
        descricao = form.descricao.data.strip()
        valor = float(form.valor.data)
        categoria_id = form.categoria_id.data
        try:
            create_transaction(descricao, valor, categoria_id)
            flash(f'Transação "{descricao}" adicionada com sucesso!', 'success')
            return redirect(url_for('transacao.listar_transacoes'))
        except BusinessRuleError as e:
            flash(str(e), 'error')
            return redirect(url_for('transacao.nova_transacao'))
        except NotFoundError as e:
            flash(str(e), 'error')
            return redirect(url_for('transacao.nova_transacao'))
        except Exception as e:
            flash(f'Erro ao criar transação: {str(e)}', 'error')
            return redirect(url_for('transacao.nova_transacao'))

    return render_template('nova_transacao.html', categorias=categorias, form=form)


@transacao_bp.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar_transacao(id):
    """
    UPDATE: Permitir alteração de descrição, valor e categoria.
    Lógica de validação é aplicada novamente.
    """
    transacao = Transacao.query.get_or_404(id)
    categorias = Categoria.query.all()
    form = TransactionForm(obj=transacao)
    form.categoria_id.choices = [(c.id, c.nome) for c in categorias]
    if request.method == 'GET':
        form.categoria_id.data = transacao.categoria_id

    if form.validate_on_submit():
        descricao = form.descricao.data.strip()
        valor = float(form.valor.data)
        categoria_id = form.categoria_id.data
        try:
            update_transaction(id, descricao, valor, categoria_id)
            flash(f'Transação "{descricao}" atualizada com sucesso!', 'success')
            return redirect(url_for('transacao.listar_transacoes'))
        except BusinessRuleError as e:
            flash(str(e), 'error')
            return redirect(url_for('transacao.editar_transacao', id=id))
        except NotFoundError as e:
            flash(str(e), 'error')
            return redirect(url_for('transacao.listar_transacoes'))
        except Exception as e:
            flash(f'Erro ao atualizar transação: {str(e)}', 'error')
            return redirect(url_for('transacao.editar_transacao', id=id))

    return render_template('editar_transacao.html', transacao=transacao, categorias=categorias, form=form)


@transacao_bp.route('/deletar/<int:id>', methods=['POST'])
def deletar_transacao(id):
    """
    DELETE: Remover transação.
    """
    transacao = Transacao.query.get_or_404(id)
    descricao = transacao.descricao
    
    try:
        delete_transaction(id)
        flash(f'Transação "{descricao}" deletada com sucesso!', 'success')
    except NotFoundError as e:
        flash(str(e), 'error')
    except Exception as e:
        flash(f'Erro ao deletar transação: {str(e)}', 'error')

    return redirect(url_for('transacao.listar_transacoes'))
