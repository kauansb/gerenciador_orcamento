import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Flask Configuration
DEBUG = False
SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')

# Database Configuration
SQLALCHEMY_DATABASE_URI = os.getenv(
    'DATABASE_URL', 
    'sqlite:///' + os.path.join(BASE_DIR, 'instance', 'orcamento.db')
)
SQLALCHEMY_TRACK_MODIFICATIONS = False
