# src/data_ingestion.py
from pathlib import Path
from typing import List

import pandas as pd

from .config import (
    RAW_JOB_MARKET_PATH,
    PROCESSED_DATA_DIR,
    PH1_STRUCTURED_PQ_PATH,
    PH1_STRUCTURED_CSV_PATH,
    CATEGORIES_COL,
    BOOL_COLS,
    DATE_COLS,
    NUMERIC_COLS,
)


def load_raw_data(path: Path) -> pd.DataFrame:
    """
    Load the raw job market CSV into a DataFrame.
    """
    if not path.exists():
        raise FileNotFoundError(f"Raw data file not found: {path}")

    df = pd.read_csv(path, low_memory=False)
    return df


def parse_categories_column(df: pd.DataFrame, col: str = CATEGORIES_COL) -> pd.DataFrame:
    """
    Parse the JSON-like 'categories' string column into a list of category names.

    Example raw value:
    "[{\"id\":1,\"category\":\"Accounting / Auditing / Taxation\"},{\"id\":19,\"category\":\"Hospitality\"}]"

    After parsing:
    - df['categories_list'] = [["Accounting / Auditing / Taxation", "Hospitality"], ...]
    - df['primary_category'] = "Accounting / Auditing / Taxation"
    """
    if col not in df.columns:
        return df  # nothing to do

    # Ensure string type and handle NaN
    s = df[col].fillna("").astype(str)

    # Use regex to find all category="..." occurrences
    categories_series = s.str.findall(r'"category":"([^"]+)"')

    df["categories_list"] = categories_series
    # Primary (first) category for convenience
    df["primary_category"] = df["categories_list"].apply(
        lambda lst: lst[0] if isinstance(lst, list) and len(lst) > 0 else None
    )

    return df


def normalize_bool_columns(df: pd.DataFrame, bool_cols: List[str]) -> pd.DataFrame:
    """
    Convert TRUE/FALSE-like string columns to actual booleans.
    """
    for col in bool_cols:
        if col not in df.columns:
            continue

        # Normalize case and common representations
        df[col] = (
            df[col]
            .astype(str)
            .str.strip()
            .str.lower()
            .map(
                {
                    "true": True,
                    "false": False,
                    "1": True,
                    "0": False,
                    "yes": True,
                    "no": False,
                }
            )
            .astype("boolean")
        )
    return df


def normalize_date_columns(df: pd.DataFrame, date_cols: List[str]) -> pd.DataFrame:
    """
    Convert date-like string columns to datetime. Invalids become NaT.
    """
    for col in date_cols:
        if col not in df.columns:
            continue
        df[col] = pd.to_datetime(df[col], errors="coerce")
    return df


def normalize_numeric_columns(df: pd.DataFrame, numeric_cols: List[str]) -> pd.DataFrame:
    """
    Convert numeric-like string columns (including salaries) to numeric dtype.
    Invalids become NaN.
    """
    for col in numeric_cols:
        if col not in df.columns:
            continue
        df[col] = pd.to_numeric(df[col], errors="coerce")
    return df


def run_phase_1_ingestion(
    raw_path: Path = RAW_JOB_MARKET_PATH,
    output_pq_path: Path = PH1_STRUCTURED_PQ_PATH,
    output_csv_path: Path = PH1_STRUCTURED_CSV_PATH,
) -> pd.DataFrame:
    """
    Execute Phase 1: Data Ingestion pipeline.
    Returns the structured DataFrame and saves it to disk.
    """
    print(f"[Phase 1.1] Loading raw data from: {raw_path}")
    df = load_raw_data(raw_path)

    print(f"[Phase 1.2] Raw shape: {df.shape}")

    # 1) Parse categories column
    print("[Phase 1.3] Parsing categories column...")
    df = parse_categories_column(df)

    # 2) Normalize boolean columns
    print("[Phase 1.4] Normalizing boolean columns...")
    df = normalize_bool_columns(df, BOOL_COLS)

    # 3) Normalize date columns
    print("[Phase 1.5] Normalizing date columns...")
    df = normalize_date_columns(df, DATE_COLS)

    # 4) Normalize numeric / salary columns
    print("[Phase 1.6] Normalizing numeric columns...")
    df = normalize_numeric_columns(df, NUMERIC_COLS)

    # 5) Let pandas infer better dtypes where possible (optional but nice)
    print("[Phase 1.7] Converting dtypes (convert_dtypes)...")
    df = df.convert_dtypes()

    # Ensure processed directory exists
    PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)

    print(f"[Phase 1] Saving structured data to: {output_pq_path} and {output_csv_path}")
    df.to_parquet(output_pq_path, index=False)
    df.to_csv(output_csv_path, index=False)

    print("[Phase 1] Done.")
    print("[Phase 1] Final dtypes:")
    print(df.dtypes)

    return df


if __name__ == "__main__":
    run_phase_1_ingestion()
