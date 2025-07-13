from sqlalchemy import Column, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from .base_model import BaseModel

class UserRole(BaseModel):
    __tablename__ = "user_roles"
    """Tabla para almacenar las asociaciones entre usuarios y roles"""
    
    role_id = Column(UUID(as_uuid=True), ForeignKey("roles.id"), nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)

    user = relationship("User", back_populates="role_associations")
    role = relationship("Role", back_populates="user_associations")