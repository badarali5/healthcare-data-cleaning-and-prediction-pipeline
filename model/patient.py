from typing import Optional

from sqlalchemy import Column, Integer, String, Float
from database import Base


class Patient(Base):
    __tablename__ = "patients"

    patient_id = Column(Integer, primary_key=True)

    patient_name = Column(String, nullable=True)
    age = Column(Integer, nullable=True)
    gender = Column(String, nullable=True)
    condition = Column(String, nullable=True)
    medication = Column(String, nullable=True)

    cholesterol = Column(Float, nullable=True)
    respiratory_rate = Column(Integer, nullable=True)
    oxygen_saturation = Column(Float, nullable=True)
    fasting_blood_sugar = Column(Float, nullable=True)
    hba1c = Column(Float, nullable=True)
    insulin_level = Column(Float, nullable=True)

    systolic_bp_reading = Column(Float, nullable=True)
    diastolic_bp_reading = Column(Float, nullable=True)

    wheezing_present = Column(String, nullable=True)
    chest_pain_type = Column(String, nullable=True)