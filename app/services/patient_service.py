from fastapi import status

from app.schema.response import ResponseModel
from database import SessionLocal
from model.patient import Patient

response = ResponseModel(
    status_code=0,
    status="",
    message="",
    data=None
    )


def patient_data(patient: Patient):
    return {
        column.name: getattr(patient, column.name)
        for column in Patient.__table__.columns
    }


def get_all_patients():
    

    db = SessionLocal()

    try:
        patients = db.query(Patient).order_by(Patient.patient_id).all()

        response.status_code = status.HTTP_200_OK
        response.status = "success"
        response.message = "Patients retrieved successfully"
        response.data = [patient_data(patient) for patient in patients]

        return response

    except Exception as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        response.status = "error"
        response.message = str(e)
        response.data = None

        return response

    finally:
        db.close()

def get_patient(patient_id: int):
    

    db = SessionLocal()

    try:
        patient = db.get(Patient, patient_id)

        if patient is None:
            response.status_code = status.HTTP_404_NOT_FOUND
            response.status = "error"
            response.message = "Patient not found"
            response.data = None

            return response

        response.status_code = status.HTTP_200_OK
        response.status = "success"
        response.message = "Patient found successfully"
        response.data = patient_data(patient)

        return response

    except Exception as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        response.status = "error"
        response.message = str(e)
        response.data = None

        return response

    finally:
        db.close()

def create_patient(patient_values: dict):
    db = SessionLocal()

    try:
        patient_id = patient_values["patient_id"]
        existing_patient= db.get(Patient, patient_id)
        if  existing_patient is not None:
            response.status_code = status.HTTP_409_CONFLICT
            response.status = "error"
            response.message = "Patient ID already exists"
            response.data = patient_data(existing_patient)

            return response

        patient = Patient(**patient_values)

        db.add(patient)
        db.commit()
        db.refresh(patient)

        response.status_code = status.HTTP_201_CREATED
        response.status = "success"
        response.message = "Patient created successfully"
        response.data = patient_data(patient)

        return response

    except Exception as e:
        db.rollback()

        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        response.status = "error"
        response.message = str(e)
        response.data = None

        return response

    finally:
        db.close()
def update_patient(updated_patient: dict):

    db = SessionLocal()

    try:
        patient_id = updated_patient["patient_id"]

        patient = db.get(Patient, patient_id)

        if patient is None:
            response.status_code = status.HTTP_404_NOT_FOUND
            response.status = "error"
            response.message = "Patient not found"
            response.data = None

            return response

        for field, value in updated_patient.items():
            if field != "patient_id" and hasattr(patient, field):
                setattr(patient, field, value)

        db.commit()
        db.refresh(patient)

        response.status_code = status.HTTP_200_OK
        response.status = "success"
        response.message = "Patient updated successfully"
        response.data = patient_data(patient)

        return response

    except Exception as e:
        db.rollback()

        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        response.status = "error"
        response.message = str(e)
        response.data = None

        return response

    finally:
        db.close()

def delete_patient(patient_id: int):

    db = SessionLocal()

    try:
        patient = db.get(Patient, patient_id)

        if patient is None:
            response.status_code = status.HTTP_404_NOT_FOUND
            response.status = "error"
            response.message = "Patient not found"
            response.data = None

            return response

        deleted_patient = patient_data(patient)

        db.delete(patient)
        db.commit()

        response.status_code = status.HTTP_200_OK
        response.status = "success"
        response.message = "Patient deleted successfully"
        response.data = deleted_patient

        return response

    except Exception as e:
        db.rollback()

        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        response.status = "error"
        response.message = str(e)
        response.data = None

        return response

    finally:
        db.close()
