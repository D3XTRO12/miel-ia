from pydantic import BaseModel, EmailStr, Field, ConfigDict, field_serializer
from datetime import datetime, timezone
from typing import Optional, List, Any
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
    model_config = ConfigDict(from_attributes=True)
    
    id: UUID
    email: EmailStr
    dni: str = Field(..., example="12345678A")
    name: str = Field(..., example="John")
    last_name: Optional[str] = Field(None, example="Doe")
    is_active: bool = Field(default=True, description="Indica si el usuario está activo")
    
    # Campos datetime opcionales
    created_at: Optional[datetime] = Field(default=None, description="Fecha de creación del usuario")
    updated_at: Optional[datetime] = Field(default=None, description="Fecha de actualización del usuario")
    
    # ✅ CRÍTICO: Cambiar roles para manejar objetos SQLAlchemy
    roles: Optional[List[Any]] = Field(default=[], description="Roles del usuario")
    
    @field_serializer('roles')
    def serialize_roles(self, roles: List[Any]) -> List[dict]:
        """
        Serializa los roles, manejando tanto objetos SQLAlchemy como diccionarios
        """
        if not roles:
            return []
        
        result = []
        for role in roles:
            if hasattr(role, '__dict__'):  # Es un objeto SQLAlchemy
                role_dict = {
                    'id': str(role.id) if hasattr(role, 'id') else None,
                    'name': role.name if hasattr(role, 'name') else None,
                    'description': role.description if hasattr(role, 'description') else None
                }
                result.append(role_dict)
            elif isinstance(role, dict):  # Ya es un diccionario
                result.append(role)
            else:  # Fallback
                result.append({'name': str(role)})
        
        return result