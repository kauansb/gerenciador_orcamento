import os
from dotenv import load_dotenv
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect

# Carregar .env ANTES de tudo
load_dotenv()

# Instâncias globais
db = SQLAlchemy()
csrf = CSRFProtect()

def create_app():
    app = Flask(__name__)
    
    # Importar config DENTRO da função
    from config import Config
    app.config.from_object(Config)
    
    # Inicializar extensões com o app
    db.init_app(app)
    csrf.init_app(app)
    
    # Registrar blueprints DENTRO do contexto do app
    with app.app_context():
        from app.routes import main_bp, categoria_bp, transacao_bp
        app.register_blueprint(main_bp)
        app.register_blueprint(categoria_bp)
        app.register_blueprint(transacao_bp)
        
        # Criar tabelas
        try:
            db.create_all()
            app.logger.info("✓ Banco de dados inicializado")
        except Exception as e:
            app.logger.warning(f"⚠ Aviso ao inicializar banco: {e}")
    
    return app