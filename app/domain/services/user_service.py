from app.infrastructure.repositories.user_repo import UserRepo
from app.infrastructure.db.db import Base

class UserService:
    def __init__(self):
        self.__user_repo = UserRepo()
    
    @cache.memoize(timeout=60)
    def find_all(self):
        try:
            users = self.__user_repo.find_all()
            return users if users else []
        except Exception as e:
            raise Exception(f"An error occurred while trying to retrieve all users: {str(e)}")
    
    def find_by_id(self, user_id: int):
        try:
            user = self.__user_repo.find_by_id(user_id)
            if not user:
                raise ValueError(f"User with ID {user_id} not found.")
            return user
        except Exception as e:
            raise Exception(f"An error occurred while trying to retrieve the user with ID {user_id}: {str(e)}")
    
    def find_by_name(self, name: str):
        try:
            user = self.__user_repo.find_by_name(name)
            if not user:
                raise ValueError(f"User with name {name} not found.")
            return user
        except Exception as e:
            raise Exception(f"An error occurred while trying to retrieve the user with name {name}: {str(e)}")
    
    def find_by_dni(self, dni: str):
        try:
            user = self.__user_repo.find_by_dni(dni)
            if not user:
                raise ValueError(f"User with DNI {dni} not found.")
            return user
        except Exception as e:
            raise Exception(f"An error occurred while trying to retrieve the user with DNI {dni}: {str(e)}")
    
    def create(self, item):
        try:
            user = self.__user_repo.create(item)
            return user
        except Exception as e:
            raise Exception(f"An error occurred while trying to create the user: {str(e)}")
    
    def update(self, item):
        try:
            user = self.__user_repo.update(item)
            return user
        except Exception as e:
            raise Exception(f"An error occurred while trying to update the user: {str(e)}")
    
    def delete(self, user_id: int):
        try:
            self.__user_repo.delete(user_id)
        except Exception as e:
            raise Exception(f"An error occurred while trying to delete the user with ID {user_id}: {str(e)}")