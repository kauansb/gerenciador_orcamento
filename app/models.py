from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func


db = SQLAlchemy()


class Categoria(db.Model):
    """Model para Categoria (Orçamento)."""
    __tablename__ = 'categoria'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False, unique=True)
    limite = db.Column(db.Float, nullable=False)
    criado_em = db.Column(db.DateTime, nullable=False, default=func.now())
    atualizado_em = db.Column(db.DateTime, nullable=False, default=func.now(), onupdate=func.now())
    
    transacoes = db.relationship('Transacao', backref='categoria', lazy='dynamic', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Categoria {self.nome}>'
    
    def obter_total_gasto(self):
        """Calcula o total gasto em transações desta categoria (via SQL)."""
        total = db.session.query(func.sum(Transacao.valor)).filter_by(categoria_id=self.id).scalar()
        return float(total) if total else 0.0
    
    def obter_saldo_restante(self):
        """Calcula o saldo restante do orçamento"""
        return self.limite - self.obter_total_gasto()
    
    def obter_percentual_gasto(self):
        """Calcula o percentual de orçamento gasto"""
        if self.limite == 0:
            return 0
        return (self.obter_total_gasto() / self.limite) * 100


class Transacao(db.Model):
    """Model para Transação (Despesa)."""
    __tablename__ = 'transacao'
    
    id = db.Column(db.Integer, primary_key=True)
    descricao = db.Column(db.String(255), nullable=False)
    valor = db.Column(db.Float, nullable=False)
    categoria_id = db.Column(db.Integer, db.ForeignKey('categoria.id'), nullable=False)
    criado_em = db.Column(db.DateTime, nullable=False, default=func.now())
    atualizado_em = db.Column(db.DateTime, nullable=False, default=func.now(), onupdate=func.now())
    
    def __repr__(self):
        return f'<Transacao {self.descricao} - R$ {self.valor}>'
