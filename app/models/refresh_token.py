from datetime import datetime, timezone
from app.extensions import db

# Funciona como Identificador de sessão segura
class RefreshToken(db.Model):
    __tablename__ = "refresh_tokens"

    id = db.Column(db.Integer, primary_key=True)

    auth_id = db.Column(
        db.Integer,
        db.ForeignKey("auth.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    refresh_token_hash = db.Column(db.String(64), unique=True, nullable=False)
    is_revoked = db.Column(db.Boolean, default=False)
    
    expires_at = db.Column(db.DateTime(timezone=True), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), default=datetime.now(timezone.utc))
    
    ip_address = db.Column(db.String(45))
    user_agent = db.Column(db.String(255))

    auth = db.relationship("Auth", back_populates="refresh_tokens")

    def __repr__(self):
        return f"<RefreshToken Auth={self.auth_id} revoked={self.is_revoked}>"