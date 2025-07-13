from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum
from uuid import UUID
from .base_dto import BaseDTO

class RoleStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"

class RoleBaseDTO(BaseDTO):
    name: str = Field(..., min_length=3, max_length=50, example="Admin")

class RoleResponseDTO(RoleBaseDTO):
    id: UUID = Field(..., example="3fa85f64-5717-4562-b3fc-2c963f66afa6")
    name: str = Field(..., min_length=3, max_length=50, example="Admin")