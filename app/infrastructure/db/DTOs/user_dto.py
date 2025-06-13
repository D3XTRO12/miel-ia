from datetime import datetime
from enum import Enum
from typing import Optional, List
from pydantic import BaseModel, EmailStr, Field, field_validator
from .role_dto import RoleBaseDTO as RoleDTO

class UserStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    SUSPENDED = "suspended"
    PENDING = "pending"

class UserBaseDTO(BaseModel):
    """Base DTO con campos comunes"""
    name: str = Field(..., min_length=3, max_length=50, example="johndoe")
    email: EmailStr = Field(..., example="user@example.com")

class UserCreateDTO(UserBaseDTO):
    """DTO para creación de usuario"""
    password: str = Field(..., min_length=8, max_length=100, example="securepassword123")
    dni: str = Field(..., min_length=8, max_length=20, example="12345678A")
    last_name: Optional[str] = Field(None, max_length=100, example="Doe")
    role_id: int = Field(..., gt=0, description="ID del rol asignado")  # Hacerlo requerido

    @field_validator('name')  # Cambiado de 'username' a 'name'
    @classmethod
    def name_alphanumeric(cls, v):
        if not v.isalnum():
            raise ValueError('El nombre debe ser alfanumérico')
        return v

    @field_validator('password')
    @classmethod
    def password_complexity(cls, v):
        if len(v) < 8:
            raise ValueError('La contraseña debe tener al menos 8 caracteres')
        return v



class UserUpdateDTO(BaseModel):
    """DTO para actualización de usuario"""
    username: Optional[str] = Field(None, min_length=3, max_length=50)
    email: Optional[EmailStr] = Field(None)
    password: Optional[str] = Field(None, min_length=8, max_length=100)
    dni: Optional[str] = Field(None, min_length=8, max_length=20)
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    last_name: Optional[str] = Field(None, max_length=100)
    role_id: Optional[int] = Field(None, gt=0)

class UserResponseDTO(UserBaseDTO):
    """DTO para respuesta de usuario"""
    id: int
    dni: str
    name: str
    last_name: Optional[str]

    roles: List[RoleDTO] = Field(default_factory=list)

    class Config:
        orm_mode = True
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

class UserLoginDTO(BaseModel):
    """DTO para autenticación"""
    username: str = Field(..., example="johndoe")
    password: str = Field(..., example="securepassword123")

class UserPasswordResetDTO(BaseModel):
    """DTO para resetear contraseña"""
    new_password: str = Field(..., min_length=8, max_length=100)
    token: str = Field(..., description="Token de verificación")

class UserMinimalResponseDTO(BaseModel):
    """DTO para respuestas mínimas de usuario"""
    id: int
    username: str
    email: str

    class Config:
        orm_mode = True

class UserCreateInternal(BaseModel):
    name: str
    last_name: str
    email: EmailStr
    dni: str
    password: str

    # Esta configuración ayuda a Pydantic a ser compatible con objetos de SQLAlchemy
    class Config:
        from_attributes = True
