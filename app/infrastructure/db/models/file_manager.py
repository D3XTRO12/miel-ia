from sqlalchemy import Column, Integer, String, Text, DateTime, LargeBinary
from sqlalchemy.sql import func
from ....core.db import Base # Asegúrate de que esta ruta a tu Base declarativa sea correcta

class FileStorage(Base):
    """
    Modelo SQLAlchemy para la tabla 'file_storage'.
    Representa el registro de un archivo guardado.
    """
    __tablename__ = 'file_storage'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    filename = Column(String(255), nullable=False)
    original_filename = Column(String(255), nullable=False)
    file_type = Column(String(100))
    file_size = Column(Integer)
    
    # Contenido del archivo almacenado como binario.
    # Para producción, se recomienda cambiar esto por una URL a un Blob Storage.
    file_content_binary = Column(LargeBinary)
    
    # Metadatos adicionales
    description = Column(Text)
    
    # Timestamps gestionados por la base de datos
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # ID del usuario que subió el archivo
    user_id = Column(String(100))
