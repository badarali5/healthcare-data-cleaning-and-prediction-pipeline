import json
from fastapi import status
from app.schema.response import ResponseModel

FILE_PATH = "data/cleaned/healthcare_clean.json"

REQUIRED_FIELDS = [
    "patient_name",
    "age",
    "gender",
    "medication",
    "cholesterol",
    "respiratory_rate",
    "oxygen_saturation",
    "fasting_blood_sugar",
    "hba1c",
    "insulin_level",
    "systolic_bp_reading",
    "diastolic_bp_reading",
    "wheezing_present",
    "chest_pain_type",
]


def validate_required_fields(patient: dict, response: ResponseModel) -> bool:
    missing = [
        field for field in REQUIRED_FIELDS
        if patient.get(field) is None
    ]

    if missing:
        response.status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
        response.status = "error"
        response.message = f"Missing required fields: {', '.join(missing)}"
        response.data = None
        return True

    return False


def read_patients():
    with open(FILE_PATH, "r") as file:
        return json.load(file)


def write_patients(patients):
    with open(FILE_PATH, "w") as file:
        json.dump(patients, file, indent=4)

def get_all_patients():
    response = ResponseModel(
        status_code=0,
        status="",
        message="",
        data=None
    )

    try:
        patients = read_patients()

        response.status_code = status.HTTP_200_OK
        response.status = "success"
        response.message = "Patients retrieved successfully"
        response.data = patients

        return response

    except Exception as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        response.status = "error"
        response.message = str(e)
        response.data = None

        return response

def get_patient(patient_id: int):
    response = ResponseModel(
        status_code=0,
        status="",
        message="",
        data=None
    )

    try:
        patients = read_patients()

        for patient in patients:
            if patient["patient_id"] == patient_id:

                response.status_code = status.HTTP_200_OK
                response.status = "success"
                response.message = "Patient retrieved successfully"
                response.data = patient

                return response

        response.status_code = status.HTTP_404_NOT_FOUND
        response.status = "error"
        response.message = "Patient not found"
        response.data = None

        return response

    except Exception as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        response.status = "error"
        response.message = str(e)
        response.data = None

        return response

def create_patient(patient: dict):
    response = ResponseModel(
        status_code=0,
        status="",
        message="",
        data=None
    )

    try:
        if validate_required_fields(patient, response):
            return response

        patients = read_patients()

        patient_id = patient["patient_id"]

        for existing_patient in patients:
            if existing_patient["patient_id"] == patient_id:

                response.status_code = status.HTTP_400_BAD_REQUEST
                response.status = "error"
                response.message = "Patient ID already exists"
                response.data = existing_patient

                return response

        patients.append(patient)
        write_patients(patients)

        response.status_code = status.HTTP_201_CREATED
        response.status = "success"
        response.message = "Patient created successfully"
        response.data = patient

        return response

    except Exception as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        response.status = "error"
        response.message = str(e)
        response.data = None

        return response
    # UPDATE
def update_patient(updated_patient: dict):
    response = ResponseModel(
        status_code=0,
        status="",
        message="",
        data=None
    )

    try:
        if validate_required_fields(updated_patient, response):
            return response

        patients = read_patients()

        patient_id = updated_patient["patient_id"]

        for i, patient in enumerate(patients):

            if patient["patient_id"] == patient_id:

                patients[i] = updated_patient
                write_patients(patients)

                response.status_code = status.HTTP_200_OK
                response.status = "success"
                response.message = "Patient updated successfully"
                response.data = updated_patient

                return response

        response.status_code = status.HTTP_404_NOT_FOUND
        response.status = "error"
        response.message = "Patient not found"
        response.data = None

        return response

    except Exception as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        response.status = "error"
        response.message = str(e)
        response.data = None

        return response

def delete_patient(patient_id: int):
    response = ResponseModel(
        status_code=0,
        status="",
        message="",
        data=None
    )

    try:
        patients = read_patients()

        for i, patient in enumerate(patients):

            if patient["patient_id"] == patient_id:

                deleted_patient = patients.pop(i)
                write_patients(patients)

                response.status_code = status.HTTP_200_OK
                response.status = "success"
                response.message = "Patient deleted successfully"
                response.data = deleted_patient

                return response

        response.status_code = status.HTTP_404_NOT_FOUND
        response.status = "error"
        response.message = "Patient not found"
        response.data = None

        return response

    except Exception as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        response.status = "error"
        response.message = str(e)
        response.data = None

        return response