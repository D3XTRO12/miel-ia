from sqlalchemy import Column, Integer, String, Text, DateTime, LargeBinary
from sqlalchemy.sql import func
import base64
from app.infrastructure.db.db import Base

class FileStorage(Base):
    __tablename__ = 'file_storage'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    filename = Column(String(255), nullable=False)
    original_filename = Column(String(255), nullable=False)
    file_type = Column(String(10), default='csv')
    file_size = Column(Integer)  # Tamaño en bytes
    
    # Opción A: Almacenar como BLOB (binario)
    file_content_binary = Column(LargeBinary)
    
    # Metadatos adicionales
    description = Column(Text)
    tags = Column(String(500))  # Tags separados por comas
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Info del usuario/sesión que subió el archivo
    user_id = Column(String(100))
    session_id = Column(String(100))

# Funciones helper para manejar archivos
class FileManager:
    
    @staticmethod
    def save_csv_file(db_session, file_content, filename, user_id=None):
        """
        Guarda un archivo CSV en la base de datos
        """
        # Si file_content es bytes, convertir a string
        if isinstance(file_content, bytes):
            content_text = file_content.decode('utf-8')
            content_binary = file_content
        else:
            content_text = file_content
            content_binary = file_content.encode('utf-8')
        
        file_record = FileStorage(
            filename=filename,
            original_filename=filename,
            file_type='csv',
            file_size=len(content_binary),
            file_content_binary=content_binary,
            file_content_text=content_text,
            user_id=user_id
        )
        
        db_session.add(file_record)
        db_session.commit()
        return file_record.id
    
    @staticmethod
    def get_csv_file(db_session, file_id):
        """
        Recupera un archivo CSV de la base de datos
        """
        file_record = db_session.query(FileStorage).filter(
            FileStorage.id == file_id
        ).first()
        
        if file_record:
            return {
                'id': file_record.id,
                'filename': file_record.filename,
                'content': file_record.file_content_text,
                'size': file_record.file_size,
                'created_at': file_record.created_at
            }
        return None
    
    @staticmethod
    def list_user_files(db_session, user_id=None):
        """
        Lista archivos de un usuario específico
        """
        query = db_session.query(FileStorage)
        if user_id:
            query = query.filter(FileStorage.user_id == user_id)
        
        return query.order_by(FileStorage.created_at.desc()).all()
    
    @staticmethod
    def delete_file(db_session, file_id):
        """
        Elimina un archivo de la base de datos
        """
        file_record = db_session.query(FileStorage).filter(
            FileStorage.id == file_id
        ).first()
        
        if file_record:
            db_session.delete(file_record)
            db_session.commit()
            return True
        return False