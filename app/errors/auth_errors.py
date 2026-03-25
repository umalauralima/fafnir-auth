from .base import AppError

class AuthError(AppError):
    pass


AUTH_ERRORS = {
    "AUTH-001": ("Credenciais inválidas", 401),
    "AUTH-002": ("Credenciais inválidas", 401),
    "AUTH-003": ("Credenciais inválidas", 403),
    "AUTH-004": ("Usuário bloqueado", 403),
    "AUTH-005": ("Muitas tentativas. Tente novamente mais tarde", 429),
    "AUTH-006": ("Conta não verificada", 403),
    "AUTH-700": ("Sessão expirada", 401),
    "AUTH-701": ("Sessão expirada", 401),
    "AUTH-008": ("Token inválido", 401),
    "AUTH-009": ("Token não fornecido", 401),
    "AUTH-010": ("Dados de entrada inválidos", 400),
    "AUTH-011": ("Campos obrigatórios não informados", 400),
    "AUTH-012": ("Erro interno", 500),
}


def raise_auth_error(code):
    message, status = AUTH_ERRORS[code]
    raise AuthError(code, message, status)