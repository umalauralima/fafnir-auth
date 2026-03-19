import uuid
from datetime import datetime
from ..extensions import db

class Auth(db.Model):
    __tablename__ = 'auth'

    id = db.Column(db.Integer, primary_key=True)

    # UUID público
    uuid = db.Column(
        db.String(36),
        unique=True,
        nullable=False,
        default=lambda: str(uuid.uuid4()),
        index=True
    )

    email = db.Column(db.String(255), unique=True, nullable=False, index=True)

    password_hash = db.Column(db.String(255), nullable=False)

    active = db.Column(db.Boolean, default=True)

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    __table_args__ = (
        db.UniqueConstraint('email', name='uq_auth_email'),
    )

    def __repr__(self):
        return f"<Auth {self.email}>"