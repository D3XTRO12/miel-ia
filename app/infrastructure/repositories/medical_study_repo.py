from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from typing import Dict, Any, Optional, List
from .base_repo import BaseRepository
from ..db.models.medical_study import MedicalStudy

class MedicalStudyRepo(BaseRepository[MedicalStudy]):
    def __init__(self):
        self.model = MedicalStudy

    def get(self, db: Session, *, id: int) -> Optional[MedicalStudy]:
        return db.query(self.model).filter(self.model.id == id).first()

    def get_by_access_code(self, db: Session, *, access_code: str) -> Optional[MedicalStudy]:
        return db.query(self.model).filter(self.model.access_code == access_code).first()

    def get_all(self, db: Session, *, skip: int = 0, limit: int = 100) -> List[MedicalStudy]:
        return db.query(self.model).order_by(self.model.id.desc()).offset(skip).limit(limit).all()

    def create(self, db: Session, *, obj_in: Dict[str, Any]) -> MedicalStudy:
        db_obj = self.model(**obj_in)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(self, db: Session, *, db_obj: MedicalStudy, obj_in: Dict[str, Any]) -> MedicalStudy:
        for field, value in obj_in.items():
            setattr(db_obj, field, value)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def delete(self, db: Session, *, id: int) -> MedicalStudy:
        db_obj = db.query(self.model).get(id)
        db.delete(db_obj)
        db.commit()
        return db_obj
    
    def find_all_studies(self, db: Session, *, skip: int = 0, limit: int = 100) -> List:
        """Obtiene todos los estudios con paginación."""
        return self.__medical_study_repo.get_all(db, skip=skip, limit=limit)

    def find_by_patient_dni(self, db: Session, *, dni: str) -> List:
        """Busca estudios por DNI del paciente."""
        studies = self.__medical_study_repo.get_by_patient_dni(db, dni=dni)
        if not studies:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No medical studies found for patient with DNI {dni}"
            )
        return studies
    
    def find_by_patient_name(self, db: Session, *, name: str) -> List:
        """Busca estudios por nombre o apellido del paciente."""
        studies = self.__medical_study_repo.get_by_patient_name(db, name=name)
        if not studies:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No medical studies found for patient with name {name}"
            )
        return studies