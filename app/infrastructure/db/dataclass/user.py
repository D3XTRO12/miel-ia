from dataclasses import dataclass
from app import db
from sqlalchemy import Column, Integer, String

@dataclass
class User(db.Model):
    __tablename__ = "users"
    id: int = Column(Integer, primary_key=True, index=True)
    dni: str = Column(String(20), unique=True, nullable=False)
    email: str = Column(String(120), unique=True, nullable=False)
    last_name: str = Column(String(100), nullable=False)
    name: str = Column(String(100), nullable=False)
    password: str = Column(String(255), nullable=False)