from .base_repo import Create, Read, Update, Delete
from app.infrastructure.db.builder.file_manager_builder import FileManagerBuilder
from typing import List, Optional
from app.infrastructure.db.db import SessionLocal

class FileManagerRepo(Create, Read, Update, Delete):
    def __init__(self):
        self.session = SessionLocal()

    def create(self, item: FileManagerBuilder) -> FileManagerBuilder:
        """Crea un nuevo archivo en la base de datos."""
        file_manager = item.build()
        self.session.add(file_manager)
        self.session.commit()
        self.session.refresh(file_manager)
        return file_manager

    def read(self, item_id: int) -> Optional[FileManagerBuilder]:
        """Lee un archivo de la base de datos por su ID."""
        return self.session.query(FileManagerBuilder).filter(FileManagerBuilder.id == item_id).first()

    def update(self, item: FileManagerBuilder) -> FileManagerBuilder:
        """Actualiza un archivo en la base de datos."""
        self.session.merge(item)
        self.session.commit()
        return item

    def delete(self, item_id: int) -> None:
        """Elimina un archivo de la base de datos por su ID."""
        file_manager = self.read(item_id)
        if file_manager:
            self.session.delete(file_manager)
            self.session.commit()