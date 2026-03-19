from ..repositories.auth import AuthRepository

class AuthService:

    def __init__(self):
        self.repo = AuthRepository()

    def login(self, dto):

        return self.repo.get_by_uuid(dto.uuid)

    def logout(self, dto):

        return self.repo.logout(dto.uuid)