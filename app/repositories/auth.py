from datetime import datetime, timezone
import traceback

from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

from app.models.refresh_token import RefreshToken

from ..models.users import User
from ..extensions import db

class AuthRepository:
    def get_user(self, email):
        stmt = select(User).where(User.email == email)
        return db.session.execute(stmt).scalar_one_or_none()
    
    def get_session_by_token(self, refresh_token):
        stmt = select(RefreshToken).where(RefreshToken.refresh_token_hash == refresh_token)
        return db.session.execute(stmt).scalar_one_or_none()

    def revoke_session(self, refresh_token_hashed):
        try:
            token = RefreshToken.query.filter_by(
                        refresh_token_hash=refresh_token_hashed
                    ).first()

            if not token:
                return False

            token.is_revoked = True

            db.session.commit()
            return True
        except SQLAlchemyError as e:
            db.session.rollback()
            print(traceback.format_exc())
            return False

    def logout(self, uuid):
        return True

    def update_last_login(self, auth_id):
        try:
            rows_updated = User.query.filter_by(id=auth_id).update({
                "last_login_at": datetime.now(timezone.utc)
            })
            db.session.commit()
            return True
        except SQLAlchemyError as e:
            db.session.rollback()
            print(traceback.format_exc())
            return False
    
    def create(self, user):
        
        try:
            db.session.add(user)
            db.session.commit()
            return user

        except Exception as e:

            db.session.rollback()
            raise e