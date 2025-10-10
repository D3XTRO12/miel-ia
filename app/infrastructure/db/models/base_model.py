# app/infrastructure/db/models/base_model.py
from sqlalchemy import Column, DateTime, CHAR
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID
import uuid
from ....core.db import Base

class BaseModel(Base):
    __abstract__ = True
    """Clase base para todos los modelos de la base de datos"""
    
    id = Column(CHAR(36, collation='ascii_bin'), primary_key=True, default=lambda: str(uuid.uuid4()))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
