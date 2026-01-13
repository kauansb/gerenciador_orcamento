import os
from dotenv import load_dotenv
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect

load_dotenv()

from config import Config

db = SQLAlchemy()
csrf = CSRFProtect()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    db.init_app(app)
    csrf.init_app(app)
    
    # Blueprints
    from app.routes import main_bp, categoria_bp, transacao_bp
    app.register_blueprint(main_bp)
    app.register_blueprint(categoria_bp)
    app.register_blueprint(transacao_bp)
    
    # Criar tabelas apenas se não existirem
    with app.app_context():
        try:
            # Apenas criar, não forçar
            db.create_all()
            if app.config.get('DEBUG'):
                print("✓ Banco de dados inicializado")
        except Exception as e:
            # Log mas não falha a inicialização
            app.logger.warning(f"⚠ Aviso ao inicializar banco: {e}")
    
    return app