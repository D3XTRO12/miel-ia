from dataclasses import dataclass
from app.infrastructure.db.db import Base
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from datetime import datetime

@dataclass
class MedicalStudy(Base):
    __tablename__ = "medical_studies"
    
    id: int = Column(Integer, primary_key=True, index=True)
    access_code: str = Column(String(100), nullable=False, unique=True)
    clinical_data: str = Column(Text, nullable=True)
    creation_date: datetime = Column(DateTime, default=datetime.utcnow)
    ml_results: str = Column(Text, nullable=True)
    status: str = Column(String(50), default="PENDING")
    
    # Referencias a usuarios
    doctor_id: int = Column(Integer, ForeignKey("users.id"))
    patient_id: int = Column(Integer, ForeignKey("users.id"))
    technician_id: int = Column(Integer, ForeignKey("users.id"), nullable=True)
    
    # NUEVA: Referencia al archivo CSV
    csv_file_id: int = Column(Integer, ForeignKey("file_storage.id"), nullable=True)
    
    # Relaciones (opcional, pero útil para SQLAlchemy ORM)
    csv_file = relationship("FileStorage", foreign_keys=[csv_file_id])
    