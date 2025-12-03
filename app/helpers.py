"""
Helpers para formatar dados de modelos para templates.
"""
from app.models import Categoria, Transacao


def format_categoria(categoria: Categoria) -> dict:
    """Formata dados de categoria para template."""
    return {
        'id': categoria.id,
        'nome': categoria.nome,
        'limite': categoria.limite,
        'gasto': categoria.obter_total_gasto(),
        'saldo': categoria.obter_saldo_restante(),
        'percentual': categoria.obter_percentual_gasto(),
        'transacoes_count': categoria.transacoes.count()
    }


def format_categorias(categorias: list) -> list:
    """Formata lista de categorias para template."""
    return [format_categoria(c) for c in categorias]


def format_transacao(transacao: Transacao) -> dict:
    """Formata dados de transação para template."""
    return {
        'id': transacao.id,
        'descricao': transacao.descricao,
        'valor': transacao.valor,
        'categoria_nome': transacao.categoria.nome,
        'categoria_id': transacao.categoria_id,
        'criado_em': transacao.criado_em.strftime('%d/%m/%Y %H:%M:%S'),
        'atualizado_em': transacao.atualizado_em.strftime('%d/%m/%Y %H:%M:%S')
    }


def format_transacoes(transacoes: list) -> list:
    """Formata lista de transações para template."""
    return [format_transacao(t) for t in transacoes]
