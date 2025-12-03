from sqlalchemy.exc import IntegrityError as SAIntegrityError
from app.models import db, Categoria
from app.services import BusinessRuleError, NotFoundError


def create_category(nome: str, limite: float) -> Categoria:
    nome = nome.strip()
    if limite <= 0:
        raise BusinessRuleError('Limite deve ser um valor positivo.')

    categoria = Categoria(nome=nome, limite=limite)
    try:
        db.session.add(categoria)
        db.session.commit()
        return categoria
    except SAIntegrityError as e:
        db.session.rollback()
        raise BusinessRuleError('Categoria com esse nome já existe.') from e
    except Exception:
        db.session.rollback()
        raise


def update_category(id: int, nome: str, limite: float) -> Categoria:
    categoria = Categoria.query.get(id)
    if not categoria:
        raise NotFoundError('Categoria não encontrada.')

    nome = nome.strip()
    total_gasto = categoria.obter_total_gasto()
    if limite < total_gasto:
        raise BusinessRuleError(f'Limite não pode ser menor que o total gasto (R$ {total_gasto:.2f}).')

    categoria.nome = nome
    categoria.limite = limite
    try:
        db.session.commit()
        return categoria
    except SAIntegrityError as e:
        db.session.rollback()
        raise BusinessRuleError('Categoria com esse nome já existe.') from e
    except Exception:
        db.session.rollback()
        raise


def delete_category(id: int) -> None:
    categoria = Categoria.query.get(id)
    if not categoria:
        raise NotFoundError('Categoria não encontrada.')

    try:
        db.session.delete(categoria)
        db.session.commit()
    except Exception:
        db.session.rollback()
        raise
