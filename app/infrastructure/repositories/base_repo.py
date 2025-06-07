from abc import ABC, abstractmethod
from typing import TypeVar
from sqlalchemy.ext.declarative import DeclarativeMeta

# Usar DeclarativeMeta como bound, que es el tipo real de las clases que heredan de Base
T = TypeVar('T', bound=DeclarativeMeta)

class Create(ABC):
    @abstractmethod
    def create(self, item: T) -> T:
        """Crea un nuevo registro en la base de datos."""
        pass

class Read(ABC):
    @abstractmethod
    def read(self, item_id: int) -> T:
        """Lee un registro de la base de datos por su ID."""
        pass

class Update(ABC):
    @abstractmethod
    def update(self, item: T) -> T:
        """Actualiza un registro en la base de datos."""
        pass

class Delete(ABC):
    @abstractmethod
    def delete(self, item_id: int) -> None:
        """Elimina un registro de la base de datos por su ID."""
        pass