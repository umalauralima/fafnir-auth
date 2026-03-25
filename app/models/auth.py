import uuid
from datetime import datetime, timezone
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
        db.DateTime(timezone=True),
        default=datetime.now(timezone.utc),
        nullable=False
    )

    last_login_at = db.Column(
        db.DateTime(timezone=True),
        nullable=True
    )

    __table_args__ = (
        db.UniqueConstraint('email', name='uq_auth_email'),
    )

    refresh_tokens = db.relationship(
        "RefreshToken",
        back_populates="auth",
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Auth {self.email}>"