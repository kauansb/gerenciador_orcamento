from app.models import db, Transacao


def criar_transacao(descricao, valor, categoria_id):
    """Criar uma nova transação."""
    transacao = Transacao(descricao=descricao, valor=valor, categoria_id=categoria_id)
    db.session.add(transacao)
    db.session.commit()
    return transacao


def atualizar_transacao(id, descricao, valor, categoria_id):
    """Atualizar uma transação existente."""
    transacao = Transacao.query.get(id)
    transacao.descricao = descricao
    transacao.valor = valor
    transacao.categoria_id = categoria_id
    db.session.commit()
    return transacao


def deletar_transacao(id):
    """Deletar uma transação."""
    transacao = Transacao.query.get(id)
    db.session.delete(transacao)
    db.session.commit()
