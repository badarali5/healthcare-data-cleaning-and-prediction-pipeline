from fastapi import status
from sqlalchemy.exc import SQLAlchemyError

from app.schema.response import ResponseModel
from database import SessionLocal
from model.patient import Patient


def _response(status_code: int, response_status: str, message: str, data=None):
    return ResponseModel(
        status_code=status_code,
        status=response_status,
        message=message,
        data=data,
    )


def _patient_data(patient: Patient):
    return {
        column.name: getattr(patient, column.name)
        for column in Patient.__table__.columns
    }


def get_all_patients():
    db = SessionLocal()
    try:
        patients = db.query(Patient).order_by(Patient.patient_id).all()
        return _response(
            status.HTTP_200_OK,
            "success",
            "Patients retrieved successfully",
            [_patient_data(patient) for patient in patients],
        )
    except SQLAlchemyError as error:
        return _response(status.HTTP_500_INTERNAL_SERVER_ERROR, "error", str(error))
    finally:
        db.close()


def get_patient(patient_id: int):
    db = SessionLocal()
    try:
        patient = db.get(Patient, patient_id)
        if patient is None:
            return _response(status.HTTP_404_NOT_FOUND, "error", "Patient not found")
        return _response(
            status.HTTP_200_OK,
            "success",
            "Patient retrieved successfully",
            _patient_data(patient),
        )
    except SQLAlchemyError as error:
        return _response(status.HTTP_500_INTERNAL_SERVER_ERROR, "error", str(error))
    finally:
        db.close()


def create_patient(patient_data: dict):
    db = SessionLocal()
    try:
        patient_id = patient_data["patient_id"]
        if db.get(Patient, patient_id) is not None:
            return _response(
                status.HTTP_409_CONFLICT,
                "error",
                "Patient ID already exists",
            )

        patient = Patient(**patient_data)
        db.add(patient)
        db.commit()
        db.refresh(patient)
        return _response(
            status.HTTP_201_CREATED,
            "success",
            "Patient created successfully",
            _patient_data(patient),
        )
    except (KeyError, TypeError, SQLAlchemyError) as error:
        db.rollback()
        return _response(status.HTTP_500_INTERNAL_SERVER_ERROR, "error", str(error))
    finally:
        db.close()


def update_patient(updated_patient: dict):
    db = SessionLocal()
    try:
        patient_id = updated_patient["patient_id"]
        patient = db.get(Patient, patient_id)
        if patient is None:
            return _response(status.HTTP_404_NOT_FOUND, "error", "Patient not found")

        for field, value in updated_patient.items():
            if field != "patient_id" and hasattr(patient, field):
                setattr(patient, field, value)

        db.commit()
        db.refresh(patient)
        return _response(
            status.HTTP_200_OK,
            "success",
            "Patient updated successfully",
            _patient_data(patient),
        )
    except (KeyError, TypeError, SQLAlchemyError) as error:
        db.rollback()
        return _response(status.HTTP_500_INTERNAL_SERVER_ERROR, "error", str(error))
    finally:
        db.close()


def delete_patient(patient_id: int):
    db = SessionLocal()
    try:
        patient = db.get(Patient, patient_id)
        if patient is None:
            return _response(status.HTTP_404_NOT_FOUND, "error", "Patient not found")

        deleted_patient = _patient_data(patient)
        db.delete(patient)
        db.commit()
        return _response(
            status.HTTP_200_OK,
            "success",
            "Patient deleted successfully",
            deleted_patient,
        )
    except SQLAlchemyError as error:
        db.rollback()
        return _response(status.HTTP_500_INTERNAL_SERVER_ERROR, "error", str(error))
    finally:
        db.close()