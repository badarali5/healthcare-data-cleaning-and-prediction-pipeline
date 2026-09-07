import json

from database import SessionLocal
from model.patient import Patient


FILE_PATH = "data/cleaned/healthcare_clean.json"


def import_patients():
    db = SessionLocal()

    valid_columns = {c.name for c in Patient.__table__.columns}

    try:
        with open(FILE_PATH, "r", encoding="utf-8") as file:
            patients = json.load(file)

        for patient_data in patients:
            filtered_data = {k: v for k, v in patient_data.items() if k in valid_columns}
            patient = Patient(**filtered_data)
            db.merge(patient)

        db.commit()
        print("Patients imported successfully.")

    except Exception as e:
        db.rollback()
        print(f"Import failed: {e}")

    finally:
        db.close()


if __name__ == "__main__":
    import_patients()

        