from sqlalchemy.orm import Session
from typing import Dict, Any, Optional
from .base_repo import BaseRepository
from ..db.models.file_manager import FileStorage

class FileStorageRepo(BaseRepository[FileStorage]):
    """
    Repositorio para las operaciones de base de datos de la entidad FileStorage.
    Ahora implementa todos los métodos abstractos de BaseRepository.
    """
    def __init__(self):
        self.model = FileStorage

    def get(self, db: Session, *, id: int) -> Optional[FileStorage]:
        """Obtiene un registro de archivo por su ID."""
        return db.query(self.model).filter(self.model.id == id).first()

    def create(self, db: Session, *, obj_in: Dict[str, Any]) -> FileStorage:
        """
        Crea un registro de archivo en la sesión de la base de datos.
        No hace commit; la transacción se maneja en una capa superior.
        """
        db_obj = self.model(**obj_in)
        db.add(db_obj)
        db.flush()
        db.refresh(db_obj)
        return db_obj

    def update(self, db: Session, *, db_obj: FileStorage, obj_in: Dict[str, Any]) -> FileStorage:
        """
        Actualiza un registro de archivo.
        'db_obj' es el objeto SQLAlchemy a actualizar.
        'obj_in' es un diccionario con los campos a actualizar.
        """
        for field, value in obj_in.items():
            if hasattr(db_obj, field):
                setattr(db_obj, field, value)
        
        db.add(db_obj)
        db.flush()
        db.refresh(db_obj)
        return db_obj

    def delete(self, db: Session, *, id: int) -> Optional[FileStorage]:
        """
        Elimina un registro de archivo por su ID.
        """
        db_obj = self.get(db, id=id)
        if db_obj:
            db.delete(db_obj)
        return db_obj
