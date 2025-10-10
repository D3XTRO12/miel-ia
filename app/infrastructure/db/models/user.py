from sqlalchemy import Column, DateTime, String, Boolean, func, CHAR
from sqlalchemy.orm import relationship
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.dialects.postgresql import UUID
import uuid
from .base_model import BaseModel

class User(BaseModel):
    __tablename__ = "users"
    """Tabla para almacenar usuarios del sistema"""
    
    dni: str = Column(String(20), unique=True, nullable=False)
    email: str = Column(String(120), unique=True, nullable=False)
    last_name: str = Column(String(100), nullable=False)
    name: str = Column(String(100), nullable=False)
    password: str = Column(String(255), nullable=False)
    is_active: bool = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), nullable=True)
    
    role_associations = relationship("UserRole", back_populates="user", cascade="all, delete-orphan")
    roles = association_proxy("role_associations", "role")
    
    def verify_password(self, plain_password: str) -> bool:
        from ....core.security import verify_password
        return verify_password(plain_password, self.password)
