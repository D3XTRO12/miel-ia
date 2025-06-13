from ....core.db import Base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.ext.associationproxy import association_proxy

class User(Base):
    __tablename__ = "users"
    id: int = Column(Integer, primary_key=True, index=True)
    dni: str = Column(String(20), unique=True, nullable=False)
    email: str = Column(String(120), unique=True, nullable=False)
    last_name: str = Column(String(100), nullable=False)
    name: str = Column(String(100), nullable=False)
    password: str = Column(String(255), nullable=False)
    role_associations = relationship("UserRole", back_populates="user", cascade="all, delete-orphan")
    roles = association_proxy("role_associations", "role")