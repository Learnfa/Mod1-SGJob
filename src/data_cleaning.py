from pathlib import Path
import pandas as pd
import numpy as np
from .config import PROCESSED_DATA_DIR, PH1_STRUCTURED_PQ_PATH

CLEAN_OUTPUT_PATH = PROCESSED_DATA_DIR / "SGJobData_clean.csv"


def load_structured_data(path: Path = PH1_STRUCTURED_PQ_PATH) -> pd.DataFrame:
    """Load Phase 1 structured dataset."""
    if not path.exists():
        raise FileNotFoundError(f"Structured dataset not found: {path}")
    return pd.read_parquet(path)


def clean_and_transform(df: pd.DataFrame) -> pd.DataFrame:
    """Perform Phase 2 cleaning and transformation."""
    print(f"[Phase 2.1] Before cleaning: No. of rows {df.shape[0]}")

    # --- Remove duplicates based on job ID ---
    id_col = "metadata_jobPostId"
    if id_col in df.columns:
        before = len(df)
        df = df.drop_duplicates(subset=[id_col])
        print(f"[Phase 2.2] Dropped {before - len(df)} duplicate rows based on '{id_col}'")
    else:
        print(f"[Phase 2.2] Column '{id_col}' not found — no duplicates dropped.")

    # --- Remove invalid rows ---
    df = df[df["title"].notna()]  # must have title
    print(f"[Phase 2.3] After dropping NaN in title: {df.shape[0]} rows")

    if "salary_minimum" in df and "salary_maximum" in df:
        df = df[(df["salary_minimum"] > 0) & (df["salary_maximum"] > 0)]
        print(f"[Phase 2.4] After dropping -ve Min/Max salary: {df.shape[0]} rows")

    # --- Drop all-NaN columns ---
    nan_cols = df.columns[df.isna().all()].tolist()
    if nan_cols:
        print(f"[Phase 2.5] Dropping {len(nan_cols)} all-NaN columns: {nan_cols}")
        df = df.dropna(axis=1, how="all")
    else:
        print("[Phase 2.5] No all-NaN columns found.")
    
    # --- Drop original JSON categories column if still present ---
    if "categories" in df.columns:
        df = df.drop(columns=["categories"])
        print("[Phase 2.6] Dropping original categories JSON column.")

    # --- Fill missing numeric values ---
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    df[numeric_cols] = df[numeric_cols].fillna(0)
    print("[Phase 2.7] Fill na with 0")

    # --- Standardize employmentTypes ---
    if "employmentTypes" in df.columns:
        df["employmentTypes"] = (
            df["employmentTypes"]
            .str.strip()
            .str.lower()
            .replace(
                {
                    "full-time": "Full Time",
                    "full time": "Full Time",
                    "permanent": "Permanent",
                    "contract": "Contract",
                    "temp": "Temporary",
                    "temporary": "Temporary",
                    "internship": "Internship",
                    "part time": "Part Time",
                }
            )
        )

    # --- Derive new columns ---
    if {"salary_minimum", "salary_maximum"}.issubset(df.columns):
        df["average_salary"] = (df["salary_minimum"] + df["salary_maximum"]) / 2

    if {
        "metadata_expiryDate",
        "metadata_originalPostingDate",
    }.issubset(df.columns):
        df["posting_duration"] = (
            df["metadata_expiryDate"] - df["metadata_originalPostingDate"]
        ).dt.days

    if "categories_list" in df.columns:
        df["num_categories"] = df["categories_list"].apply(
            lambda x: len(x) if isinstance(x, list) else 0
        )

    # --- Extract posting month for trend analysis ---
    date_col = (
        "metadata_newPostingDate"
        if "metadata_newPostingDate" in df.columns
        else "metadata_originalPostingDate"
    )
    if date_col in df.columns:
        df["posting_month"] = df[date_col].dt.to_period("M").astype(str)

    print(f"[Phase 2] Finished transformation: {df.shape[0]} rows × {df.shape[1]} cols")
    return df


def save_clean_data(df: pd.DataFrame, path: Path = CLEAN_OUTPUT_PATH) -> None:
    PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False)
    print(f"[Phase 2] Clean dataset saved to {path}")


def run_phase2_cleaning():
    df = load_structured_data()
    df_clean = clean_and_transform(df)
    save_clean_data(df_clean)
    return df_clean


if __name__ == "__main__":
    run_phase2_cleaning()
