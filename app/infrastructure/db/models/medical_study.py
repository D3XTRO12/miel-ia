from ....core.db import Base
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

class MedicalStudy(Base):
    __tablename__ = "medical_studies"
    
    id = Column(Integer, primary_key=True, index=True)
    access_code = Column(String(100), nullable=False, unique=True, index=True)
    clinical_data = Column(Text, nullable=True)
    creation_date = Column(DateTime(timezone=True), server_default=func.now())
    ml_results = Column(Text, nullable=True)
    status = Column(String(50), default="PENDING")
    
    # Referencias a usuarios
    doctor_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    patient_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    technician_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    
    # Referencia al archivo CSV (se añadirá en el endpoint de diagnóstico)
    csv_file_id = Column(Integer, ForeignKey("file_storage.id"), nullable=True)
    
    # Relaciones para que SQLAlchemy pueda hacer joins
    doctor = relationship("User", foreign_keys=[doctor_id])
    patient = relationship("User", foreign_keys=[patient_id])
    technician = relationship("User", foreign_keys=[technician_id])
    csv_file = relationship("FileStorage", foreign_keys=[csv_file_id])