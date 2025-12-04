from app.models import db, Categoria


def criar_categoria(nome, limite):
    """Criar uma nova categoria."""
    categoria = Categoria(nome=nome, limite=limite)
    db.session.add(categoria)
    db.session.commit()
    return categoria


def atualizar_categoria(id, nome, limite):
    """Atualizar uma categoria existente."""
    categoria = Categoria.query.get(id)
    categoria.nome = nome
    categoria.limite = limite
    db.session.commit()
    return categoria


def deletar_categoria(id):
    """Deletar uma categoria."""
    categoria = Categoria.query.get(id)
    db.session.delete(categoria)
    db.session.commit()
