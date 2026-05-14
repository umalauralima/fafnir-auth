from datetime import datetime, timedelta, timezone
import hashlib
import uuid
from ..config import Config 
from app.models.users import User
from app.models.refresh_token import RefreshToken

from ..repositories.auth import AuthRepository

class AuthService:

    def __init__(self):
        self.repo = AuthRepository()

    def get_user(self, dto):
        user = self.repo.get_user(dto.email)
        return user

    def get_session_by_token(self, refresh_token):
        incoming_token_hashed = hashlib.sha256(refresh_token.encode()).hexdigest()
        token = self.repo.get_session_by_token(incoming_token_hashed)
        return token

    def revoke_session(self, refresh_token):
        incoming_token_hashed = hashlib.sha256(refresh_token.encode()).hexdigest()
        token = self.repo.revoke_session(incoming_token_hashed)
        return token

    def login(self, user_id):
        return self.repo.update_last_login(user_id)

    def logout(self, dto):

        return self.repo.logout(dto.uuid)
    
    def create_default_user(self, dto, hashed_password):

        user_uuid = str(uuid.uuid4())
        
        user = User(
            uuid=user_uuid,
            email=dto.email,
            password_hash=hashed_password,
        )
        
        return self.repo.create(user)
    
    #TODO Guardar o contexto da sessão: ip, user-agent
    def create_refresh_token(self, user_id, refresh_token):
        token_hashed = hashlib.sha256(refresh_token.encode()).hexdigest()

        token_db = RefreshToken(
            auth_id=user_id,
            refresh_token_hash=token_hashed,
            expires_at=datetime.now(timezone.utc) + timedelta(days=int(Config.JWT_REFRESH_TOKEN_DAYS)),
        )

        return self.repo.create(token_db)
    
