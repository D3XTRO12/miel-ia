from dataclasses import dataclass
from app import db
from sqlalchemy import BINARY, Column, String, event
from sqlalchemy.orm import relationship
import uuid


@dataclass
class Role(db.Model):
    __tablename__ = 'roles'
    
    id: bytes = Column(BINARY(16), primary_key=True)
    name: str = Column(String(50), unique=True, nullable=False)

    def __init__(self, **kwargs):
        self.id = uuid.uuid4().bytes
        super(Role, self).__init__(**kwargs)

    @property
    def uuid(self):
        return uuid.UUID(bytes=self.id)

@event.listens_for(Role, 'before_insert')
def role_before_insert(mapper, connection, target):
    if target.id is None:
        target.id = uuid.uuid4().bytes