import uuid
from sqlalchemy.orm import Session
from typing import List, Optional, Union
from ...infrastructure.db.models.user_role import UserRole
from ...infrastructure.db.DTOs.user_role_dto import (
    UserRoleCreateDTO,
    UserRoleUpdateDTO,
)
from ...infrastructure.repositories.base_repo import BaseRepository

class UserRoleRepo(BaseRepository[UserRole]):
    def _normalize_id(self, id_value: Union[str, uuid.UUID]) -> str:
        """Normaliza IDs a string para consistencia"""
        if isinstance(id_value, uuid.UUID):
            return str(id_value)
        return str(id_value) if id_value is not None else None
    
    def get(self, db: Session, id: Union[str, uuid.UUID]) -> Optional[UserRole]:
        """Obtiene una relación user_role por UUID (acepta string o UUID)"""
        normalized_id = self._normalize_id(id)
        return db.query(UserRole).filter(UserRole.id == normalized_id).first()
    
    def get_by_role_id(self, db: Session, role_id: Union[str, uuid.UUID]) -> List[UserRole]:
        """Obtiene todas las asignaciones de rol para un role_id dado."""
        normalized_role_id = self._normalize_id(role_id)
        return db.query(UserRole).filter(UserRole.role_id == normalized_role_id).all()

    def create(self, db: Session, *, obj_in: UserRoleCreateDTO) -> UserRole:
        create_data = obj_in.model_dump()
        create_data['user_id'] = self._normalize_id(create_data['user_id'])
        create_data['role_id'] = self._normalize_id(create_data['role_id'])
        
        db_user_role = UserRole(**create_data)
        db.add(db_user_role)
        db.commit()
        db.refresh(db_user_role)
        return db_user_role
    
    def get_by_user_id(self, db: Session, user_id: Union[str, uuid.UUID]) -> List[UserRole]:
        """Obtiene todas las asignaciones de rol para un user_id dado."""
        normalized_user_id = self._normalize_id(user_id)
        return db.query(UserRole).filter(UserRole.user_id == normalized_user_id).all()

    def update(self, db: Session, *, db_obj: UserRole, obj_in: UserRoleUpdateDTO) -> UserRole:
        update_data = obj_in.model_dump(exclude_unset=True)
        
        if 'user_id' in update_data:
            update_data['user_id'] = self._normalize_id(update_data['user_id'])
        if 'role_id' in update_data:
            update_data['role_id'] = self._normalize_id(update_data['role_id'])
            
        for field, value in update_data.items():
            setattr(db_obj, field, value)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def delete(self, db: Session, *, id: Union[str, uuid.UUID]) -> UserRole:
        """Elimina una relación user_role por UUID (acepta string o UUID)"""
        normalized_id = self._normalize_id(id)
        db_user_role = db.query(UserRole).filter(UserRole.id == normalized_id).first()
        if not db_user_role:
            raise ValueError("UserRole not found")
        db.delete(db_user_role)
        db.commit()
        return db_user_role

    def get_by_user_and_role(self, db: Session, user_id: Union[str, uuid.UUID], role_id: Union[str, uuid.UUID]) -> Optional[UserRole]:
        """Busca una relación específica user-role (acepta strings o UUIDs)"""
        normalized_user_id = self._normalize_id(user_id)
        normalized_role_id = self._normalize_id(role_id)
        
        return (
            db.query(UserRole)
            .filter(UserRole.user_id == normalized_user_id, UserRole.role_id == normalized_role_id)
            .first()
        )