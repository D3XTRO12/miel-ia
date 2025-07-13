from sqlalchemy import Column, String, ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID
from .base_model import BaseModel
from sqlalchemy.orm import relationship


class MedicalStudy(BaseModel):
    __tablename__ = "medical_studies"
    """Tabla para almacenar estudios médicos realizados por los usuarios"""
    
    access_code = Column(String(100), nullable=False, unique=True, index=True)
    clinical_data = Column(Text, nullable=True)
    ml_results = Column(Text, nullable=True)
    status = Column(String(50), default="PENDING")
    
    # Referencias a usuarios (ahora con UUID)
    doctor_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    patient_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    technician_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    csv_file_id = Column(UUID(as_uuid=True), ForeignKey("file_storage.id"), nullable=True)
    
    # Relaciones
    doctor = relationship("User", foreign_keys=[doctor_id])
    patient = relationship("User", foreign_keys=[patient_id])
    technician = relationship("User", foreign_keys=[technician_id])
    csv_file = relationship("FileStorage", foreign_keys=[csv_file_id])