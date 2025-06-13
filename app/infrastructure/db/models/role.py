from ....core.db import Base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.ext.associationproxy import association_proxy # <-- 1. Importar



class Role(Base):
    __tablename__ = "roles"
    id: int = Column(Integer, primary_key=True, index=True)
    name: str = Column(String(50), unique=True, nullable=False)
    user_associations = relationship("UserRole", back_populates="role", cascade="all, delete-orphan")
    users = association_proxy("user_associations", "user")