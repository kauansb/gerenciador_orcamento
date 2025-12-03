from sqlalchemy.exc import IntegrityError as SAIntegrityError
from app.models import db, Categoria, Transacao
from app.services import BusinessRuleError, NotFoundError


def create_transaction(descricao: str, valor: float, categoria_id: int) -> Transacao:
    descricao = descricao.strip()
    if valor <= 0:
        raise BusinessRuleError('Valor deve ser positivo.')

    categoria = Categoria.query.get(categoria_id)
    if not categoria:
        raise NotFoundError('Categoria não encontrada.')

    saldo_restante = categoria.obter_saldo_restante()
    if valor > saldo_restante:
        raise BusinessRuleError(f'Transação de R$ {valor:.2f} excede o saldo restante de R$ {saldo_restante:.2f}')

    transacao = Transacao(descricao=descricao, valor=valor, categoria_id=categoria_id)
    try:
        db.session.add(transacao)
        db.session.commit()
        return transacao
    except SAIntegrityError as e:
        db.session.rollback()
        raise BusinessRuleError('Erro de integridade ao criar transação.') from e
    except Exception:
        db.session.rollback()
        raise


def update_transaction(id: int, descricao: str, valor: float, categoria_id: int) -> Transacao:
    transacao = Transacao.query.get(id)
    if not transacao:
        raise NotFoundError('Transação não encontrada.')

    descricao = descricao.strip()
    if valor <= 0:
        raise BusinessRuleError('Valor deve ser positivo.')

    categoria_nova = Categoria.query.get(categoria_id)
    if not categoria_nova:
        raise NotFoundError('Categoria não encontrada.')

    # calcular gasto novo considerando remoção do valor atual se permanecer na mesma categoria
    total_gasto_novo = categoria_nova.obter_total_gasto()
    if categoria_nova.id == transacao.categoria_id:
        total_gasto_novo -= transacao.valor

    if total_gasto_novo + valor > categoria_nova.limite:
        saldo_restante = categoria_nova.limite - total_gasto_novo
        raise BusinessRuleError(f'Transação de R$ {valor:.2f} excede o saldo restante de R$ {saldo_restante:.2f}')

    transacao.descricao = descricao
    transacao.valor = valor
    transacao.categoria_id = categoria_id

    try:
        db.session.commit()
        return transacao
    except SAIntegrityError as e:
        db.session.rollback()
        raise BusinessRuleError('Erro de integridade ao atualizar transação.') from e
    except Exception:
        db.session.rollback()
        raise


def delete_transaction(id: int) -> None:
    transacao = Transacao.query.get(id)
    if not transacao:
        raise NotFoundError('Transação não encontrada.')

    try:
        db.session.delete(transacao)
        db.session.commit()
    except Exception:
        db.session.rollback()
        raise
