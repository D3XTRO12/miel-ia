# user_role_dto.py
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class UserRoleBaseDTO(BaseModel):
    role_id: int = Field(..., gt=0, description="ID del rol")
    user_id: int = Field(..., gt=0, description="ID del usuario")
    class Config:
        from_attributes = True

class UserRoleCreateDTO(UserRoleBaseDTO):
    """DTO para creación de UserRole"""
    pass

class UserRoleUpdateDTO(BaseModel):
    """DTO para actualización de UserRole"""
    role_id: Optional[int] = Field(None, gt=0)
    user_id: Optional[int] = Field(None, gt=0)

class UserRoleResponseDTO(UserRoleBaseDTO):
    """DTO para respuesta de UserRole"""
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }
