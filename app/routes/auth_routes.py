## -*- coding: utf-8 -*-

from datetime import datetime, timezone, timedelta
import uuid
import jwt

from app.decorators.decorators import handle_auth_errors
from app.errors.auth_errors import raise_auth_error
from app.helpers.generate_tokens_login import generate_tokens_login
from app.security import hash_password, verify_password
from ..config import Config
from flask import Blueprint, jsonify, request
from pydantic import ValidationError

from app.dto.auth import CreateUserDTO, LoginDTO, LogoutDTO
from ..services.auth import AuthService

auth_bp = Blueprint("auth", __name__)
service = AuthService()

#TODO Criar o serviço de logs com nivel, em arquivo especifico etc

@auth_bp.route("/login", methods=["POST"])
@handle_auth_errors
def login_user():

    dto = LoginDTO(**request.json)
    user = service.get_user(dto)
    
    if not user:
        raise_auth_error("AUTH-001")

    if not verify_password(dto.password, user.password_hash):
        raise_auth_error("AUTH-002")

    if not user.active:
        raise_auth_error("AUTH-003")
    
    access_token, refresh_token = generate_tokens_login(user)
    
    # Salva o token de sessão no banco
    service.create_refresh_token(user.id, refresh_token)

    ## Login = atualiza a coluna last_login_at do User
    service.login(user.id)

    return jsonify({"access_token": access_token, "refresh_token": refresh_token}), 200

@auth_bp.route("/logout", methods=["POST"])
@handle_auth_errors
def logout():
    
    dto = LogoutDTO(**request.json)
    
    ## Invalida a sessão
    token_in_db = service.revoke_session(dto.refresh_token)
    
    return {"message": "Logout com sucesso"}, 200

@auth_bp.route("/refresh", methods=["POST"])
@handle_auth_errors
def refresh():
    
    dto = LogoutDTO(**request.json)
    
    token_in_db = service.get_session_by_token(dto.refresh_token)

    if not token_in_db or token_in_db.is_revoked:
        raise_auth_error("AUTH-008")
    
    if token_in_db.expires_at.replace(tzinfo=timezone.utc) < datetime.now(timezone.utc):
        raise_auth_error("AUTH-007")

    # Valida JWT
    try:
        payload = jwt.decode(dto.refresh_token, Config.JWT_SECRET_KEY, algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        raise_auth_error("AUTH-701")
    
    # Rotaciona a sessão (revoga o antigo)
    service.revoke_session(dto.refresh_token)

    access_token, new_refresh_token = generate_tokens_login(token_in_db.user)

    # Salva o token de sessão no banco
    service.create_refresh_token(token_in_db.user_id, new_refresh_token)

    return {
        "access_token": access_token,
        "refresh_token": new_refresh_token
    }

#TODO Decorator para apenas DEV ter acesso ao endpoint
@auth_bp.route("/login/create", methods=["POST"])
@handle_auth_errors
def create_user():

    try:
        dto = CreateUserDTO(**request.json)
    except ValidationError as e:
        return jsonify(e.errors()), 400

    user = service.login(dto)
    if user:
        return jsonify({
            "error": {
                "code": "AUTH-013",
                "message": "Usuário já existe"
            }
        }), 409
    else:
        hashed_password = hash_password(dto.password)
        new_user = service.create_default_user(dto, hashed_password)
        return jsonify({
                    "message": "Usuário criado com sucesso",
                }), 201


"""
# Erros de Autenticação (Login)
AUTH-001 → Credenciais inválidas (Usuário não encontrado)
AUTH-002 → Credenciais inválidas (senha incorreta)
AUTH-003 → Usuário inativo
AUTH-004 → Usuário bloqueado
AUTH-005 → Muitas tentativas de login (rate limit)
AUTH-006 → Conta não verificada
# Token / Sessão
AUTH-700 → Token expirado  OK
AUTH-701 → Token Refresh expirado  OK
AUTH-008 → Token inválido  OK
AUTH-009 → Token não fornecido
# Requisição / Payload
AUTH-010 → Dados inválidos
AUTH-011 → Campos obrigatórios ausentes
# Interno
AUTH-012 → Erro interno de autenticação
"""