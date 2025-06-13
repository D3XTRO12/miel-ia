from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

# DTO para crear un nuevo estudio. Estos son los campos que el secretario llenará.
class MedicalStudyCreateDTO(BaseModel):
    access_code: str = Field(..., description="Código de acceso único para el estudio.")
    doctor_id: int = Field(..., description="ID del médico solicitante.")
    patient_id: int = Field(..., description="ID del paciente.")
    technician_id: Optional[int] = Field(None, description="ID del técnico (opcional).")
    clinical_data: Optional[str] = Field(None, description="Datos clínicos iniciales.")

# DTO para actualizar un estudio. Todos los campos son opcionales.
class MedicalStudyUpdateDTO(BaseModel):
    access_code: Optional[str] = None
    doctor_id: Optional[int] = None
    patient_id: Optional[int] = None
    technician_id: Optional[int] = None
    clinical_data: Optional[str] = None
    status: Optional[str] = None
    ml_results: Optional[str] = None # El endpoint de diagnóstico usará esto
    csv_file_id: Optional[int] = None # El endpoint de diagnóstico usará esto

# DTO para las respuestas de la API. Incluye campos generados por la BD.
class MedicalStudyResponseDTO(BaseModel):
    id: int
    access_code: str
    status: str
    creation_date: datetime
    doctor_id: int
    patient_id: int
    technician_id: Optional[int]
    clinical_data: Optional[str]
    ml_results: Optional[str]
    
    class Config:
        from_attributes = True # Permite la creación desde objetos ORM