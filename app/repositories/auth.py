from ..models.auth import Auth
from ..extensions import db

class AuthRepository:
    def get_by_uuid(self, uuid):
        return Auth.query.get(Auth.uuid == uuid)
    
    def logout(self, uuid):
        return True