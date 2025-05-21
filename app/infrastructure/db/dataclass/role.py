from dataclasses import dataclass
from app import db
from sqlalchemy import Column, Integer, String

@dataclass
class Role(db.Model):
    __tablename__ = "roles"
    id: int = Column(Integer, primary_key=True, index=True)
    name: str = Column(String(50), unique=True, nullable=False)