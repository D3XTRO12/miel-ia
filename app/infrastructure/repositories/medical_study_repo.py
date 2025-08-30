from uuid import UUID
from fastapi import HTTPException, status
from sqlalchemy.orm import Session, joinedload
from typing import Dict, Any, Optional, List

from ..db.models.user import User
from .base_repo import BaseRepository
from ..db.models.medical_study import MedicalStudy

class MedicalStudyRepo(BaseRepository[MedicalStudy]):
    def __init__(self):
        self.__study_model = MedicalStudy
        self.__user_model = User

    def get_by_id(self, db: Session, id: UUID) -> Optional[MedicalStudy]:
        """
        Obtiene un estudio médico por ID con todas las relaciones cargadas.
        """
        return db.query(MedicalStudy).options(
            joinedload(MedicalStudy.patient),
            joinedload(MedicalStudy.doctor), 
            joinedload(MedicalStudy.technician)
        ).filter(MedicalStudy.id == id).first()
    
    def get(self, db: Session) -> list[MedicalStudy]:
        """
        Obtiene todos los estudios médicos con relaciones cargadas.
        """
        return db.query(MedicalStudy).options(
            joinedload(MedicalStudy.patient),
            joinedload(MedicalStudy.doctor),
            joinedload(MedicalStudy.technician)
        ).all()
    def get_by_patient_dni_and_access_code(self, db: Session, dni: str, access_code: str) -> List[MedicalStudy]:
        """
        Busca estudios médicos por DNI del paciente y código de acceso,
        cargando eficientemente la información del doctor.
        """
        return (
            db.query(self.__study_model)
            .options(
                # === LA LÍNEA QUE SOLUCIONA TODO ===
                # Le dice a SQLAlchemy que cargue la relación 'doctor' en la misma consulta.
                # Asume que tu modelo MedicalStudy tiene una relación llamada 'doctor'.
                joinedload(self.__study_model.doctor)
            )
            # El join con el paciente sigue siendo necesario para poder filtrar por DNI.
            .join(self.__user_model, self.__study_model.patient_id == self.__user_model.id)
            .filter(
                self.__user_model.dni == dni,
                self.__study_model.access_code == access_code
            )
            .all()
        )


    def get_by_access_code(self, db: Session, *, access_code: str) -> Optional[MedicalStudy]:
        return db.query(self.__study_model).filter(self.__study_model.access_code == access_code).first()

    
    def get_all(self, db: Session, *, skip: int = 0, limit: int = 100) -> List[MedicalStudy]:
        return (
            db.query(self.__study_model)
            .options(
                joinedload(self.__study_model.doctor),
                joinedload(self.__study_model.patient),
                joinedload(self.__study_model.technician)  # Si existe esta relación
            )
            .order_by(self.__study_model.id.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )
    def create(self, db: Session, *, obj_in: Dict[str, Any]) -> MedicalStudy:
        db_obj = self.__study_model(**obj_in)
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

    def delete(self, db: Session, *, id: UUID) -> MedicalStudy:  # Cambiar de int a UUID
        db_obj = db.query(self.__study_model).filter(self.__study_model.id == id).first()
        if not db_obj:
            raise HTTPException(status_code=404, detail="Medical study not found")
        
        db.delete(db_obj)
        db.commit()
        return db_obj