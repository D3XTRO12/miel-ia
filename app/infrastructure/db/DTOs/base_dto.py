from pydantic import BaseModel
from uuid import UUID
from datetime import datetime

class BaseDTO(BaseModel):
    class Config:
        from_attributes = True
        json_encoders = {
            datetime: lambda v: v.isoformat(),
            UUID: lambda v: str(v)
        }