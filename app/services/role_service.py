# services/role_service.py

from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from typing import List
from ..infrastructure.repositories.role_repo import RoleRepo
from ..infrastructure.db.DTOs.role_dto import RoleBaseDTO as RoleDTO
from ..infrastructure.db.models.role import Role

class RoleService:
    def __init__(self, role_repo: RoleRepo):
        self.__role_repo = role_repo

    def get_role(self, db: Session, role_id: int) -> RoleDTO:
        role: Role | None = self.__role_repo.get_by_id(db, id=role_id)
        if not role:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Role not found"
            )
        return RoleDTO.from_orm(role)

    def get_all_roles(self, db: Session) -> List[RoleDTO]:
        roles = self.__role_repo.get_all(db)
        return [RoleDTO.from_orm(role) for role in roles]
