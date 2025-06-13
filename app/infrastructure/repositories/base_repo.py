from abc import ABC, abstractmethod
from typing import Generic, TypeVar, Any
from sqlalchemy.orm import Session

T = TypeVar("T")

class BaseRepository(ABC, Generic[T]):
    """Interfaz base para repositorios de datos.
    Define las operaciones CRUD básicas que deben implementarse.
    """
    @abstractmethod
    def get(self, db: Session, id: Any) -> T | None:
        pass

    @abstractmethod
    def create(self, db: Session, *, obj_in: Any) -> T:
        pass

    @abstractmethod
    def update(self, db: Session, *, db_obj: T, obj_in: Any) -> T:
        pass

    @abstractmethod
    def delete(self, db: Session, *, id: Any) -> T:
        pass