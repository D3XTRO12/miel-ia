from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from uuid import UUID
from .base_dto import BaseDTO

class UserRoleBaseDTO(BaseDTO):
    role_id: UUID = Field(..., description="ID del rol")
    user_id: UUID = Field(..., description="ID del usuario")

class UserRoleCreateDTO(UserRoleBaseDTO):
    pass

class UserRoleUpdateDTO(BaseDTO):
    role_id: Optional[UUID] = None
    user_id: Optional[UUID] = None

class UserRoleResponseDTO(UserRoleBaseDTO):
    id: UUID
    role_id: UUID
    
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None