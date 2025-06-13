from ..models.role import Role
from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum
class RoleStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
class RoleBaseDTO(BaseModel):
    """Base DTO con campos comunes para roles"""
    name: str = Field(..., min_length=3, max_length=50, example="Admin")
    class Config:
        # Esta línea le permite al DTO ser creado desde un modelo de ORM
        from_attributes = True

class RoleResponseDTO(RoleBaseDTO):
    """DTO para respuesta de rol"""
    id: int = Field(..., example=1)
    name: str = Field(..., min_length=3, max_length=50, example="Admin")    
    class Config:
        orm_mode = True
