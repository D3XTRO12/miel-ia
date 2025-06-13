from sqlalchemy.orm import Session
from fastapi import UploadFile, HTTPException, status
from ..infrastructure.repositories.file_manager_repo import FileStorageRepo
from typing import Optional # <-- Añadir Optional

class FileStorageService:
    def __init__(self, file_storage_repo: FileStorageRepo):
        self.__file_storage_repo = file_storage_repo

    async def save_file_to_db(self, db: Session, *, file: UploadFile, user_id: int, custom_filename: Optional[str] = None):
        """
        Procesa un archivo subido y prepara su registro para ser guardado en la BD.
        Ahora acepta un nombre de archivo personalizado.
        """
        file_content_binary = await file.read()

        if not file_content_binary:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Cannot save an empty file.")

        # Usa el nombre de archivo personalizado si se proporciona; si no, usa el original.
        filename_to_save = custom_filename or file.filename

        file_data = {
            "filename": filename_to_save,
            "original_filename": file.filename,
            "file_type": file.content_type,
            "file_size": len(file_content_binary),
            "file_content_binary": file_content_binary,
            "user_id": str(user_id)
        }
        
        db_file = self.__file_storage_repo.create(db, obj_in=file_data)
        return db_file