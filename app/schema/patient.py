from typing import Optional
from pydantic import BaseModel


class PatientBase(BaseModel):
    patient_id: int
    patient_name: Optional[str] = None
    age: Optional[int] = None
    gender: Optional[str] = None
    condition: Optional[str] = None
    medication: Optional[str] = None
    cholesterol: Optional[float] = None
    respiratory_rate: Optional[int] = None
    oxygen_saturation: Optional[float] = None
    fasting_blood_sugar: Optional[float] = None
    hba1c: Optional[float] = None
    insulin_level: Optional[float] = None
    systolic_bp_reading: Optional[float] = None
    diastolic_bp_reading: Optional[float] = None
    wheezing_present: Optional[str] = None
    chest_pain_type: Optional[str] = None


class PatientCreate(PatientBase):
    pass


class PatientUpdate(PatientBase):
    pass


class Patient(PatientBase):
    class Config:
        from_attributes = True    