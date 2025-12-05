from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Categoria(db.Model):
    """Model para Categoria (Orçamento)."""
    __tablename__ = 'categoria'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False, unique=True)
    limite = db.Column(db.Float, nullable=False)
    
    transacoes = db.relationship('Transacao', backref='categoria', cascade='all, delete-orphan')
    
    @property
    def gasto(self):
        """Total gasto em transações desta categoria."""
        return sum(t.valor for t in self.transacoes)
    
    @property
    def saldo(self):
        """Saldo restante do orçamento."""
        return self.limite - self.gasto
    
    @property
    def percentual(self):
        """Percentual de orçamento gasto."""
        if self.limite == 0:
            return 0
        return (self.gasto / self.limite) * 100
    
    @property
    def transacoes_count(self):
        """Número de transações desta categoria."""
        return len(self.transacoes)


class Transacao(db.Model):
    """Model para Transação (Despesa)."""
    __tablename__ = 'transacao'
    
    id = db.Column(db.Integer, primary_key=True)
    descricao = db.Column(db.String(255), nullable=False)
    valor = db.Column(db.Float, nullable=False)
    categoria_id = db.Column(db.Integer, db.ForeignKey('categoria.id'), nullable=False)
