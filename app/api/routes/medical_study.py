from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional, Union
from enum import Enum

from ...services.medical_study_service import MedicalStudyService
from ...infrastructure.repositories.medical_study_repo import MedicalStudyRepo
from ...infrastructure.db.DTOs.medical_study_dto import MedicalStudyUpdateDTO
from ...infrastructure.repositories.user_repo import UserRepo
from ...infrastructure.db.DTOs.response import MessageResponse
from ...infrastructure.db.DTOs.medical_study_dto import MedicalStudyCreateDTO, MedicalStudyResponseDTO
from ...core.db import get_db_session as get_db

class MedicalStudySearchType(str, Enum):
    ALL = "all"
    ID = "id"
    PATIENT_DNI = "patient_dni"
    PATIENT_NAME = "patient_name"

router = APIRouter(prefix="/medical_studies", tags=["Medical Studies"])

def get_medical_study_service(db: Session = Depends(get_db)) -> MedicalStudyService:
    # El servicio necesita los repositorios para funcionar
    study_repo = MedicalStudyRepo()
    user_repo = UserRepo()
    return MedicalStudyService(medical_study_repo=study_repo, user_repo=user_repo)

@router.post("/", response_model=MedicalStudyResponseDTO, status_code=status.HTTP_201_CREATED)
def create_medical_study(
    study_data: MedicalStudyCreateDTO,
    study_service: MedicalStudyService = Depends(get_medical_study_service),
    db: Session = Depends(get_db)
):
    """
    Crea una nueva orden de estudio médico.
    """
    try:
        return study_service.create_study(db, study_data=study_data)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.get("/search/", response_model=Union[List[MedicalStudyResponseDTO], MedicalStudyResponseDTO])
def search_medical_studies(
    search_type: MedicalStudySearchType = Query(..., description="Tipo de búsqueda a realizar"),
    study_id: Optional[int] = Query(None, description="ID del estudio (si search_type es 'id')"),
    patient_dni: Optional[str] = Query(None, description="DNI del paciente (si search_type es 'patient_dni')"),
    patient_name: Optional[str] = Query(None, description="Nombre o apellido del paciente (si search_type es 'patient_name')"),
    study_service: MedicalStudyService = Depends(get_medical_study_service),
    db: Session = Depends(get_db)
):
    """
    Búsqueda unificada de estudios médicos.
    """
    if search_type == MedicalStudySearchType.ALL:
        return study_service.find_all_studies(db)
    
    if search_type == MedicalStudySearchType.ID:
        if not study_id:
            raise HTTPException(status_code=400, detail="study_id is required for 'id' search type")
        return study_service.get_study_by_id(db, study_id=study_id)
        
    if search_type == MedicalStudySearchType.PATIENT_DNI:
        if not patient_dni:
            raise HTTPException(status_code=400, detail="patient_dni is required for 'patient_dni' search type")
        return study_service.find_by_patient_dni(db, dni=patient_dni)
        
    if search_type == MedicalStudySearchType.PATIENT_NAME:
        if not patient_name:
            raise HTTPException(status_code=400, detail="patient_name is required for 'patient_name' search type")
        return study_service.find_by_patient_name(db, name=patient_name)

@router.delete("/{study_id}", response_model=MessageResponse)
def delete_medical_study(
    study_id: int,
    study_service: MedicalStudyService = Depends(get_medical_study_service),
    db: Session = Depends(get_db)
):
    """
    Elimina un estudio médico por su ID.
    """
    study_service.delete_study(db, study_id=study_id)
    return MessageResponse(message=f"Medical study with id {study_id} deleted successfully.")

@router.patch("/{study_id}", response_model=MedicalStudyResponseDTO)
def partial_update_study(
    study_id: int,
    study_data: MedicalStudyUpdateDTO, # El DTO con campos opcionales
    study_service: MedicalStudyService = Depends(get_medical_study_service),
    db: Session = Depends(get_db)
):
    """
    Actualiza parcialmente un estudio médico existente.
    Solo envía los campos que deseas cambiar en el cuerpo de la petición.
    """
    try:
        updated_study = study_service.update(db, study_id=study_id, study_update=study_data)
        # Es buena práctica hacer commit aquí, en la capa del endpoint
        db.commit()
        return updated_study
    except HTTPException:
        db.rollback()
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))