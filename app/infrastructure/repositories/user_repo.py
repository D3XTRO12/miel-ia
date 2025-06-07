
from .base_repo import Create, Read, Update, Delete
from app.infrastructure.db.builder.user_builder import UserBuilder
from app.infrastructure.db.dataclass.user import User
from typing import List, Optional
from app.infrastructure.db.db import SessionLocal
from sqlalchemy.orm import Session

class UserRepo(Create, Read, Update, Delete):
    def __init__(self):
        self.session: Session = SessionLocal()
        self.__model = User  # El modelo, no el builder
        self.builder = UserBuilder()  # El builder como herramienta separada
    
    def find_all(self) -> List[User]:
        """nos traerá todos los usuarios"""
        try:
            users = self.session.query(self.__model).all()
            return users
        except Exception as e:
            # Rollback en caso de error
            self.session.rollback()
            raise Exception(f"An error occurred while trying to retrieve the users: {str(e)}")
    
    def find_by_id(self, user_id: int) -> Optional[User]:
        """Obtiene un usuario por su ID."""
        try:
            user = self.session.query(self.__model).filter(self.__model.id == user_id).first()
            return user
        except Exception as e:
            self.session.rollback()
            raise Exception(f"An error occurred while trying to retrieve the user with ID {user_id}: {str(e)}")
    
    def find_by_name(self, name: str) -> Optional[User]:
        """Obtiene un usuario por su nombre."""
        try:
            user = self.session.query(self.__model).filter(self.__model.name == name).first()
            return user
        except Exception as e:
            self.session.rollback()
            raise Exception(f"An error occurred while trying to retrieve the user with name {name}: {str(e)}")
    
    def find_by_dni(self, dni: str) -> Optional[User]:
        """Obtiene un usuario por su DNI."""
        try:
            user = self.session.query(self.__model).filter(self.__model.dni == dni).first()
            return user
        except Exception as e:
            self.session.rollback()
            raise Exception(f"An error occurred while trying to retrieve the user with DNI {dni}: {str(e)}")
    
    def create(self, item: UserBuilder) -> User:
        """Crea un nuevo usuario."""
        try:
            user = item.build()
            self.session.add(user)
            self.session.commit()
            self.session.refresh(user)
            return user
        except Exception as e:
            # Rollback en caso de error
            self.session.rollback()
            raise Exception(f"An error occurred while trying to create the user: {str(e)}")
    
    def update(self, item: UserBuilder) -> User:
        """Actualiza un usuario existente."""
        try:
            user = item.build()
            self.session.merge(user)
            self.session.commit()
            return user
        except Exception as e:
            # Rollback en caso de error
            self.session.rollback()
            raise Exception(f"An error occurred while trying to update the user: {str(e)}")
    
    def delete(self, user_id: int) -> None:
        """Elimina un usuario por su ID."""
        try:
            user = self.find_by_id(user_id)
            if user:
                self.session.delete(user)
                self.session.commit()
            else:
                raise Exception(f"User with ID {user_id} does not exist.")
        except Exception as e:
            # Rollback en caso de error
            self.session.rollback()
            raise Exception(f"An error occurred while trying to delete the user with ID {user_id}: {str(e)}")