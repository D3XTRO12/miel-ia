from .base_repo import Create, Read, Update, Delete
from app.infrastructure.db.builder.role_builder import RoleBuilder
from typing import List, Optional
from app.infrastructure.db.db import SessionLocal

class RoleRepo(Create, Read, Update, Delete):
    def __init__(self):
        self.session = SessionLocal()

    def create(self, item: RoleBuilder) -> RoleBuilder:
        """Crea un nuevo rol en la base de datos."""
        role = item.build()
        self.session.add(role)
        self.session.commit()
        self.session.refresh(role)
        return role

    def read(self, item_id: int) -> Optional[RoleBuilder]:
        """Lee un rol de la base de datos por su ID."""
        return self.session.query(RoleBuilder).filter(RoleBuilder.id == item_id).first()

    def update(self, item: RoleBuilder) -> RoleBuilder:
        """Actualiza un rol en la base de datos."""
        self.session.merge(item)
        self.session.commit()
        return item

    def delete(self, item_id: int) -> None:
        """Elimina un rol de la base de datos por su ID."""
        role = self.read(item_id)
        if role:
            self.session.delete(role)
            self.session.commit()
        