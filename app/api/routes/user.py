# app/api/routes/user.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional

from ...api.v1.auth import get_current_user
from ...infrastructure.db.DTOs.auth_schema import UserOut
from ...core.db import get_db_session as get_db
from ...infrastructure.db.DTOs.user_dto import (
    UserCreateDTO,
    UserUpdateDTO,
    UserResponseDTO as UserResponse,
    UserCreateInternal
)
from ...infrastructure.repositories.user_repo import UserRepo
from ...services.user_service import UserService
from ...services.auth_service import get_auth_service, AuthService

router = APIRouter(
    prefix="/api/v1/users",
    tags=["users"]
)

# Dependency para obtener el servicio de usuarios
def get_user_service(db: Session = Depends(get_db)) -> UserService:
    user_repo = UserRepo(db)
    return UserService(user_repo=user_repo)

# Dependency para obtener el repositorio de usuarios
def get_user_repository(db: Session = Depends(get_db)) -> UserRepo:
    return UserRepo(db)

@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(
    user_data: UserCreateDTO,
    db: Session = Depends(get_db),
    user_service: UserService = Depends(get_user_service),
    current_user: UserOut = Depends(get_current_user)
) -> UserResponse:
    """Crear un nuevo usuario"""
    try:
        # Convertir UserCreateDTO a UserCreateInternal
        user_for_creation = UserCreateInternal(
            name=user_data.name,
            last_name=user_data.last_name or "",
            email=user_data.email,
            dni=user_data.dni,
            password=user_data.password
        )
        
        user = user_service.create_user(db, user_for_creation)
        return UserResponse.model_validate(user)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error creating user: {str(e)}"
        )

@router.get("/", response_model=List[UserResponse])
async def get_users(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    user_repo: UserRepo = Depends(get_user_repository),
    current_user: UserOut = Depends(get_current_user)

) -> List[UserResponse]:
    """Obtener lista de usuarios"""
    try:
        users = user_repo.get_all(db, skip=skip, limit=limit)
        return [UserResponse.model_validate(user) for user in users]
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving users: {str(e)}"
        )

@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: int,
    db: Session = Depends(get_db),
    user_repo: UserRepo = Depends(get_user_repository),
    current_user: UserOut = Depends(get_current_user)
) -> UserResponse:
    """Obtener un usuario por ID"""
    try:
        user = user_repo.get(db, id=user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        return UserResponse.model_validate(user)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving user: {str(e)}"
        )

@router.put("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: int,
    user_data: UserUpdateDTO,
    db: Session = Depends(get_db),
    user_repo: UserRepo = Depends(get_user_repository),
    current_user: UserOut = Depends(get_current_user)
) -> UserResponse:
    """Actualizar un usuario"""
    try:
        # Obtener el usuario existente
        existing_user = user_repo.get(db, id=user_id)
        if not existing_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        # Actualizar el usuario
        updated_user = user_repo.update(db, db_obj=existing_user, obj_in=user_data)
        return UserResponse.model_validate(updated_user)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error updating user: {str(e)}"
        )

@router.delete("/{user_id}", response_model=UserResponse)
async def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    user_repo: UserRepo = Depends(get_user_repository),
    current_user: UserOut = Depends(get_current_user)
) -> UserResponse:
    """Eliminar un usuario"""
    try:
        deleted_user = user_repo.delete(db, id=user_id)
        return UserResponse.model_validate(deleted_user)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error deleting user: {str(e)}"
        )

@router.get("/by-email/{email}", response_model=UserResponse)
async def get_user_by_email(
    email: str,
    db: Session = Depends(get_db),
    user_repo: UserRepo = Depends(get_user_repository),
    current_user: UserOut = Depends(get_current_user)

) -> UserResponse:
    """Obtener un usuario por email"""
    try:
        user = user_repo.get_by_email(db, email=email)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        return UserResponse.model_validate(user)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving user: {str(e)}"
        )

@router.get("/by-dni/{dni}", response_model=UserResponse)
async def get_user_by_dni(
    dni: str,
    db: Session = Depends(get_db),
    user_repo: UserRepo = Depends(get_user_repository),
    current_user: UserOut = Depends(get_current_user)
) -> UserResponse:
    """Obtener un usuario por DNI"""
    try:
        user = user_repo.get_by_dni(db, dni=dni)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        return UserResponse.model_validate(user)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving user: {str(e)}"
        )