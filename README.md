# Healthcare Data Cleaning and Prediction Pipeline

This project combines a healthcare data cleaning workflow, validation checks, feature analysis, and machine learning model training into a single Python application. It also exposes patient endpoints through a FastAPI service for CRUD operations and condition prediction.

## Overview

The pipeline processes raw patient data from CSV format, cleans and validates it, selects relevant features, trains classification models, saves the best-performing model, and allows predictions to be made from API requests.

The model predicts patient condition labels such as:

- Asthma
- Diabetes
- Heart Disease
- Hypertension

## Features

- Raw healthcare dataset ingestion from CSV files
- Data cleaning and normalization
- Duplicate and missing-value handling
- Validation reporting for data quality issues
- Feature selection for model training
- Model benchmarking and best-model selection
- Artifacts saving for reuse during prediction
- FastAPI endpoints for patient management
- Patient condition prediction endpoint

## Tech stack

- Python
- Pandas
- NumPy
- scikit-learn
- SciPy
- Matplotlib
- Seaborn
- FastAPI
- SQLAlchemy
- PostgreSQL
- psycopg
- python-dotenv

## Project structure

```text
data-cleaning-pipeline/
├── app/
│   ├── controller/
│   │   └── patient_routes.py
│   ├── schema/
│   │   ├── patient.py
│   │   └── response.py
│   ├── services/
│   │   └── patient_service.py
│   └── main.py
├── cleaning/
│   ├── clean_data.py
│   └── validate_data.py
├── data/
│   ├── cleaned/
│   │   └── healthcare_clean.json
│   └── raw/
│       └── healthcare.csv
├── model/
│   └── patient.py
├── training/
│   ├── feature_analysis.py
│   ├── model_training.py
│   └── predict.py
├── validation_report/
│   └── validation_report.json
├── artifacts/
├── main.py
├── database.py
├── import_json.py
├── requirements.txt
├── README.md
└── .env.example (optional, if you create one locally)
```

## Data pipeline

### 1. Cleaning
The cleaning step reads the raw CSV file, standardizes column names, normalizes values, removes duplicates, and handles missing or inconsistent records before preparing the dataset for modeling.

### 2. Validation
The validator checks for: 

- missing fields
- invalid values
- duplicate rows
- schema inconsistencies
- low-quality or malformed records

Validation results are written to the `validation_report/` directory.

### 3. Feature analysis
Feature analysis identifies the variables most strongly associated with the target condition, helping reduce noise and improve model performance.

### 4. Model training
The project trains several classification models, compares their results, and saves the best-performing model together with preprocessing artifacts used for inference.

### 5. API access
FastAPI exposes patient management and prediction endpoints so the model can be used programmatically from a service or frontend.

## Prerequisites

Before running the project, make sure you have:

- Python 3.10+
- PostgreSQL running locally or in a configured environment
- A virtual environment for the project

## Setup

### 1. Clone the repository

```bash
git clone <repository-url>
cd data-cleaning-pipeline
```

### 2. Create and activate a virtual environment

Windows PowerShell:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

macOS/Linux:

```bash
python -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure the database

The app uses PostgreSQL through SQLAlchemy and loads connection settings from environment variables. Default values are:

- host: `localhost`
- port: `5432`
- database: `healthcare_db`
- user: `postgres`

Example environment configuration:

```bash
DB_HOST=localhost
DB_PORT=5432
DB_NAME=healthcare_db
DB_USER=postgres
DB_PASSWORD=your_password
```

Make sure a PostgreSQL database with the configured name already exists before starting the API or running the training pipeline.

## Run the full pipeline

This script cleans the dataset, validates it, trains the model, and saves the final artifacts:

```bash
python main.py
```

## Start the API

```bash
uvicorn app.main:app --reload
```

The API is exposed through the `app.main:app` entry point and includes the following routes.

### Patient routes

- `GET /patients/` — list all patients
- `GET /patients/{patient_id}` — fetch one patient by ID
- `POST /patients/` — create a patient record
- `PUT /patients/` — update a patient record
- `DELETE /patients/{patient_id}` — delete a patient record
- `POST /patients/predict` — predict a patient condition from input data

### Root endpoint

- `GET /` — health check message confirming the service is running

## Input and output files

### Raw data

```text
data/raw/healthcare.csv
```

### Cleaned data

```text
data/cleaned/healthcare_clean.json
```

### Validation report

```text
validation_report/validation_report.json
```

### Model artifacts

```text
artifacts/
```

These artifacts include the trained model and metadata required for prediction.

## Example workflow

```bash
python main.py
uvicorn app.main:app --reload
```

Once the model has been trained, you can send patient records to the prediction endpoint and receive a predicted condition along with probability scores.

## Notes

This repository is intended as a practical example of a healthcare ML pipeline that combines data engineering, model training, and backend API integration in a single project. It is useful for learning, prototyping, and extending into a larger healthcare analytics workflow.


The prediction script outputs the predicted condition for each input patient.

## Technologies Used

* Python
* Pandas
* NumPy
* Scikit-learn
* SciPy
* Matplotlib
* Seaborn

## Project Goal

The goal of this project is to demonstrate an end-to-end data processing and machine learning workflow, from raw healthcare data to validated data, statistical feature analysis, trained classification models, and patient condition predictions.
