from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID

from ...infrastructure.db.DTOs.auth_schema import UserOut
from ...services.auth_service import get_auth_service, oauth2_scheme
from ...core.db import get_db_session as get_db

# Importamos el servicio orquestador y los DTOs necesarios
from ...services.diagnose_service import DiagnoseService
from ...infrastructure.db.DTOs.medical_study_dto import MedicalStudyResponseDTO

# Importamos todos los componentes necesarios para la inyección de dependencias
from ...services.medical_study_service import MedicalStudyService
from ...services.file_manager_service import FileStorageService
from ...infrastructure.repositories.medical_study_repo import MedicalStudyRepo
from ...infrastructure.repositories.file_manager_repo import FileStorageRepo
from ...infrastructure.repositories.user_repo import UserRepo

# Importamos la dependencia de la sesión de BD
from ...core.db import get_db_session as get_db
from ...services.auth_service import oauth2_scheme
from ...api.v1.auth import get_current_user

router = APIRouter(prefix="/diagnose", tags=["Diagnosis"])


# --- Inyección de Dependencias ---
def get_diagnose_service() -> DiagnoseService:
    """
    Construye y provee el servicio de diagnóstico con todas sus dependencias.
    """
    return DiagnoseService(
        study_service=MedicalStudyService(
            medical_study_repo=MedicalStudyRepo(), 
            user_repo=UserRepo()
        ),
        file_service=FileStorageService(
            file_storage_repo=FileStorageRepo()
        )
    )

# --- Endpoint de Diagnóstico CORREGIDO ---
@router.post("/{study_id}", response_model=MedicalStudyResponseDTO)
async def perform_diagnosis(
    study_id: UUID,  # ← CAMBIO: De int a UUID
    user_id: UUID = Form(..., description="ID del técnico/doctor que realiza el diagnóstico."),  # ← CAMBIO: De int a UUID
    file: UploadFile = File(..., description="Archivo CSV con datos del electromiograma."),
    db: Session = Depends(get_db),
    diagnose_service: DiagnoseService = Depends(get_diagnose_service),
    current_user: UserOut = Depends(get_current_user)
):
    """
    Recibe un CSV para un estudio, ejecuta el pipeline de diagnóstico,
    guarda el archivo y actualiza el estudio con los resultados.
    Toda la operación es una única transacción atómica.
    """
    if not file.filename or not file.filename.endswith(('.csv', '.CSV')):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid file type. Only CSV files are allowed."
        )
        
    try:
        updated_study = await diagnose_service.run_diagnosis_workflow(
            db, study_id=study_id, file=file, user_id=user_id
        )
        # Si todo el flujo en el servicio fue exitoso, hacemos commit a la BD.
        db.commit() 
        return updated_study
    except HTTPException:
        # Si ocurre un error HTTP conocido (400, 404, 409), hacemos rollback y lo re-lanzamos.
        db.rollback()
        raise
    except Exception as e:
        # Si ocurre cualquier otro error inesperado, hacemos rollback y devolvemos un 500.
        db.rollback()
        # En producción, es mejor no exponer el detalle del error interno
        print(f"ERROR en /diagnose/{study_id}: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An internal error occurred during diagnosis.")