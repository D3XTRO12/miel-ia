from sqlalchemy.orm import Session
from typing import Dict, Any, List, Optional
from ..db.models.user import User
from ..repositories.base_repo import BaseRepository

# El DTO aquí no es estrictamente necesario si los servicios manejan la conversión,
# pero es bueno tenerlo para referencia.
from ..db.DTOs.user_dto import UserUpdateDTO

class UserRepo(BaseRepository[User]):
    def __init__(self):
        # Asignamos el modelo de SQLAlchemy con el que trabajará este repo
        self.model = User

    def get(self, db: Session, *, id: int) -> Optional[User]:
        """Obtiene un usuario por su ID."""
        return db.query(self.model).filter(self.model.id == id).first()

    def get_by_email(self, db: Session, *, email: str) -> Optional[User]:
        """Obtiene un usuario por su email."""
        return db.query(self.model).filter(self.model.email == email).first()

    def email_exists(self, db: Session, *, email: str) -> bool:
        """Verifica si un email ya está registrado."""
        return db.query(self.model).filter(self.model.email == email).first() is not None

    # --- MÉTODOS NUEVOS ---
    def get_all(self, db: Session, *, skip: int = 0, limit: int = 100) -> List[User]:
        """Obtiene una lista de todos los usuarios con paginación."""
        return db.query(self.model).offset(skip).limit(limit).all()

    def get_by_name(self, db: Session, *, name: str) -> List[User]:
        """Obtiene una lista de usuarios por coincidencia de nombre (no sensible a mayúsculas)."""
        return db.query(self.model).filter(self.model.name.ilike(f"%{name}%")).all()

    def get_by_dni(self, db: Session, *, dni: str) -> Optional[User]:
        """Obtiene un usuario por su DNI."""
        return db.query(self.model).filter(self.model.dni == dni).first()
    # --- FIN DE MÉTODOS NUEVOS ---

    def create(self, db: Session, *, obj_in: Dict[str, Any]) -> User:
        """Crea un objeto User. Asume que obj_in es un diccionario limpio."""
        db_obj = self.model(**obj_in)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    
    def update(self, db: Session, *, db_obj: User, obj_in: UserUpdateDTO | Dict[str, Any]) -> User:
        """Actualiza un usuario. db_obj es el objeto SQLAlchemy a actualizar."""
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.model_dump(exclude_unset=True)
        
        for field in update_data:
            if hasattr(db_obj, field):
                setattr(db_obj, field, update_data[field])
        
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def delete(self, db: Session, *, id: int) -> User:
        """Elimina un usuario por su ID."""
        user = db.query(self.model).get(id)
        if not user:
            # En un caso real, el servicio manejaría la excepción, pero es bueno tenerla.
            raise ValueError("Usuario no encontrado para eliminar")
        
        db.delete(user)
        db.commit()
        # El objeto 'user' todavía contiene los datos antes de ser eliminado, 
        # lo que puede ser útil para devolver un mensaje de confirmación.
        return user