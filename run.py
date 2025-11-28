#!/usr/bin/env python3
"""
Script para executar a aplicação Flask.

Uso:
    python run.py              # Modo desenvolvimento
    FLASK_ENV=production python run.py  # Modo produção
"""

import os
from app import create_app

if __name__ == '__main__':
    # Criar aplicação
    app = create_app()
    
    # Configurar host e porta
    host = os.environ.get('FLASK_HOST', '0.0.0.0')
    port = int(os.environ.get('FLASK_PORT', 5000))
    debug = os.environ.get('FLASK_ENV') != 'production'
    
    # Executar servidor
    app.run(host=host, port=port, debug=debug)
