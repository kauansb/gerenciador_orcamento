import os
from dotenv import load_dotenv
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect

load_dotenv()

db = SQLAlchemy()
csrf = CSRFProtect()

def create_app():
    app = Flask(__name__)
    from config import Config
    app.config.from_object(Config)
    
    db.init_app(app)
    csrf.init_app(app)
    
    # Importar models AQUI para o SQLAlchemy reconhecer
    from app import models
    
    # Registrar Blueprints
    from app.routes import main_bp, categoria_bp, transacao_bp
    app.register_blueprint(main_bp)
    app.register_blueprint(categoria_bp)
    app.register_blueprint(transacao_bp)
    
    # Criar tabelas
    with app.app_context():
        try:
            db.create_all()
            app.logger.info("✓ Banco de dados inicializado")
        except Exception as e:
            app.logger.error(f"Erro BD: {e}")
            
    return app