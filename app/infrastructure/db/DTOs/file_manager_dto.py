from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from uuid import UUID
from .base_dto import BaseDTO

class FileStorageBaseDTO(BaseDTO):
    
    filename: str = Field(..., description="El nombre con el que se guarda el archivo")
    original_filename: str = Field(..., description="El nombre original del archivo")
    file_type: Optional[str] = Field(None, description="El tipo MIME del archivo")
    file_size: Optional[int] = Field(None, description="El tamaño del archivo en bytes")
    description: Optional[str] = Field(None, description="Descripción opcional")
    user_id: Optional[UUID] = Field(None, description="ID del usuario que subió el archivo")

class FileStorageResponseDTO(FileStorageBaseDTO):
    id: UUID = Field(..., description="El identificador único del archivo")
    created_at: datetime = Field(..., description="Fecha y hora de creación")