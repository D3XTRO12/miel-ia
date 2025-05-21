from dataclasses import dataclass
from app import db
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text
from datetime import datetime

@dataclass
class MedicalStudy(db.Model):
    __tablename__ = "medical_studies"
    id: int = Column(Integer, primary_key=True, index=True)
    access_code: str = Column(String(100), nullable=False, unique=True)
    clinical_data: str = Column(Text, nullable=True)
    creation_date: datetime = Column(DateTime, default=datetime.utcnow)
    ml_results: str = Column(Text, nullable=True)
    status: str = Column(String(50), default="PENDING")
    doctor_id: int = Column(Integer, ForeignKey("users.id"))
    patient_id: int = Column(Integer, ForeignKey("users.id"))
    technician_id: int = Column(Integer, ForeignKey("users.id"))