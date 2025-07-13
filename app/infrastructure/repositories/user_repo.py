from sqlalchemy.orm import Session
from typing import Dict, Any, List, Optional
from ..db.models.user import User
from ..repositories.base_repo import BaseRepository
from ...core.security import get_password_hash, verify_password

# DTOs
from ..db.DTOs.user_dto import UserUpdateDTO, UserCreateDTO

class UserRepo(BaseRepository[User]):
    def __init__(self, db: Session = None):
          # Ahora es opcional
        super().__init__(User, db)
    # Métodos existentes (se mantienen igual)
    def get(self, db: Session, *, id: int) -> Optional[User]:
        return db.query(self.model).filter(self.model.id == id).first()

    def get_by_email(self, db: Session, *, email: str) -> Optional[User]:
        return db.query(self.model).filter(self.model.email == email).first()

    def email_exists(self, db: Session, *, email: str) -> bool:
        return db.query(self.model).filter(self.model.email == email).first() is not None

    def get_all(self, db: Session, *, skip: int = 0, limit: int = 100) -> List[User]:
        return db.query(self.model).offset(skip).limit(limit).all()

    def get_by_name(self, db: Session, *, name: str) -> List[User]:
        return db.query(self.model).filter(self.model.name.ilike(f"%{name}%")).all()

    def get_by_dni(self, db: Session, *, dni: str) -> Optional[User]:
        return db.query(self.model).filter(self.model.dni == dni).first()

    # Método create actualizado para hashear la contraseña
    def create(self, db: Session, *, obj_in: UserCreateDTO | Dict[str, Any]) -> User:
        if isinstance(obj_in, dict):
            create_data = obj_in
        else:
            create_data = obj_in.model_dump(exclude_unset=True)
        
        # Hashear la contraseña antes de guardarla
        if 'password' in create_data:
            create_data['password'] = get_password_hash(create_data['password'])

        db_obj = self.model(**create_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        print(f"🔍 [DEBUG] Contraseña original: {create_data['password']}")
        print(f"🔍 [DEBUG] Hash generado: {create_data['password']}")  # Debería mostrar el hash
        return db_obj

    # Método update actualizado para manejar contraseñas
    def update(self, db: Session, *, db_obj: User, obj_in: UserUpdateDTO | Dict[str, Any]) -> User:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.model_dump(exclude_unset=True)
        
        # Si se actualiza la contraseña, la hasheamos
        if 'password' in update_data:
            update_data['password'] = get_password_hash(update_data['password'])
        
        for field in update_data:
            if hasattr(db_obj, field):
                setattr(db_obj, field, update_data[field])
        
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    # Método delete se mantiene igual
    def delete(self, db: Session, *, id: int) -> User:
        user = db.query(self.model).get(id)
        if not user:
            raise ValueError("Usuario no encontrado para eliminar")
        
        db.delete(user)
        db.commit()
        return user

    # Nuevo método para autenticación
    def authenticate(self, db: Session, *, email: str, password: str) -> Optional[User]:
        user = self.get_by_email(db, email=email)
        if not user:
            return None
        # Añade logs para depuración
        print(f"🔍 [REPO DEBUG] Contraseña ingresada: {password}")
        print(f"🔍 [REPO DEBUG] Hash almacenado: {user.password}")
        if not verify_password(password, user.password):  # <- Asegúrate de pasar la contraseña plana
            return None
        return user