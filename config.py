import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Flask Configuration
DEBUG = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')

# Database Configuration
database_url = os.getenv('DATABASE_URL')

if database_url:
    # Produção: PostgreSQL, MySQL ou outro banco via DATABASE_URL
    if database_url.startswith('postgres://'):
        database_url = database_url.replace('postgres://', 'postgresql://', 1)
    # MySQL da Hostinger: mysql+pymysql://user:password@host:port/database
    SQLALCHEMY_DATABASE_URI = database_url
else:
    # Desenvolvimento: SQLite
    instance_path = os.path.join(BASE_DIR, 'instance')
    # Criar pasta instance/ se não existir
    os.makedirs(instance_path, exist_ok=True)
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(instance_path, 'orcamento.db')

SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_ENGINE_OPTIONS = {
    'pool_pre_ping': True,  # Verifica conexão antes de usar
    'pool_recycle': 300,    # Recicla conexões a cada 5 minutos
}
