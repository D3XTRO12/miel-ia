from sqlalchemy.orm import Session
from typing import Optional
from ...infrastructure.db.models.user_role import UserRole
from ...infrastructure.db.DTOs.user_role_dto import (
    UserRoleCreateDTO,
    UserRoleUpdateDTO,
)
from ...infrastructure.repositories.base_repo import BaseRepository

class UserRoleRepo(BaseRepository[UserRole]):
    def get(self, db: Session, id: int) -> Optional[UserRole]:
        return db.query(UserRole).filter(UserRole.id == id).first()

    def create(self, db: Session, *, obj_in: UserRoleCreateDTO) -> UserRole:
        db_user_role = UserRole(**obj_in.dict())
        db.add(db_user_role)
        db.commit()
        db.refresh(db_user_role)
        return db_user_role

    def update(self, db: Session, *, db_obj: UserRole, obj_in: UserRoleUpdateDTO) -> UserRole:
        update_data = obj_in.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_obj, field, value)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def delete(self, db: Session, *, id: int) -> UserRole:
        db_user_role = db.query(UserRole).get(id)
        db.delete(db_user_role)
        db.commit()
        return db_user_role

    def get_by_user_and_role(self, db: Session, user_id: int, role_id: int) -> Optional[UserRole]:
        return (
            db.query(UserRole)
            .filter(UserRole.user_id == user_id, UserRole.role_id == role_id)
            .first()
        )

    def get_by_user_id(self, db: Session, user_id: int) -> list[UserRole]:
        return db.query(UserRole).filter(UserRole.user_id == user_id).all()
