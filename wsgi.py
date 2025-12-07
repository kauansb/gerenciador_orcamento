#!/usr/bin/env python3
"""
WSGI entry point for production servers (Gunicorn, Waitress, etc.)
Use with: gunicorn --bind 0.0.0.0:5000 wsgi:app
"""

import os
import sys

# Verificar versão do Python (SQLAlchemy 2.x não suporta Python 3.13+)
if sys.version_info >= (3, 13):
    raise RuntimeError(
        f"Python {sys.version_info.major}.{sys.version_info.minor} não é suportado. "
        f"Este projeto requer Python 3.8 a 3.12. "
        f"Configure o runtime.txt para python-3.12.7"
    )

from app import create_app

# Set production environment variables if not already set
if not os.getenv('FLASK_ENV'):
    os.environ['FLASK_ENV'] = 'production'

app = create_app()

if __name__ == '__main__':
    # This block only runs when executed directly (development)
    app.run()
