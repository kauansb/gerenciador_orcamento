import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Configurações base"""
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-key-change-in-production')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SESSION_COOKIE_SECURE = os.getenv('SESSION_COOKIE_SECURE', 'False') == 'True'
    SESSION_COOKIE_HTTPONLY = os.getenv('SESSION_COOKIE_HTTPONLY', 'True') == 'True'
    
    # Database URL com fallback para SQLite desenvolvimento
    database_url = os.getenv('DATABASE_URL')
    if database_url:
        # Produção: MySQL/PostgreSQL
        SQLALCHEMY_DATABASE_URI = database_url
    else:
        # Desenvolvimento: SQLite
        SQLALCHEMY_DATABASE_URI = 'sqlite:///instance/orcamento.db'

class DevelopmentConfig(Config):
    """Desenvolvimento"""
    FLASK_DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///instance/orcamento.db'

class ProductionConfig(Config):
    """Produção"""
    FLASK_DEBUG = False