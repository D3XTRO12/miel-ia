from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class FileStorageBaseDTO(BaseModel):
    """
    DTO base con los campos comunes que definen un registro de archivo.
    """
    filename: str = Field(..., description="El nombre con el que se guarda el archivo (puede ser personalizado).")
    original_filename: str = Field(..., description="El nombre original del archivo subido por el usuario.")
    file_type: Optional[str] = Field(None, description="El tipo MIME del archivo (ej. 'text/csv').")
    file_size: Optional[int] = Field(None, description="El tamaño del archivo en bytes.")
    description: Optional[str] = Field(None, description="Una descripción opcional del contenido del archivo.")
    user_id: Optional[str] = Field(None, description="El ID del usuario que subió el archivo.")


class FileStorageResponseDTO(FileStorageBaseDTO):
    """
    DTO para las respuestas de la API.
    Expone los metadatos de un archivo, pero nunca su contenido binario.
    Este es el 'contrato' público de cómo se ve un archivo en tu sistema.
    """
    id: int = Field(..., description="El identificador único del registro del archivo.")
    created_at: datetime = Field(..., description="La fecha y hora en que el archivo fue creado.")

    class Config:
        # Esencial para que Pydantic pueda crear este DTO
        # a partir de un objeto de modelo de SQLAlchemy (modo ORM).
        from_attributes = True
