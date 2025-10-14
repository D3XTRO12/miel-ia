import uuid
from sqlalchemy.orm import Session
from typing import Dict, Any, List, Optional, Union
from ..db.models.user import User
from ..repositories.base_repo import BaseRepository
from ...core.security import get_password_hash, verify_password
from ..db.DTOs.user_dto import UserUpdateDTO, UserCreateDTO

class UserRepo(BaseRepository[User]):
    def __init__(self, db: Session = None):
        super().__init__(User, db)
    
    def _normalize_id(self, id_value: Union[str, uuid.UUID]) -> str:
        """Normaliza IDs a string para consistencia"""
        if isinstance(id_value, uuid.UUID):
            return str(id_value)
        return str(id_value) if id_value is not None else None
    
    def get(self, db: Session, *, id: Union[str, uuid.UUID]) -> Optional[User]:
        """Obtiene un usuario por UUID (acepta string o UUID)"""
        normalized_id = self._normalize_id(id)
        return db.query(self.model).filter(self.model.id == normalized_id).first()

    def get_by_email(self, db: Session, *, email: str) -> Optional[User]:
        return db.query(self.model).filter(self.model.email == email).first()

    def email_exists(self, db: Session, *, email: str) -> bool:
        return db.query(self.model).filter(self.model.email == email).first() is not None

    def get_all(self, db: Session, *, skip: int = 0, limit: int = 100) -> List[User]:
        return db.query(self.model).offset(skip).limit(limit).all()

    def get_by_name(self, db: Session, *, name: str) -> List[User]:
        return db.query(self.model).filter(self.model.name.ilike(f"%{name}%")).all()

    def get_by_dni(self, db: Session, *, dni: str) -> Optional[User]:
        return db.query(self.model).filter(self.model.dni == dni).first()

    def dni_exists(self, db: Session, *, dni: str) -> bool:
        """Verifica si existe un usuario con el DNI dado."""
        return db.query(self.model).filter(self.model.dni == dni).first() is not None

    def create(self, db: Session, *, obj_in: UserCreateDTO | Dict[str, Any]) -> User:
        if isinstance(obj_in, dict):
            create_data = obj_in
        else:
            create_data = obj_in.model_dump(exclude_unset=True)
        
        if 'password' in create_data:
            create_data['password'] = get_password_hash(create_data['password'])

        db_obj = self.model(**create_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    
    def get_users_by_role_id(self, db: Session, role_id: Union[str, uuid.UUID]) -> List[User]:
        """
        Obtiene todos los usuarios que tienen un rol específico usando JOIN.
        """
        from ..db.models.user_role import UserRole
        
        normalized_role_id = self._normalize_id(role_id)

        return (
            db.query(User)
            .join(UserRole, User.id == UserRole.user_id)
            .filter(UserRole.role_id == normalized_role_id)
            .all()
        )

    def update(self, db: Session, *, db_obj: User, obj_in: UserUpdateDTO | Dict[str, Any]) -> User:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.model_dump(exclude_unset=True)
        
        if 'password' in update_data:
            update_data['password'] = get_password_hash(update_data['password'])
        
        for field in update_data:
            if hasattr(db_obj, field):
                setattr(db_obj, field, update_data[field])
        
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def delete(self, db: Session, *, id: Union[str, uuid.UUID]) -> User:
        """Elimina un usuario por UUID (acepta string o UUID)"""
        normalized_id = self._normalize_id(id)
        user = db.query(self.model).filter(self.model.id == normalized_id).first()
        if not user:
            raise ValueError("Usuario no encontrado para eliminar")
        
        db.delete(user)
        db.commit()
        return user
    
    def delete_with_relations(self, db: Session, *, id: Union[str, uuid.UUID]) -> User:
        """
        Elimina un usuario y todas sus relaciones en tablas intermedias (ej. user_role).
        """
        from ..db.models.user_role import UserRole

        normalized_id = self._normalize_id(id)
        user = db.query(self.model).filter(self.model.id == normalized_id).first()
        if not user:
            raise ValueError(f"Usuario con id {normalized_id} no encontrado")

        try:
            relations = db.query(UserRole).filter(UserRole.user_id == normalized_id).all()
            if relations:
                for rel in relations:
                    db.delete(rel)
                db.flush()

            db.delete(user)
            db.commit()
            return user

        except Exception as e:
            db.rollback()
            raise RuntimeError(f"Error eliminando usuario y sus relaciones: {str(e)}")


    def authenticate(self, db: Session, *, email: str, password: str) -> Optional[User]:
        user = self.get_by_email(db, email=email)
        if not user:
            return None
        if not verify_password(password, user.password):
            return None
        return user
    
    def get_multiple_by_ids(self, db: Session, user_ids: List[Union[str, uuid.UUID]]) -> List[User]:
        """Obtiene múltiples usuarios por sus UUIDs (acepta strings o UUIDs)"""
        normalized_ids = [self._normalize_id(user_id) for user_id in user_ids]
        return db.query(User).filter(User.id.in_(normalized_ids)).all()    
