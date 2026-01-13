from app import db
from datetime import datetime

class Categoria(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), nullable=False)
    limite = db.Column(db.Float, default=0.0)
    transacoes = db.relationship('Transacao', backref='categoria', lazy=True, cascade='all, delete-orphan')

    @property
    def gasto(self):
        return sum(t.valor for t in self.transacoes)

    @property
    def saldo(self):
        return self.limite - self.gasto
    
    @property
    def percentual(self):
        if self.limite == 0: return 0
        return (self.gasto / self.limite) * 100

    @property
    def transacoes_count(self):
        """Número de transações na categoria."""
        return len(self.transacoes)

class Transacao(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    descricao = db.Column(db.String(100), nullable=False)
    valor = db.Column(db.Float, nullable=False)
    data = db.Column(db.DateTime, default=datetime.utcnow)
    categoria_id = db.Column(db.Integer, db.ForeignKey('categoria.id'), nullable=False)