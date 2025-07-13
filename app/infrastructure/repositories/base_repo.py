from abc import ABC, abstractmethod
from typing import Generic, TypeVar, Any, Type
from sqlalchemy.orm import Session

T = TypeVar("T")

class BaseRepository(ABC, Generic[T]):
    """Interfaz base para repositorios de datos.
    Define las operaciones CRUD básicas que deben implementarse.
    """

    def __init__(self, model: Type[T], db: Session = None):
        self.model = model
        self._db = db  # Usamos _db para indicar que es interno
    
    @property
    def db(self) -> Session:
        if self._db is None:
            raise ValueError("Sesión de DB no configurada")
        return self._db
    
    @db.setter
    def db(self, session: Session):
        self._db = session
    @abstractmethod
    def get(self, db: Session, id: Any) -> T | None:
        pass

    @abstractmethod
    def create(self, db: Session, *, obj_in: Any) -> T:
        pass

    # @abstractmethod
    # def update(self, db: Session, *, db_obj: T, obj_in: Any) -> T:
    #     pass

    # @abstractmethod
    # def delete(self, db: Session, *, id: Any) -> T:
    #     pass