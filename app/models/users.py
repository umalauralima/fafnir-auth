import uuid
from datetime import datetime, timezone
from ..extensions import db

user_permissions = db.Table(
    'user_permissions',

    db.Column(
        'user_id',
        db.Integer,
        db.ForeignKey('users.id', ondelete='CASCADE'),
        primary_key=True
    ),

    db.Column(
        'permission_id',
        db.Integer,
        db.ForeignKey('permissions.id', ondelete='CASCADE'),
        primary_key=True
    )
)


user_roles = db.Table(
    'user_roles',

    db.Column(
        'user_id',
        db.Integer,
        db.ForeignKey('users.id', ondelete='CASCADE'),
        primary_key=True
    ),

    db.Column(
        'role_id',
        db.Integer,
        db.ForeignKey('roles.id', ondelete='CASCADE'),
        primary_key=True
    )
)

class User(db.Model):
    __tablename__ = 'users'

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

    # Roles do usuário
    roles = db.relationship(
        'Role',
        secondary=user_roles,
        backref='users'
    )

    # Permissões extras/diretas
    permissions = db.relationship(
        'Permission',
        secondary=user_permissions,
        lazy='subquery',
        backref=db.backref('users', lazy=True)
    )

    __table_args__ = (
        db.UniqueConstraint('email', name='uq_auth_email'),
    )

    def __repr__(self):
        return f"<Auth {self.email}>"