from sqlalchemy.orm import Session
from ...infrastructure.db.models.role import Role
from ...infrastructure.db.DTOs.role_dto import RoleBaseDTO, RoleResponseDTO
from ...infrastructure.repositories.base_repo import BaseRepository
from typing import List
class RoleRepo(BaseRepository):
    def create(self, db: Session, obj_in):
        raise NotImplementedError("Role creation is not allowed")

    def update(self, db: Session, db_obj, obj_in):
        raise NotImplementedError("Role update is not allowed")

    def delete(self, db: Session, db_obj):
        raise NotImplementedError("Role deletion is not allowed")

    def get_by_id(self, db: Session, id: int):
        return db.query(Role).filter(Role.id == id).first()
    def get(self, db: Session) -> List[Role]:
        return db.query(Role).all()


    