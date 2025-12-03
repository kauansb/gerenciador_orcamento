"""
Decoradores para simplificar tratamento de erros e validações nas rotas.
"""
from functools import wraps
from flask import redirect, url_for, flash


def handle_service_errors(redirect_endpoint):
    """
    Decorator para capturar erros de serviço e exibir mensagens amigáveis.
    
    Args:
        redirect_endpoint: Rota para redirecionar em caso de erro
        
    Exemplo:
        @handle_service_errors('categoria.nova_categoria')
        def nova_categoria():
            # Qualquer erro de serviço é automaticamente tratado
            pass
    """
    def decorator(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            try:
                return f(*args, **kwargs)
            except Exception as e:
                # Importa aqui para evitar circular imports
                from app.services import BusinessRuleError, NotFoundError
                
                if isinstance(e, (BusinessRuleError, NotFoundError)):
                    flash(str(e), 'error')
                else:
                    flash(f'Erro: {str(e)}', 'error')
                
                return redirect(url_for(redirect_endpoint))
        return wrapped
    return decorator


def flash_success(message, category='success'):
    """Helper para exibir mensagem de sucesso."""
    flash(message, category)


def flash_error(message, category='error'):
    """Helper para exibir mensagem de erro."""
    flash(message, category)
