# src/config.py
from pathlib import Path

# Project root = directory containing this file's parent (src/)
PROJECT_ROOT = Path(__file__).resolve().parents[1]

DATA_DIR = PROJECT_ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"

RAW_JOB_MARKET_PATH = RAW_DATA_DIR / "SGJobData.csv"
PH1_STRUCTURED_PQ_PATH = PROCESSED_DATA_DIR / "SGJobData_structured.parquet"
PH1_STRUCTURED_CSV_PATH = PROCESSED_DATA_DIR / "SGJobData_structured.csv"

# Column names used in ingestion
CATEGORIES_COL = "categories"

BOOL_COLS = [
    "metadata_isPostedOnBehalf",
]

DATE_COLS = [
    "metadata_originalPostingDate",
    "metadata_newPostingDate",
    "metadata_expiryDate",
]

NUMERIC_COLS = [
    "salary_minimum",
    "salary_maximum",
    "minimumYearsExperience",
    "numberOfVacancies",
    "metadata_totalNumberJobApplication",
    "metadata_totalNumberOfView",
    "metadata_repostCount",
]
