# app/services/auth_service.py
from datetime import timedelta
from jose import JWTError
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from ..core.security import create_access_token, decode_access_token, get_password_hash, verify_password
from ..core.config import settings
from ..infrastructure.repositories.user_repo import UserRepo
from ..infrastructure.db.DTOs.auth_schema import Token, UserLogin, UserOut
from ..core.db import get_db_session

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/auth/login")

class AuthService:
    def __init__(self, user_repo: UserRepo):
        self.__user_repo = user_repo

    def login(self, db: Session, user_login: UserLogin) -> Token:
        print(f"🔍 [DEBUG] Intentando login con email: {user_login.email}")
        
        # Verificar si el usuario existe
        user_by_email = self.__user_repo.get_by_email(db, email=user_login.email)
        print(f"🔍 [DEBUG] Usuario encontrado por email: {user_by_email is not None}")
        
        if user_by_email:
            print(f"🔍 [DEBUG] Usuario ID: {user_by_email.id}")
            print(f"🔍 [DEBUG] Hash almacenado: {user_by_email.password[:20]}...")
            
            # Verificar contraseña manualmente
            stored_hash = user_by_email.password
            input_password = user_login.password
            print(f"🔍 [DEBUG] Contraseña ingresada: {input_password}")
            print(f"🔍 [DEBUG] Hash almacenado: {stored_hash}")
            print(f"🔍 [DEBUG] Hash generado ahora: {get_password_hash(input_password)}")  # Añade esta línea
            password_valid = verify_password(input_password, stored_hash)
            print(f"🔍 [DEBUG] Contraseña válida: {password_valid}")
        
        # Usar el método authenticate que ya existe en UserRepo
        user = self.__user_repo.authenticate(db, email=user_login.email, password=user_login.password)
        print(f"🔍 [DEBUG] Resultado authenticate: {user is not None}")
        
        if not user:
            print(f"❌ [DEBUG] Fallo en autenticación")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        print(f"✅ [DEBUG] Login exitoso para usuario: {user.email}")
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user.email},
            expires_delta=access_token_expires
        )
        return Token(access_token=access_token, token_type="bearer")

    def get_current_user(self, db: Session, token: str = Depends(oauth2_scheme)) -> UserOut:
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            payload = decode_access_token(token)
            if payload is None:
                raise credentials_exception
            email: str = payload.get("sub")
            if email is None:
                raise credentials_exception
        except JWTError:
            raise credentials_exception
        
        user = self.__user_repo.get_by_email(db, email=email)
        if user is None:
            raise credentials_exception
        return user

def get_auth_service(db: Session = Depends(get_db_session)) -> AuthService:
    user_repo = UserRepo(db)  # Pasamos la sesión al constructor
    return AuthService(user_repo)