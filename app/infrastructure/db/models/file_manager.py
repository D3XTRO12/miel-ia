from sqlalchemy import Column, String, Text, Integer, LargeBinary
from sqlalchemy.dialects.postgresql import UUID
from .base_model import BaseModel

class FileStorage(BaseModel):
    __tablename__ = 'file_storage'
    """Tabla para almacenar archivos subidos por los usuarios"""
    
    filename = Column(String(255), nullable=False)
    original_filename = Column(String(255), nullable=False)
    file_type = Column(String(100))
    file_size = Column(Integer)
    file_content_binary = Column(LargeBinary)
    description = Column(Text)
    user_id = Column(UUID(as_uuid=True))  