import uuid
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from ..infrastructure.repositories.user_role_repo import UserRoleRepo
from ..infrastructure.repositories.user_repo import UserRepo
from ..infrastructure.repositories.role_repo import RoleRepo
from typing import List
from ..infrastructure.db.DTOs.user_role_dto import (
    UserRoleCreateDTO,
    UserRoleUpdateDTO,
    UserRoleResponseDTO,
)

class UserRoleService:
    def __init__(
        self,
        user_role_repo: UserRoleRepo,
        user_repo: UserRepo,
        role_repo: RoleRepo
    ):
        self.__user_role_repo = user_role_repo
        self.__user_repo = user_repo
        self.__role_repo = role_repo
    
    def get_user_role(self, db: Session, id: uuid.UUID) -> UserRoleResponseDTO:
        """Obtiene una relación user_role por UUID"""
        user_role = self.__user_role_repo.get(db, id)
        if not user_role:
            raise HTTPException(status_code=404, detail="UserRole not found")
        return UserRoleResponseDTO.model_validate(user_role)
    
    def get_users_by_role_id(self, db: Session, role_id: uuid.UUID) -> List:
        """
        Obtiene todos los usuarios que tienen un rol específico.
        Retorna objetos User completos, no UserRole.
        """
        # Obtener las relaciones user_role para el role_id dado
        user_roles = self.__user_role_repo.get_by_role_id(db, role_id)
        
        # Extraer los user_ids
        user_ids = [ur.user_id for ur in user_roles]
        
        if not user_ids:
            return []
        
        # Obtener los usuarios completos
        users = []
        for user_id in user_ids:
            user = self.__user_repo.get(db, id=user_id)
            if user:
                users.append(user)
        
        return users
    
    def get_user_roles_by_user_id(self, db: Session, user_id: uuid.UUID) -> List[UserRoleResponseDTO]:
        """
        Obtiene todos los UserRoleResponseDTO para un user_id dado.
        """
        user_roles_orm = self.__user_role_repo.get_by_user_id(db, user_id)
        return [UserRoleResponseDTO.model_validate(ur) for ur in user_roles_orm]

    def create_user_role(self, db: Session, obj_in: UserRoleCreateDTO) -> UserRoleResponseDTO:
        # Validar existencia de user
        if not self.__user_repo.get(db, id=obj_in.user_id):
            raise HTTPException(status_code=404, detail="User not found")
        
        # Validar existencia de role
        if not self.__role_repo.get_by_id(obj_in.role_id):
            raise HTTPException(status_code=404, detail="Role not found")

        # Evitar duplicados
        existing = self.__user_role_repo.get_by_user_and_role(db, obj_in.user_id, obj_in.role_id)
        if existing:
            raise HTTPException(status_code=400, detail="User already has this role assigned")
        
        user_role = self.__user_role_repo.create(db, obj_in=obj_in)
        return UserRoleResponseDTO.model_validate(user_role)

    def update_user_role(self, db: Session, id: uuid.UUID, obj_in: UserRoleUpdateDTO) -> UserRoleResponseDTO:
        db_user_role = self.__user_role_repo.get(db, id)
        if not db_user_role:
            raise HTTPException(status_code=404, detail="UserRole not found")

        if obj_in.user_id and not self.__user_repo.get(db, obj_in.user_id):
            raise HTTPException(status_code=404, detail="User not found")
        
        if obj_in.role_id and not self.__role_repo.get_by_id(obj_in.role_id):
            raise HTTPException(status_code=404, detail="Role not found")
            
        updated = self.__user_role_repo.update(db, db_obj=db_user_role, obj_in=obj_in)
        return UserRoleResponseDTO.model_validate(updated)

    def delete_user_role(self, db: Session, id: uuid.UUID) -> UserRoleResponseDTO:
        db_user_role = self.__user_role_repo.get(db, id)
        if not db_user_role:
            raise HTTPException(status_code=404, detail="UserRole not found")
        deleted = self.__user_role_repo.delete(db, id=id)
        return UserRoleResponseDTO.model_validate(deleted)