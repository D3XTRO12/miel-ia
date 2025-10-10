import json
import pathlib
from sqlalchemy.orm import Session
from fastapi import UploadFile, HTTPException, status
from uuid import UUID
from .medical_study_service import MedicalStudyService
from .file_manager_service import FileStorageService
from ..infrastructure.db.DTOs.medical_study_dto import MedicalStudyUpdateDTO
from ..ml_pipeline.pipeline import run_diagnosis_pipeline

class DiagnoseService:
    def __init__(self, study_service: MedicalStudyService, file_service: FileStorageService):
        self.__study_service = study_service
        self.__file_service = file_service

    async def run_diagnosis_workflow(self, db: Session, study_id: UUID, file: UploadFile, user_id: UUID):
        # 1. Validar que el estudio exista y esté pendiente
        # USAR el método del repositorio directamente para obtener el objeto del modelo, no el DTO
        from ..infrastructure.repositories.medical_study_repo import MedicalStudyRepo
        study_repo = MedicalStudyRepo()
        study = study_repo.get_by_id(db, study_id)  # ← Esto devuelve el objeto MedicalStudy, no el DTO
        
        if not study:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Medical study with ID {study_id} not found."
            )
            
        if study.status != "PENDING":
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Medical study with ID {study_id} is not in PENDING state."
            )

        # 2. Generar el nuevo nombre de archivo personalizado
        # Acceder directamente a las relaciones del modelo
        patient = study.patient
        
        # CORREGIDO: Usar created_at del modelo, no creation_date del DTO
        study_date_str = study.created_at.strftime('%Y%m%d')
        original_extension = pathlib.Path(file.filename).suffix
        new_filename = f"{patient.id}_{patient.name}_{patient.last_name}_{study_date_str}{original_extension}".replace(" ", "_")
        
        # 3. Guardar el archivo con su nuevo nombre
        saved_file = await self.__file_service.save_file_to_db(
            db, file=file, user_id=user_id, custom_filename=new_filename
        )
        
        # 4. Ejecutar el pipeline de ML
        try:
            await file.seek(0)
            ml_verdict = run_diagnosis_pipeline(file.file)
        except ValueError as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"An error occurred during ML processing: {e}")

        # 5. Actualizar el estudio médico
        update_data = MedicalStudyUpdateDTO(
            status="COMPLETED",
            ml_results=json.dumps(ml_verdict),
            csv_file_id=saved_file.id
        )
        
        # Usar el servicio para actualizar (esto maneja la conversión a DTO)
        updated_study = self.__study_service.update(db, study_id=study.id, study_update=update_data)
        
        return updated_study