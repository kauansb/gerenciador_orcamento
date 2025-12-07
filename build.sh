#!/usr/bin/env bash
# Build script for Render.com deployment

set -o errexit

echo "Python version: $(python --version)"

# Verificar versão do Python
PYTHON_VERSION=$(python -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')
echo "Detected Python version: $PYTHON_VERSION"

if [ "$PYTHON_VERSION" = "3.13" ]; then
    echo "ERROR: Python 3.13 is not supported by SQLAlchemy 2.0.x"
    echo "Please configure Render to use Python 3.12"
    echo "Add 'python-3.12.7' to runtime.txt file"
    exit 1
fi

# Instalar dependências
pip install --upgrade pip
pip install -r requirements.txt

echo "Build completed successfully!"
