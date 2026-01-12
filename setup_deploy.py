#!/usr/bin/env python3
"""
Setup para Deploy - Gera SECRET_KEY segura
Suporta: PostgreSQL (Render), MySQL (Hostinger VPS), SQLite (dev)
Uso: python setup_deploy.py
"""

import secrets
from pathlib import Path


def create_env_file():
    """Cria arquivo .env com SECRET_KEY segura"""
    env_file = Path('.env')
    
    if env_file.exists():
        print("✓ Arquivo .env já existe")
        return
    
    secret_key = secrets.token_urlsafe(32)
    env_file.write_text(f"SECRET_KEY={secret_key}\n")
    
    print("✓ Arquivo .env criado com sucesso!")
    print(f"  SECRET_KEY: {secret_key[:20]}...")


def main():
    print("\n🚀 Setup para Deploy - Gerenciador de Orçamento\n")
    create_env_file()
    print("\n✓ Setup completo! Próximos passos:\n")
    print("  📋 Para MySQL (Hostinger VPS):\n")
    print("     1. Defina DATABASE_URL no .env ou na VPS:")
    print("        DATABASE_URL=mysql+pymysql://user:password@host:3306/database_name\n")
    print("     2. SSH na VPS e instale dependências:")
    print("        pip install -r requirements.txt\n")
    print("     3. Inicie o gunicorn:")
    print("        gunicorn --bind 0.0.0.0:5000 --workers 2 wsgi:app\n")
    print("  📋 Para PostgreSQL (Render.com):\n")
    print("     1. A DATABASE_URL é fornecida automaticamente\n")
    print("     2. Deploy via GitHub: git push\n")
    print("  📋 Desenvolvimento (SQLite):\n")
    print("     1. Executar localmente: flask run\n")


if __name__ == '__main__':
    main()

