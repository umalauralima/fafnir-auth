from datetime import datetime, timezone, timedelta
from ..config import Config
import uuid
import jwt

def generate_tokens_login(auth):
    ## Gerando o código de acesso curto
    payload = {
        "sub": str(auth.uuid),
        "roles": None,
        "permissions": None,
        "exp": datetime.now(timezone.utc) + timedelta(seconds=int(Config.JWT_EXPIRATION_SECONDS))
    }
    access_token = jwt.encode(payload, Config.JWT_SECRET_KEY, algorithm="HS256")

    # Gerando o token de identificação de sessão segura
    refresh_payload = {
        "sub": str(auth.uuid),
        "jti": str(uuid.uuid4()),
        "exp": datetime.now(timezone.utc) + timedelta(days=int(Config.JWT_REFRESH_TOKEN_DAYS)),
    }
    refresh_token = jwt.encode(refresh_payload, Config.JWT_SECRET_KEY, algorithm="HS256")
    
    return access_token, refresh_token