import pandas as pd
from sqlalchemy.orm import Session

from app.schema.response import ResponseModel
from model.patient import Patient
from training.predict import load_artifacts, predict_new


PREDICTION_COLUMN_ALIASES = {
    "age": "Age",
    "gender": "Gender",
    "medication": "Medication",
    "cholesterol": "Cholesterol",
    "respiratory_rate": "Respiratory_Rate",
    "oxygen_saturation": "Oxygen_Saturation",
    "peak_expiratory_flow": "Peak_Expiratory_Flow",
    "resting_heart_rate": "Resting_Heart_Rate",
    "troponin_level": "Troponin_Level",
    "max_heart_rate_achieved": "Max_Heart_Rate_Achieved",
    "fasting_blood_sugar": "Fasting_Blood_Sugar",
    "hba1c": "HbA1c",
    "insulin_level": "Insulin_Level",
    "systolic_bp_reading": "Systolic_BP_Reading",
    "diastolic_bp_reading": "Diastolic_BP_Reading",
    "sodium_level": "Sodium_Level",
    "wheezing_present": "Wheezing_Present",
    "chest_pain_type": "Chest_Pain_Type",
}


def predict_patient(patient_values: dict):
    try:
        prediction_values = {
            PREDICTION_COLUMN_ALIASES.get(field, field): value
            for field, value in patient_values.items()
        }

        model, scaler, target_encoder, feature_columns = load_artifacts()
        required_columns = {
            column.rsplit("_", 1)[0]
            for column in feature_columns
            if column.endswith("_Yes") or column.endswith("_No")
        }
        required_columns.update(
            column for column in feature_columns if column not in required_columns
        )
        required_columns.update({"Gender", "Medication"})

        missing_columns = sorted(
            column for column in required_columns if column not in prediction_values
        )
        if missing_columns:
            return ResponseModel(
                status_code=400,
                status="error",
                message=f"Missing prediction fields: {', '.join(missing_columns)}",
                data=None,
            )

        labels, probabilities = predict_new(
            pd.DataFrame([prediction_values]),
            model,
            scaler,
            target_encoder,
            feature_columns,
        )

        prediction = {"condition": str(labels[0])}
        if probabilities is not None:
            prediction["probabilities"] = {
                str(condition): float(probability)
                for condition, probability in probabilities.iloc[0].items()
            }

        return ResponseModel(
            status_code=200,
            status="success",
            message="Patient condition predicted successfully",
            data=prediction,
        )

    except Exception as e:
        return ResponseModel(
            status_code=500,
            status="error",
            message=str(e),
            data=None,
        )


def patient_data(patient: Patient):
    return {
        column.name: getattr(patient, column.name)
        for column in Patient.__table__.columns
    }


def get_all_patients(db: Session):
    try:
        patients = db.query(Patient).order_by(Patient.patient_id).all()

        response = ResponseModel(
            status_code=200,
            status="success",
            message="Patients retrieved successfully",
            data=[patient_data(patient) for patient in patients]
        )

        return response

    except Exception as e:
        response = ResponseModel(
            status_code=500,
            status="error",
            message=str(e),
            data=None
        )

        return response


def get_patient(patient_id: int, db: Session):
    try:
        patient = db.get(Patient, patient_id)

        if patient is None:
            response = ResponseModel(
                status_code=404,
                status="error",
                message="Patient not found",
                data=None
            )
            return response

        response = ResponseModel(
            status_code=200,
            status="success",
            message="Patient found successfully",
            data=patient_data(patient)
        )

        return response

    except Exception as e:
        response = ResponseModel(
            status_code=500,
            status="error",
            message=str(e),
            data=None
        )

        return response


def create_patient(patient_values: dict, db: Session):
    try:
        patient_id = patient_values["patient_id"]

        existing_patient = db.get(Patient, patient_id)

        if existing_patient is not None:
            response = ResponseModel(
                status_code=409,
                status="error",
                message="Patient ID already exists",
                data=patient_data(existing_patient)
            )
            return response

        patient = Patient(**patient_values)

        db.add(patient)
        db.commit()
        db.refresh(patient)

        response = ResponseModel(
            status_code=201,
            status="success",
            message="Patient created successfully",
            data=patient_data(patient)
        )

        return response

    except Exception as e:
        db.rollback()

        response = ResponseModel(
            status_code=500,
            status="error",
            message=str(e),
            data=None
        )

        return response


def update_patient(updated_patient: dict, db: Session):
    try:
        patient_id = updated_patient["patient_id"]

        patient = db.get(Patient, patient_id)

        if patient is None:
            response = ResponseModel(
                status_code=404,
                status="error",
                message="Patient not found",
                data=None
            )
            return response

        for field, value in updated_patient.items():
            if field != "patient_id" and hasattr(patient, field):
                setattr(patient, field, value)

        db.commit()
        db.refresh(patient)

        response = ResponseModel(
            status_code=200,
            status="success",
            message="Patient updated successfully",
            data=patient_data(patient)
        )

        return response

    except Exception as e:
        db.rollback()

        response = ResponseModel(
            status_code=500,
            status="error",
            message=str(e),
            data=None
        )

        return response


def delete_patient(patient_id: int, db: Session):
    try:
        patient = db.get(Patient, patient_id)

        if patient is None:
            response = ResponseModel(
                status_code=404,
                status="error",
                message="Patient not found",
                data=None
            )
            return response

        deleted_patient = patient_data(patient)

        db.delete(patient)
        db.commit()

        response = ResponseModel(
            status_code=200,
            status="success",
            message="Patient deleted successfully",
            data=deleted_patient
        )

        return response

    except Exception as e:
        db.rollback()

        response = ResponseModel(
            status_code=500,
            status="error",
            message=str(e),
            data=None
        )

        return response