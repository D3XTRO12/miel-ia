from .base_repo import Create, Read, Update, Delete
from app.infrastructure.db.builder.medical_study_builder import MedicalStudyBuilder
from typing import List, Optional
from app.infrastructure.db.db import SessionLocal

class MedicalStudyRepo(Create, Read, Update, Delete):
    def __init__(self):
        self.session = SessionLocal()

    def create(self, item: MedicalStudyBuilder) -> MedicalStudyBuilder:
        """Crea un nuevo estudio médico en la base de datos."""
        study = item.build()
        self.session.add(study)
        self.session.commit()
        self.session.refresh(study)
        return study

    def read(self, item_id: int) -> Optional[MedicalStudyBuilder]:
        """Lee un estudio médico de la base de datos por su ID."""
        return self.session.query(MedicalStudyBuilder).filter(MedicalStudyBuilder.id == item_id).first()

    def update(self, item: MedicalStudyBuilder) -> MedicalStudyBuilder:
        """Actualiza un estudio médico en la base de datos."""
        self.session.merge(item)
        self.session.commit()
        return item

    def delete(self, item_id: int) -> None:
        """Elimina un estudio médico de la base de datos por su ID."""
        study = self.read(item_id)
        if study:
            self.session.delete(study)
            self.session.commit()