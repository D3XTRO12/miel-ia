from dataclasses import dataclass
from app.infrastructure.db.db import Base

from sqlalchemy import Column, Integer, String

@dataclass
class Role(Base):
    __tablename__ = "roles"
    id: int = Column(Integer, primary_key=True, index=True)
    name: str = Column(String(50), unique=True, nullable=False)