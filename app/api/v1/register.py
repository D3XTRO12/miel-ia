import os
import uuid
from typing import Optional
from pydantic import BaseModel
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ...infrastructure.db.DTOs.user_dto import UserCreateInternal, UserResponseDTO as UserResponse, UserCreateDTO as UserCreate
from ...infrastructure.db.DTOs.user_role_dto import UserRoleCreateDTO
from ...services.user_service import UserService
from ...core.db import get_db_session as get_db
from ...services.role_service import RoleService
from ...services.user_role_service import UserRoleService
from ...infrastructure.repositories.user_repo import UserRepo
from ...infrastructure.repositories.role_repo import RoleRepo
from ...infrastructure.repositories.user_role_repo import UserRoleRepo

def get_user_service(db: Session = Depends(get_db)) -> UserService:
    return UserService(user_repo=UserRepo())

def get_user_role_service(db: Session = Depends(get_db)) -> UserRoleService:
    user_repo = UserRepo(db)
    role_repo = RoleRepo(db)
    user_role_repo = UserRoleRepo(db)
    return UserRoleService(user_role_repo, user_repo, role_repo)

def get_role_service(db: Session = Depends(get_db)) -> RoleService:
    return RoleService(role_repo=RoleRepo(db))

def get_user_repository(db: Session = Depends(get_db)) -> UserRepo:
    return UserRepo(db)

router = APIRouter(
    prefix="/api/v1/register",
    tags=["register-global"]
)

class PatientRegister(BaseModel):
    email: str
    dni: str
    password: str
    name: Optional[str] = None
    last_name: Optional[str] = None

@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register_patient(
    user_data: PatientRegister,
    user_service: UserService = Depends(get_user_service),
    user_role_service: UserRoleService = Depends(get_user_role_service),
    role_service: RoleService = Depends(get_role_service),
    db: Session = Depends(get_db)
):
    """Registrar un nuevo paciente (todos los registros son pacientes por defecto)"""
    try:
        patient_role_id_str = os.getenv("PATIENT_ROLE_ID")
        
        if not patient_role_id_str:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="PATIENT_ROLE_ID environment variable not set"
            )
        
        try:
            default_patient_role_id = uuid.UUID(patient_role_id_str)
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Invalid UUID format in PATIENT_ROLE_ID environment variable"
            )
        
        role_service.get_role(role_id=default_patient_role_id)

        user_create_data = UserCreate(
            dni=user_data.dni,  
            email=user_data.email,
            password=user_data.password,
            name=user_data.name,
            last_name=user_data.last_name,
            role_id=default_patient_role_id  
        )

        user_for_creation = UserCreateInternal.model_validate(user_create_data)
        user = user_service.create_user(db, user_for_creation)

        user_role_data = UserRoleCreateDTO(user_id=user.id, role_id=default_patient_role_id)
        user_role_service.create_user_role(db, obj_in=user_role_data)

        db.refresh(user)
        return user

    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred: {e}"
        )