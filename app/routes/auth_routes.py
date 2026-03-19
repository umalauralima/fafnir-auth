from flask import Blueprint, jsonify, request
from pydantic import ValidationError

from app.dto.auth import LoginDTO, LogoutDTO
from ..services.auth import AuthService

auth_bp = Blueprint("auth", __name__)
service = AuthService

@auth_bp.route("/login", methods=["POST"])
def login_user():

    try:
        dto = LoginDTO(**request.json)
    except ValidationError as e:
        return jsonify(e.errors()), 400

    user = service.create_user(dto)

    return LoginDTO.model_validate(user).model_dump(), 200

@auth_bp.route("/logout", methods=["POST"])
def logout():
    dto = LogoutDTO(**request.json)
    users = service.logout(dto)
    return {"message": "Logout com sucesso"}, 200