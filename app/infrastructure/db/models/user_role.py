from ....core.db import Base
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship


class UserRole(Base):
    __tablename__ = "user_roles"
    id: int = Column(Integer, primary_key=True, index=True)
    role_id: int = Column(Integer, ForeignKey("roles.id"), nullable=False)
    user_id: int = Column(Integer, ForeignKey("users.id"), nullable=False)

    user = relationship("User", back_populates="role_associations") # <-- El cambio clave
    role = relationship("Role", back_populates="user_associations")