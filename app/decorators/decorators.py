from functools import wraps
import traceback
from flask import jsonify
from pydantic import ValidationError

from ..errors.auth_errors import AuthError, AUTH_ERRORS

def handle_auth_errors(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            return fn(*args, **kwargs)

        # erros de negócio
        except AuthError as e:
            return jsonify({
                "error": {
                    "code": e.code,
                    "message": e.message
                }
            }), e.status_code

        # validação (AUTH-010 / AUTH-011)
        except ValidationError as e:
            errors = e.errors()

            missing = []
            invalid = []

            for err in errors:
                field = err["loc"][0]

                if err["type"] == "missing":
                    missing.append(field)
                else:
                    invalid.append({
                        "field": field,
                        "message": err["msg"]
                    })

            if missing:
                code = "AUTH-011"
                message, status = AUTH_ERRORS[code]

                return jsonify({
                    "error": {
                        "code": code,
                        "message": message,
                        "fields": missing
                    }
                }), status

            code = "AUTH-010"
            message, status = AUTH_ERRORS[code]

            return jsonify({
                "error": {
                    "code": code,
                    "message": message,
                    "details": invalid
                }
            }), status

        # fallback (AUTH-012)
        except Exception as e:
            code = "AUTH-012"
            message, status = AUTH_ERRORS[code]
            ## TODO imprimir log
            print(e, traceback.format_exc())
            return jsonify({
                "error": {
                    "code": code,
                    "message": message
                }
            }), status

    return wrapper