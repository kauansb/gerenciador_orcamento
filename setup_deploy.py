#!/usr/bin/env python3
"""
Setup para Render - Gera SECRET_KEY segura
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
    print("\n🚀 Setup para Render - Gerenciador de Orçamento\n")
    create_env_file()
    print("\n✓ Setup completo! Próximos passos:\n")
    print("  1. Testar localmente: gunicorn wsgi:app")
    print("  2. Fazer commit: git add . && git commit -m 'Deploy ready'")
    print("  3. Push para GitHub: git push")
    print("  4. Conectar no Render (render.com)")
    print("  5. Deploy! 🎉\n")


if __name__ == '__main__':
    main()

