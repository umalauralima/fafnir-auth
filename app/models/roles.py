from ..extensions import db

role_permissions = db.Table(
    'role_permissions',

    db.Column(
        'role_id',
        db.Integer,
        db.ForeignKey('roles.id', ondelete='CASCADE'),
        primary_key=True
    ),

    db.Column(
        'permission_id',
        db.Integer,
        db.ForeignKey('permissions.id', ondelete='CASCADE'),
        primary_key=True
    )
)

class Role(db.Model):

    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.String(255), nullable=True)

    permissions = db.relationship(
        'Permission',
        secondary=role_permissions,
        lazy='subquery',
        backref=db.backref('roles', lazy=True)
    )

    created_at = db.Column(
        db.DateTime,
        server_default=db.func.now()
    )

    def __repr__(self):
        return f'<Role {self.name}>'
    

