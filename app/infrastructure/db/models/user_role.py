from sqlalchemy import Column, ForeignKey, CHAR
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from .base_model import BaseModel

class UserRole(BaseModel):
    __tablename__ = "user_roles"
    """Tabla para almacenar las asociaciones entre usuarios y roles"""
    
    role_id = Column(CHAR(36, collation='ascii_bin'), ForeignKey("roles.id"), nullable=False ,default=lambda: str(uuid.uuid4()))
    user_id = Column(CHAR(36, collation='ascii_bin'), ForeignKey("users.id"), nullable=False ,default=lambda: str(uuid.uuid4()))


    user = relationship("User", back_populates="role_associations")
    role = relationship("Role", back_populates="user_associations")
