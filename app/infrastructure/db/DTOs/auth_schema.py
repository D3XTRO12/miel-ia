from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional
from uuid import UUID

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserCreate(BaseModel):
    email: EmailStr = Field(..., example="user@example.com")
    password: str = Field(..., min_length=8, max_length=100, example="securepassword123")
    dni: str = Field(..., example="12345678A")
    name: str = Field(..., example="John")
    last_name: str = Field(..., example="Doe")
    role_id: UUID = Field(..., description="ID del rol asignado")

class UserOut(BaseModel):
    id: UUID
    email: EmailStr
    dni: str = Field(..., example="12345678A")
    first_name: str = Field(..., example="John")
    last_name: str = Field(..., example="Doe")
    is_active: bool = Field(default=True, description="Indica si el usuario está activo")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Fecha de creación del usuario")
    updated_at: datetime = Field(default_factory=datetime.utcnow, description="Fecha de actualización del usuario")

    class Config:
        from_attributes = True