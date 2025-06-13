from typing import Any, List
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

# Importamos todos los DTOs que el servicio va a necesitar o devolver
from ..infrastructure.db.DTOs.user_dto import UserCreateInternal, UserUpdateDTO, UserBaseDTO
from ..infrastructure.repositories.user_repo import UserRepo
from ..core.security import get_password_hash


class UserService:
    def __init__(self, user_repo: UserRepo):
        self.__user_repo = user_repo

    # --- MÉTODOS DE BÚSQUEDA ---
    def find_all(self, db: Session, *, skip: int = 0, limit: int = 100) -> List[UserBaseDTO]:
        """Llama al repo para obtener todos los usuarios."""
        users = self.__user_repo.get_all(db, skip=skip, limit=limit)
        return users

    def find_by_id(self, db: Session, user_id: int) -> UserBaseDTO:
        """Busca un usuario por ID, si no lo encuentra, lanza error 404."""
        user = self.__user_repo.get(db, id=user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with id {user_id} not found"
            )
        return user

    def find_by_name(self, db: Session, name: str) -> List[UserBaseDTO]:
        """Busca usuarios por nombre. Devuelve una lista vacía si no hay coincidencias."""
        users = self.__user_repo.get_by_name(db, name=name)
        return users

    def find_by_dni(self, db: Session, dni: str) -> UserBaseDTO:
        """Busca un usuario por DNI, si no lo encuentra, lanza error 404."""
        user = self.__user_repo.get_by_dni(db, dni=dni)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with DNI {dni} not found"
            )
        return user
    # --- FIN DE MÉTODOS DE BÚSQUEDA ---

    def create_user(self, db: Session, user_create: UserCreateInternal) -> UserBaseDTO:
        """Crea un nuevo usuario."""
        if self.__user_repo.email_exists(db, email=user_create.email):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email already registered"
            )
        
        hashed_password = get_password_hash(user_create.password)
        user_data = user_create.model_dump()
        user_data["password"] = hashed_password

        return self.__user_repo.create(db, obj_in=user_data)
            
    def update(self, db: Session, user_id: int, user_update: UserUpdateDTO) -> UserBaseDTO:
        """Actualiza un usuario."""
        db_user = self.find_by_id(db, user_id) # Reutilizamos find_by_id para obtener y validar
        
        if user_update.email and user_update.email != db_user.email:
            if self.__user_repo.email_exists(db, email=user_update.email):
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Email already registered by another user"
                )

        return self.__user_repo.update(db, db_obj=db_user, obj_in=user_update)

    def delete(self, db: Session, user_id: int) -> UserBaseDTO:
        """Elimina un usuario."""
        db_user = self.find_by_id(db, user_id) # Reutilizamos find_by_id para obtener y validar
        return self.__user_repo.delete(db, id=user_id)