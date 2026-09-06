from fastapi import APIRouter
from fastapi.responses import JSONResponse

from app.schema.patient import PatientCreate, PatientUpdate
from app.schema.response import ResponseModel

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
def get_patients():

    response = get_all_patients()

    return JSONResponse(
        status_code=response.status_code,
        content=response.model_dump()
    )


@router.get("/{patient_id}", response_model=ResponseModel)
def get_patient_by_id(patient_id: int):

    response = get_patient(patient_id)

    return JSONResponse(
        status_code=response.status_code,
        content=response.model_dump()
    )


@router.post("/", response_model=ResponseModel)
def create_new_patient(patient: PatientCreate):

    response = create_patient(patient.model_dump())

    return JSONResponse(
        status_code=response.status_code,
        content=response.model_dump()
    )


@router.put("/", response_model=ResponseModel)
def update_existing_patient(patient: PatientUpdate):

    response = update_patient(patient.model_dump())

    return JSONResponse(
        status_code=response.status_code,
        content=response.model_dump()
    )


@router.delete("/{patient_id}", response_model=ResponseModel)
def delete_existing_patient(patient_id: int):

    response = delete_patient(patient_id)

    return JSONResponse(
        status_code=response.status_code,
        content=response.model_dump()
    )