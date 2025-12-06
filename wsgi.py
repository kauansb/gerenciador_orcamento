#!/usr/bin/env python3
"""
WSGI entry point for production servers (Gunicorn, Waitress, etc.)
Use with: gunicorn --bind 0.0.0.0:5000 wsgi:app
"""

import os
from app import create_app

# Set production environment variables if not already set
if not os.getenv('FLASK_ENV'):
    os.environ['FLASK_ENV'] = 'production'

app = create_app()

if __name__ == '__main__':
    # This block only runs when executed directly (development)
    app.run()
