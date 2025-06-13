from fastapi import APIRouter, Depends, HTTPException, Query, Path, status
from typing import Optional, List, Union
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from enum import Enum
from pydantic import BaseModel, EmailStr


# Enums
class SearchType(Enum):
    ALL = "all"
    ID = "id"
    NAME = "name"
    DNI = "dni"

# DTOs y modelos
from ...infrastructure.db.models.user import User
from ...infrastructure.db.DTOs.user_dto import (
    UserCreateDTO as UserCreate,
    UserUpdateDTO as UserUpdate,
    UserResponseDTO as UserResponse,
    UserCreateInternal
)
from ...infrastructure.db.DTOs.response import MessageResponse
from ...infrastructure.db.DTOs.user_role_dto import UserRoleCreateDTO

# Servicios y repositorios
from ...services.user_service import UserService
from ...services.role_service import RoleService
from ...services.user_role_service import UserRoleService
from ...infrastructure.repositories.user_repo import UserRepo
from ...infrastructure.repositories.user_role_repo import UserRoleRepo
from ...infrastructure.repositories.role_repo import RoleRepo
# DB
from core.db import get_db_session as get_db

router = APIRouter(prefix="/users", tags=["users"])

# Dependencies

def get_role_service(db: Session = Depends(get_db)) -> RoleService:
    return RoleService(role_repo=RoleRepo())

def get_user_repository(db: Session = Depends(get_db)) -> UserRepo:
    return UserRepo()

def get_user_service(db: Session = Depends(get_db)) -> UserService:
    return UserService(user_repo=UserRepo())

def get_user_role_service(db: Session = Depends(get_db)) -> UserRoleService:
    user_repo = UserRepo()
    role_repo = RoleRepo()
    user_role_repo = UserRoleRepo()
    return UserRoleService(user_role_repo, user_repo, role_repo)

@router.get("/", response_model=List[UserResponse])
async def get_all_users(
    skip: int = 0,
    limit: int = 100,
    user_service: UserService = Depends(get_user_service),
    db: Session = Depends(get_db)
):
    """Obtener todos los usuarios con paginación"""
    return user_service.find_all(db)[skip:skip+limit]

@router.get("/search", response_model=Union[List[UserResponse], UserResponse])
async def search_users(
    search_type: SearchType = Query(..., description="Tipo de búsqueda"),
    user_id: Optional[int] = Query(None, description="ID del usuario"),
    name: Optional[str] = Query(None, description="Nombre del usuario"),
    dni: Optional[str] = Query(None, description="DNI del usuario"),
    user_service: UserService = Depends(get_user_service),
    db: Session = Depends(get_db)
):
    """Búsqueda unificada de usuarios"""
    try:
        if search_type == SearchType.ALL:
            return user_service.find_all(db)
        elif search_type == SearchType.ID and user_id:
            return user_service.find_by_id(db, user_id)
        elif search_type == SearchType.NAME and name:
            return user_service.find_by_name(db, name)
        elif search_type == SearchType.DNI and dni:
            return user_service.find_by_dni(db, dni)
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid search parameters for the selected search type"
            )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(
    user_data: UserCreate,
    user_service: UserService = Depends(get_user_service),
    user_role_service: UserRoleService = Depends(get_user_role_service),
    role_service: RoleService = Depends(get_role_service),
    db: Session = Depends(get_db)
):
    """Crear un nuevo usuario y asignarle un rol"""
    try:
        role_service.get_role(db, role_id=user_data.role_id)

        user_for_creation = UserCreateInternal.model_validate(user_data)
        user = user_service.create_user(db, user_for_creation)

        user_role_data = UserRoleCreateDTO(user_id=user.id, role_id=user_data.role_id)
        
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
    
@router.put("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: int,
    user_data: UserUpdate,
    user_service: UserService = Depends(get_user_service),
    db: Session = Depends(get_db)
):
    """Actualizar un usuario existente"""
    return user_service.update(db, user_id, user_data)

@router.delete("/{user_id}", response_model=MessageResponse)
async def delete_user(
    user_id: int,
    user_service: UserService = Depends(get_user_service),
    db: Session = Depends(get_db)
):
    """Eliminar un usuario por ID"""
    user_service.delete(db, user_id)
    return MessageResponse(message=f"User {user_id} deleted successfully")
