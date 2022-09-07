"""
Useful code handle file paths for the project and data configurations
"""
import os


class FilePaths:
    PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
    DATA_DIR = os.path.abspath(os.path.join(PROJECT_DIR, "data"))
    MODEL_DIR = os.path.abspath(os.path.join(PROJECT_DIR, "models"))
    RAW_DATA = os.path.abspath(os.path.join(DATA_DIR, "raw"))
    PROCESSED_DATA = os.path.abspath(os.path.join(DATA_DIR, "processed"))
    ENCOUNTERS_DATA = os.path.abspath(os.path.join(RAW_DATA, "encounters.csv"))
    PATIENTS_DATA = os.path.abspath(os.path.join(RAW_DATA, "patients.csv"))
    TEST_DATA = os.path.abspath(os.path.join(RAW_DATA, "test_patients.csv"))


class EncountersConfig:
    COLUMNS = [
        "START",
        "PATIENT",
        "CODE",
        "DESCRIPTION",
        "REASONCODE",
        "REASONDESCRIPTION",
    ]
    DATE_COLUMNS = ["START"]


class PatientsConfig:
    COLUMNS = ["Id", "BIRTHDATE", "DEATHDATE", "RACE", "GENDER"]
    DATE_COLUMNS = ["BIRTHDATE", "DEATHDATE"]
