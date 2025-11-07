# src/config.py
from pathlib import Path

# ---------------------------------------------------------------------
# Project structure
# ---------------------------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parents[1]

DATA_DIR = PROJECT_ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"

RAW_JOB_MARKET_PATH = RAW_DATA_DIR / "SGJobData.csv"
PH1_STRUCTURED_PQ_PATH = PROCESSED_DATA_DIR / "SGJobData_structured.parquet"
PH1_STRUCTURED_CSV_PATH = PROCESSED_DATA_DIR / "SGJobData_structured.csv"
PH2_CLEANED_CSV_PATH = PROCESSED_DATA_DIR / "SGJobData_clean.csv"

REPORTS_DIR = PROJECT_ROOT / "reports"
FIGURES_DIR = REPORTS_DIR / "figures"
TABLES_DIR = REPORTS_DIR / "data"
NOTEBOOKS_DIR = PROJECT_ROOT / "notebooks"

# Ensure key dirs exist (optional safety)
for d in [RAW_DATA_DIR, PROCESSED_DATA_DIR, REPORTS_DIR, FIGURES_DIR, TABLES_DIR]:
    d.mkdir(parents=True, exist_ok=True)
    
# ---------------------------------------------------------------------
# Data schema metadata
# ---------------------------------------------------------------------
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

# ---------------------------------------------------------------------
# Convenience helpers
# ---------------------------------------------------------------------
def path_exists(path: Path) -> bool:
    """Return True if path exists, False otherwise."""
    return path.exists()

def get_data_path(filename: str) -> Path:
    """Get full path of a file inside processed data dir."""
    return PROCESSED_DATA_DIR / filename