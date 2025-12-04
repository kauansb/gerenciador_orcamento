from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Categoria(db.Model):
    """Model para Categoria (Orçamento)."""
    __tablename__ = 'categoria'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False, unique=True)
    limite = db.Column(db.Float, nullable=False)
    
    transacoes = db.relationship('Transacao', backref='categoria', cascade='all, delete-orphan')
    
    def total_gasto(self):
        """Calcula o total gasto em transações desta categoria."""
        return sum(t.valor for t in self.transacoes)
    
    def saldo_restante(self):
        """Calcula o saldo restante do orçamento."""
        return self.limite - self.total_gasto()
    
    def percentual_gasto(self):
        """Calcula o percentual de orçamento gasto."""
        if self.limite == 0:
            return 0
        return (self.total_gasto() / self.limite) * 100


class Transacao(db.Model):
    """Model para Transação (Despesa)."""
    __tablename__ = 'transacao'
    
    id = db.Column(db.Integer, primary_key=True)
    descricao = db.Column(db.String(255), nullable=False)
    valor = db.Column(db.Float, nullable=False)
    categoria_id = db.Column(db.Integer, db.ForeignKey('categoria.id'), nullable=False)
