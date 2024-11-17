from dataclasses import dataclass
from app import db
from sqlalchemy import BINARY, Column, ForeignKey, event
from sqlalchemy.orm import relationship
import uuid

@dataclass
class UserRole(db.Model):
    __tablename__ = 'user_roles'
    
    id: bytes = Column(BINARY(16), primary_key=True)
    user_id: bytes = Column(BINARY(16), ForeignKey('users.id'), nullable=False)
    role_id: bytes = Column(BINARY(16), ForeignKey('roles.id'), nullable=False)

    # Relaciones
    user = relationship('User', backref=db.backref('roles', lazy=True))
    role = relationship('Role', backref=db.backref('users', lazy=True))

    def __init__(self, **kwargs):
        self.id = uuid.uuid4().bytes
        super(UserRole, self).__init__(**kwargs)

    @property
    def uuid(self):
        return uuid.UUID(bytes=self.id)

@event.listens_for(UserRole, 'before_insert')
def user_role_before_insert(mapper, connection, target):
    if target.id is None:
        target.id = uuid.uuid4().bytes
    if isinstance(target.user_id, (str, uuid.UUID)):
        target.user_id = uuid.UUID(target.user_id).bytes if isinstance(target.user_id, str) else target.user_id.bytes
    if isinstance(target.role_id, (str, uuid.UUID)):
        target.role_id = uuid.UUID(target.role_id).bytes if isinstance(target.role_id, str) else target.role_id.bytes