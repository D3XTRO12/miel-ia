from dataclasses import dataclass
from app import db
from sqlalchemy import BINARY, Column, ForeignKey, Integer, String, event
from sqlalchemy.orm import relationship
import uuid

@dataclass
class User(db.Model):
    __tablename__ = 'users'
    
    id: bytes = Column(BINARY(16), primary_key=True)
    name: str = Column(String(50), nullable=False)
    dni: int = Column(Integer, nullable=False, unique=True)
    gender: str = Column(String(50), nullable=False)
    email: str = Column(String(100), nullable=False, unique=True)
    phone: str = Column(String(50), nullable=False)
    address: str = Column(String(255), nullable=False)
    password: str = Column(String(200), nullable=False)
    role_type: str = Column(String(50), nullable=False)

    def __init__(self, **kwargs):
        self.id = uuid.uuid4().bytes
        super(User, self).__init__(**kwargs)

    @property
    def uuid(self):
        return uuid.UUID(bytes=self.id)

@event.listens_for(User, 'before_insert')
def user_before_insert(mapper, connection, target):
    if target.id is None:
        target.id = uuid.uuid4().bytes