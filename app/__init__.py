from flask import Flask
from flask_wtf import CSRFProtect
import config


def create_app():
    """Criar e configurar a aplicação Flask."""
    app = Flask(__name__, static_folder='static', static_url_path='/static')
    app.config.from_object(config)
    
    # Banco de dados
    from app.models import db
    db.init_app(app)
    
    # CSRF Protection
    CSRFProtect(app)
    
    # Blueprints
    from app.routes import main_bp, categoria_bp, transacao_bp
    app.register_blueprint(main_bp)
    app.register_blueprint(categoria_bp)
    app.register_blueprint(transacao_bp)
    
    # Criar tabelas
    with app.app_context():
        db.create_all()
    
    return app
