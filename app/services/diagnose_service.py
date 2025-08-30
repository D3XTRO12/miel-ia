import json
import pathlib # Para manejar extensiones de archivo fácilmente
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
        study = self.__study_service.get_by_id(db, study_id=study_id)  # ← CAMBIO: usar get_by_id en lugar de get_study_by_id
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
        patient = study.patient # SQLAlchemy carga la relación automáticamente
        
        # Obtener la fecha de creación del estudio correctamente
        study_date_str = study.creation_date.strftime('%Y%m%d') if study.creation_date else study.created_at.strftime('%Y%m%d')
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

        # 5. Actualizar el estudio médico con los resultados, el nuevo estado y la referencia al archivo
        update_data = MedicalStudyUpdateDTO(
            status="COMPLETED", # El estado cambia a "Listo"
            ml_results=json.dumps(ml_verdict), # Guardamos el veredicto como JSON
            csv_file_id=saved_file.id
        )
        
        updated_study = self.__study_service.update(db, study_id=study.id, study_update=update_data)
        
        return updated_study