from flask import Flask
from flask_wtf import CSRFProtect
from config import config
import os


def create_app(config_name=None):
    """
    Factory function para criar e configurar a aplicação Flask.
    
    Args:
        config_name (str): Nome da configuração ('development', 'testing', 'production')
        
    Returns:
        Flask: Instância da aplicação Flask configurada
    """
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'development')
    
    app = Flask(__name__)
    
    # Carregar configuração
    app.config.from_object(config[config_name])
    
    # Criar diretório de instância se não existir
    try:
        os.makedirs(app.instance_path, exist_ok=True)
    except OSError:
        pass
    
    # Inicializar banco de dados
    from app.models import db
    db.init_app(app)

    # Inicializar proteção CSRF (Flask-WTF)
    csrf = CSRFProtect()
    csrf.init_app(app)
    
    # Registrar blueprints
    from app.routes import main_bp, categoria_bp, transacao_bp
    app.register_blueprint(main_bp)
    app.register_blueprint(categoria_bp)
    app.register_blueprint(transacao_bp)
    
    # Criar tabelas do banco de dados
    with app.app_context():
        db.create_all()
    
    return app
