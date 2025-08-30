import uuid
from sqlalchemy.orm import Session
from typing import List, Optional
from ...infrastructure.db.models.user_role import UserRole
from ...infrastructure.db.DTOs.user_role_dto import (
    UserRoleCreateDTO,
    UserRoleUpdateDTO,
)
from ...infrastructure.repositories.base_repo import BaseRepository

class UserRoleRepo(BaseRepository[UserRole]):
    def get(self, db: Session, id: uuid.UUID) -> Optional[UserRole]:
        """Obtiene una relación user_role por UUID"""
        return db.query(UserRole).filter(UserRole.id == id).first()
    
    def get_by_role_id(self, db: Session, role_id: uuid.UUID) -> List[UserRole]:
        """Obtiene todas las asignaciones de rol para un role_id dado."""
        return db.query(UserRole).filter(UserRole.role_id == role_id).all()

    def create(self, db: Session, *, obj_in: UserRoleCreateDTO) -> UserRole:
        db_user_role = UserRole(**obj_in.model_dump())
        db.add(db_user_role)
        db.commit()
        db.refresh(db_user_role)
        return db_user_role
    
    def get_by_user_id(self, db: Session, user_id: uuid.UUID) -> List[UserRole]:
        """Obtiene todas las asignaciones de rol para un user_id dado."""
        return db.query(UserRole).filter(UserRole.user_id == user_id).all()

    def update(self, db: Session, *, db_obj: UserRole, obj_in: UserRoleUpdateDTO) -> UserRole:
        update_data = obj_in.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_obj, field, value)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def delete(self, db: Session, *, id: uuid.UUID) -> UserRole:
        """Elimina una relación user_role por UUID"""
        db_user_role = db.query(UserRole).filter(UserRole.id == id).first()
        if not db_user_role:
            raise ValueError("UserRole not found")
        db.delete(db_user_role)
        db.commit()
        return db_user_role

    def get_by_user_and_role(self, db: Session, user_id: uuid.UUID, role_id: uuid.UUID) -> Optional[UserRole]:
        """Busca una relación específica user-role"""
        return (
            db.query(UserRole)
            .filter(UserRole.user_id == user_id, UserRole.role_id == role_id)
            .first()
        )