from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from app.schema.patient import PatientCreate, PatientUpdate
from app.schema.response import ResponseModel
from database import get_db

from app.services.patient_service import (
    get_all_patients,
    get_patient,
    create_patient,
    update_patient,
    delete_patient
)


router = APIRouter(
    prefix="/patients",
    tags=["Patients"]
)


@router.get("/", response_model=ResponseModel)
def get_patients(db: Session = Depends(get_db)):

    response = get_all_patients(db)

    return JSONResponse(
        status_code=response.status_code,
        content=response.model_dump()
    )


@router.get("/{patient_id}", response_model=ResponseModel)
def get_patient_by_id(patient_id: int, db: Session = Depends(get_db)):

    response = get_patient(patient_id, db)

    return JSONResponse(
        status_code=response.status_code,
        content=response.model_dump()
    )


@router.post("/", response_model=ResponseModel)
def create_new_patient(patient: PatientCreate, db: Session = Depends(get_db)):

    response = create_patient(patient.model_dump(), db)

    return JSONResponse(
        status_code=response.status_code,
        content=response.model_dump()
    )


@router.put("/", response_model=ResponseModel)
def update_existing_patient(patient: PatientUpdate, db: Session = Depends(get_db)):

    response = update_patient(patient.model_dump(), db)

    return JSONResponse(
        status_code=response.status_code,
        content=response.model_dump()
    )


@router.delete("/{patient_id}", response_model=ResponseModel)
def delete_existing_patient(patient_id: int, db: Session = Depends(get_db)):

    response = delete_patient(patient_id, db)

    return JSONResponse(
        status_code=response.status_code,
        content=response.model_dump()
    )