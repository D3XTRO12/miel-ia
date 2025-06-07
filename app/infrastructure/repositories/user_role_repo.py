from .base_repo import Create, Read, Update, Delete
from app.infrastructure.db.builder.user_role_builder import UserRoleBuilder
from typing import List, Optional
from app.infrastructure.db.db import SessionLocal

class UserRoleRepo(Create, Read, Update, Delete):
    def __init__(self):
        self.session = SessionLocal()

    def create(self, item: UserRoleBuilder) -> UserRoleBuilder:
        """Crea un nuevo rol de usuario en la base de datos."""
        user_role = item.build()
        self.session.add(user_role)
        self.session.commit()
        self.session.refresh(user_role)
        return user_role

    def read(self, item_id: int) -> Optional[UserRoleBuilder]:
        """Lee un rol de usuario de la base de datos por su ID."""
        return self.session.query(UserRoleBuilder).filter(UserRoleBuilder.id == item_id).first()

    def update(self, item: UserRoleBuilder) -> UserRoleBuilder:
        """Actualiza un rol de usuario en la base de datos."""
        self.session.merge(item)
        self.session.commit()
        return item

    def delete(self, item_id: int) -> None:
        """Elimina un rol de usuario de la base de datos por su ID."""
        user_role = self.read(item_id)
        if user_role:
            self.session.delete(user_role)
            self.session.commit()