import os

class Config:
    """Configuração base da aplicação Flask"""
    
    # Diretório base da aplicação
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    
    # Configuração do banco de dados SQLite
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'instance', 'orcamento.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Chave secreta para sessões e CSRF
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'


class DevelopmentConfig(Config):
    """Configuração para desenvolvimento"""
    DEBUG = True
    TESTING = False
    # Durante desenvolvimento, desative o cache de arquivos estáticos
    # e force recarregamento de templates para facilitar testes
    SEND_FILE_MAX_AGE_DEFAULT = 0
    TEMPLATES_AUTO_RELOAD = True


class TestingConfig(Config):
    """Configuração para testes"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'


class ProductionConfig(Config):
    """Configuração para produção"""
    DEBUG = False
    TESTING = False


# Seleção de configuração baseada no ambiente
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
