from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class Categoria(db.Model):
    """
    Model para Categoria (Orçamento).
    
    Relacionamento: Uma Categoria pode ter muitas Transações (One-to-Many).
    """
    __tablename__ = 'categoria'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False, unique=True)
    limite = db.Column(db.Float, nullable=False)
    criado_em = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    atualizado_em = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relacionamento com Transacao (One-to-Many)
    transacoes = db.relationship('Transacao', backref='categoria', lazy='dynamic', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Categoria {self.nome}>'
    
    def obter_total_gasto(self):
        """Calcula o total gasto em transações desta categoria"""
        return sum(t.valor for t in self.transacoes.all()) or 0.0
    
    def obter_saldo_restante(self):
        """Calcula o saldo restante do orçamento"""
        return self.limite - self.obter_total_gasto()
    
    def obter_percentual_gasto(self):
        """Calcula o percentual de orçamento gasto"""
        if self.limite == 0:
            return 0
        return (self.obter_total_gasto() / self.limite) * 100
    
    def validar_transacao(self, valor):
        """
        Valida se uma nova transação pode ser adicionada sem exceder o limite.
        
        Args:
            valor (float): Valor da transação a ser validada
            
        Returns:
            tuple: (bool, str) - (é_válida, mensagem)
        """
        saldo_restante = self.obter_saldo_restante()
        
        if valor > saldo_restante:
            return False, f'Transação de R$ {valor:.2f} excede o saldo restante de R$ {saldo_restante:.2f}'
        
        return True, 'Transação válida'


class Transacao(db.Model):
    """
    Model para Transação (Despesa).
    
    Relacionamento: Uma Transação pertence a apenas uma Categoria (Many-to-One).
    """
    __tablename__ = 'transacao'
    
    id = db.Column(db.Integer, primary_key=True)
    descricao = db.Column(db.String(255), nullable=False)
    valor = db.Column(db.Float, nullable=False)
    categoria_id = db.Column(db.Integer, db.ForeignKey('categoria.id'), nullable=False)
    criado_em = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    atualizado_em = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<Transacao {self.descricao} - R$ {self.valor}>'
    
    def to_dict(self):
        """Converte a transação para um dicionário"""
        return {
            'id': self.id,
            'descricao': self.descricao,
            'valor': self.valor,
            'categoria_id': self.categoria_id,
            'categoria_nome': self.categoria.nome,
            'criado_em': self.criado_em.strftime('%d/%m/%Y %H:%M:%S'),
            'atualizado_em': self.atualizado_em.strftime('%d/%m/%Y %H:%M:%S')
        }
