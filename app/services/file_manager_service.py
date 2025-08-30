import uuid
from fastapi import UploadFile, HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional
from uuid import UUID

from ..infrastructure.repositories.file_manager_repo import FileStorageRepo
from ..infrastructure.db.DTOs.file_manager_dto import FileStorageBaseDTO, FileStorageResponseDTO

class FileStorageService:
    def __init__(self, file_storage_repo: FileStorageRepo):
        self.__file_storage_repo = file_storage_repo

    async def save_file_to_db(
        self, 
        db: Session, 
        file: UploadFile, 
        user_id: UUID, 
        custom_filename: Optional[str] = None,
        description: Optional[str] = None
    ) -> FileStorageResponseDTO:
        """
        Guarda un archivo en la base de datos.
        
        Args:
            db: Session de base de datos
            file: Archivo a guardar
            user_id: UUID del usuario que sube el archivo
            custom_filename: Nombre personalizado para el archivo (opcional)
            description: Descripción del archivo (opcional)
        
        Returns:
            FileStorageResponseDTO: Información del archivo guardado
        """
        try:
            # Leer el contenido del archivo
            file_content = await file.read()
            
            # Crear el DTO para guardar el archivo
            file_data = FileStorageBaseDTO(
                filename=custom_filename or file.filename,
                original_filename=file.filename,
                file_type=file.content_type or 'application/octet-stream',
                file_size=len(file_content),
                file_content_binary=file_content,
                description=description,
                user_id=user_id  # ← Ya es UUID, no necesita conversión
            )
            
            # Guardar en la base de datos
            saved_file = self.__file_storage_repo.create(db, obj_in=file_data.model_dump())
            
            return FileStorageResponseDTO.model_validate(saved_file)
            
        except Exception as e:
            print(f"Error saving file to database: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error saving file: {str(e)}"
            )

    def get_file_by_id(self, db: Session, file_id: UUID) -> Optional[FileStorageResponseDTO]:
        """
        Obtiene un archivo por su ID.
        """
        file_record = self.__file_storage_repo.get(db, id=file_id)
        if not file_record:
            return None
        
        return FileStorageResponseDTO.model_validate(file_record)

    def delete_file(self, db: Session, file_id: UUID, user_id: UUID) -> bool:
        """
        Elimina un archivo (solo el propietario puede eliminarlo).
        """
        file_record = self.__file_storage_repo.get(db, id=file_id)
        if not file_record:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="File not found"
            )
        
        if file_record.user_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to delete this file"
            )
        
        self.__file_storage_repo.delete(db, id=file_id)
        return True