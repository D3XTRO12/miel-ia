from dataclasses import dataclass
from app.infrastructure.db.db import Base
from sqlalchemy import Column, Integer, ForeignKey

@dataclass
class UserRole(Base):
    __tablename__ = "user_roles"
    id: int = Column(Integer, primary_key=True, index=True)
    role_id: int = Column(Integer, ForeignKey("roles.id"), nullable=False)
    user_id: int = Column(Integer, ForeignKey("users.id"), nullable=False)