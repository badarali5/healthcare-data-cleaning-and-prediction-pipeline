from sqlalchemy.orm import Session

from app.schema.response import ResponseModel
from model.patient import Patient


def patient_data(patient: Patient):
    return {
        column.name: getattr(patient, column.name)
        for column in Patient.__table__.columns
    }


def get_all_patients(db: Session):
    try:
        patients = db.query(Patient).order_by(Patient.patient_id).all()

        return ResponseModel.success(
            "Patients retrieved successfully",[patient_data(patient) for patient in patients]
        )

    except Exception as e:
        return ResponseModel.error(
            500,
            str(e)
        )


def get_patient(patient_id: int, db: Session):
    try:
        patient = db.get(Patient, patient_id)

        if patient is None:
            return ResponseModel.error(
                404,
                "Patient not found"
            )

        return ResponseModel.success(
            "Patient found successfully",
            patient_data(patient)
        )

    except Exception as e:
        return ResponseModel.error(
            500,
            str(e)
        )


def create_patient(patient_values: dict, db: Session):
    try:
        patient_id = patient_values["patient_id"]

        existing_patient = db.get(Patient, patient_id)

        if existing_patient is not None:
            return ResponseModel.error(
                409,
                "Patient ID already exists",
                patient_data(existing_patient)
            )

        patient = Patient(**patient_values)

        db.add(patient)
        db.commit()
        db.refresh(patient)

        return ResponseModel.created(
            "Patient created successfully",
            patient_data(patient)
        )

    except Exception as e:
        db.rollback()

        return ResponseModel.error(
            500,
            str(e)
        )


def update_patient(updated_patient: dict, db: Session):
    try:
        patient_id = updated_patient["patient_id"]

        patient = db.get(Patient, patient_id)

        if patient is None:
            return ResponseModel.error(
                404,
                "Patient not found"
            )

        for field, value in updated_patient.items():
            if field != "patient_id" and hasattr(patient, field):
                setattr(patient, field, value)

        db.commit()
        db.refresh(patient)

        return ResponseModel.success(
            "Patient updated successfully",
            patient_data(patient)
        )

    except Exception as e:
        db.rollback()

        return ResponseModel.error(
            500,
            str(e)
        )


def delete_patient(patient_id: int, db: Session):
    try:
        patient = db.get(Patient, patient_id)

        if patient is None:
            return ResponseModel.error(
                404,
                "Patient not found"
            )

        deleted_patient = patient_data(patient)

        db.delete(patient)
        db.commit()

        return ResponseModel.success(
            "Patient deleted successfully",
            deleted_patient
        )

    except Exception as e:
        db.rollback()

        return ResponseModel.error(
            500,
            str(e)
        )