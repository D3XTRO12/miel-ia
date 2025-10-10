import uuid  # ← AÑADIR ESTO
from sqlalchemy import Column, String, ForeignKey, Text, CHAR
from sqlalchemy.dialects.postgresql import UUID
from .base_model import BaseModel
from sqlalchemy.orm import relationship

class MedicalStudy(BaseModel):
    __tablename__ = "medical_studies"
    
    access_code = Column(String(100), nullable=False, unique=True, index=True)
    clinical_data = Column(Text, nullable=True)
    ml_results = Column(Text, nullable=True)
    status = Column(String(50), default="PENDING")
    
    doctor_id = Column(CHAR(36, collation='ascii_bin'), ForeignKey("users.id"))  
    patient_id = Column(CHAR(36, collation='ascii_bin'), ForeignKey("users.id"))   
    technician_id = Column(CHAR(36, collation='ascii_bin'), ForeignKey("users.id"), nullable=True)  
    csv_file_id = Column(CHAR(36, collation='ascii_bin'), ForeignKey("file_storage.id"), nullable=True)  
    
    doctor = relationship("User", foreign_keys=[doctor_id])
    patient = relationship("User", foreign_keys=[patient_id])
    technician = relationship("User", foreign_keys=[technician_id])
    csv_file = relationship("FileStorage", foreign_keys=[csv_file_id])