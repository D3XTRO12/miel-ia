from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID

from ...infrastructure.db.DTOs.auth_schema import UserOut
from ...services.diagnose_service import DiagnoseService
from ...infrastructure.db.DTOs.medical_study_dto import MedicalStudyResponseDTO
from ...services.medical_study_service import MedicalStudyService
from ...services.file_manager_service import FileStorageService
from ...infrastructure.repositories.medical_study_repo import MedicalStudyRepo
from ...infrastructure.repositories.file_manager_repo import FileStorageRepo
from ...infrastructure.repositories.user_repo import UserRepo
from ...core.db import get_db_session as get_db
from ...api.v1.auth import get_current_user

router = APIRouter(prefix="/diagnose", tags=["Diagnosis"])

# CORREGIDO: Pasar la sesión db a los repositorios
def get_diagnose_service(db: Session = Depends(get_db)) -> DiagnoseService:
    """
    Construye y provee el servicio de diagnóstico con todas sus dependencias.
    """
    return DiagnoseService(
        study_service=MedicalStudyService(
            medical_study_repo=MedicalStudyRepo(), 
            user_repo=UserRepo(db)  # ← CORREGIDO: Pasar la sesión
        ),
        file_service=FileStorageService(
            file_storage_repo=FileStorageRepo()  # Si FileStorageRepo necesita db, pásala aquí también
        )
    )

@router.post("/{study_id}", response_model=MedicalStudyResponseDTO)
async def perform_diagnosis(
    study_id: UUID,
    user_id: UUID = Form(..., description="ID del técnico/doctor que realiza el diagnóstico."),
    file: UploadFile = File(..., description="Archivo CSV con datos del electromiograma."),
    db: Session = Depends(get_db),
    diagnose_service: DiagnoseService = Depends(get_diagnose_service),
    current_user: UserOut = Depends(get_current_user)
):
    """
    Recibe un CSV para un estudio, ejecuta el pipeline de diagnóstico,
    guarda el archivo y actualiza el estudio con los resultados.
    """
    print(f"🔍 DEBUG - Endpoint called:")
    print(f"  study_id: {study_id} (type: {type(study_id)})")
    print(f"  user_id: {user_id} (type: {type(user_id)})")
    print(f"  file: {file.filename}")
    print(f"  current_user: {current_user.id}")
    
    if not file.filename or not file.filename.endswith(('.csv', '.CSV')):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid file type. Only CSV files are allowed."
        )
        
    try:
        print(f"🔍 Calling diagnose_service.run_diagnosis_workflow...")
        
        updated_study = await diagnose_service.run_diagnosis_workflow(
            db, study_id=study_id, file=file, user_id=user_id
        )
        
        db.commit() 
        print(f"✅ Diagnosis completed successfully")
        return updated_study
        
    except HTTPException as he:
        db.rollback()
        print(f"❌ HTTPException: {he.status_code} - {he.detail}")
        raise he
    except Exception as e:
        db.rollback()
        print(f"❌ Unexpected error: {str(e)}")
        import traceback
        traceback_str = traceback.format_exc()
        print(f"🔍 Full traceback:\n{traceback_str}")
        
        # Detectar si es un error de UUID/CHAR
        if "char" in str(e).lower() or "uuid" in str(e).lower():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Error en formato de ID: {str(e)}"
            )
        
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail=f"Internal server error: {str(e)}"
        )