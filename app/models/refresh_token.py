from datetime import datetime, timezone
from app.extensions import db

# Funciona como Identificador de sessão segura
class RefreshToken(db.Model):
    __tablename__ = "refresh_tokens"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    refresh_token_hash = db.Column(db.String(64), unique=True, nullable=False)
    is_revoked = db.Column(db.Boolean, default=False)
    
    expires_at = db.Column(db.DateTime(timezone=True), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), default=datetime.now(timezone.utc))
    
    ip_address = db.Column(db.String(45))

    user_agent = db.Column(db.String(255))

    def __repr__(self):
        return f"<RefreshToken User={self.user_id} revoked={self.is_revoked}>"