import os
from dotenv import load_dotenv

load_dotenv()

# Caminho base do projeto
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    """Configurações base"""
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-key-change-in-production')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SESSION_COOKIE_SECURE = os.getenv('SESSION_COOKIE_SECURE', 'False') == 'True'
    SESSION_COOKIE_HTTPONLY = os.getenv('SESSION_COOKIE_HTTPONLY', 'True') == 'True'
    
    # Database URL com fallback para SQLite
    database_url = os.getenv('DATABASE_URL')
    if database_url:
        # Produção: MySQL/PostgreSQL
        SQLALCHEMY_DATABASE_URI = database_url
    else:
        # Fallback: SQLite com caminho ABSOLUTO
        db_path = os.path.join(basedir, 'instance', 'orcamento.db')
        SQLALCHEMY_DATABASE_URI = f'sqlite:///{db_path}'

class DevelopmentConfig(Config):
    """Desenvolvimento"""
    DEBUG = True
    # Desenvolvimento também usa caminho absoluto
    db_path = os.path.join(basedir, 'instance', 'orcamento.db')
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{db_path}'

class ProductionConfig(Config):
    """Produção"""
    DEBUG = False