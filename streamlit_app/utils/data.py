# -----------------------------
# streamlit_app/utils/data.py
# loader for the cleaned CSV (Phase 2/3 output) 
# a few helper columns.
# ------------------------------

from pathlib import Path
import pandas as pd
import streamlit as st
from src.config import PH2_CLEANED_CSV_PATH

@st.cache_data(show_spinner="Loading job postings data...")
def get_job_data(remove_outliers: bool = True) -> pd.DataFrame:
    """
    Load the pre-cleaned Singapore job dataset.
    Optionally remove salary outliers (1st–99th percentile).
    """
    data_path = PH2_CLEANED_CSV_PATH

    st.write(f"📂 Loading dataset from: `{data_path}`")
    df = pd.read_csv(data_path)
    
    # --- Base type handling -------------------------------------------------
    # Date columns (if present)
    if "metadata_originalPostingDate" in df.columns:
        df["posting_date"] = pd.to_datetime(
            df["metadata_originalPostingDate"], errors="coerce"
        )
        df["posting_month"] = df["posting_date"].dt.to_period("M").astype(str)

    # Salary: ensure numeric
    if "average_salary" in df.columns:
        df["average_salary"] = pd.to_numeric(df["average_salary"], errors="coerce")

    # Experience
    if "minimumYearsExperience" in df.columns:
        df["minimumYearsExperience"] = pd.to_numeric(
            df["minimumYearsExperience"], errors="coerce"
        )
    
    # Apps per vacancy
    if {"metadata_totalNumberJobApplication", "numberOfVacancies"} <= set(df.columns):
        df["apps_per_vacancy"] = (
            df["metadata_totalNumberJobApplication"]
            / df["numberOfVacancies"].replace({0: pd.NA})
        )

    # --- Salary outlier removal (consistent with EDA) ----------------------
    if remove_outliers and "average_salary" in df.columns:
        lower_thr = df["average_salary"].quantile(0.01)
        upper_thr = df["average_salary"].quantile(0.99)

        original_len = len(df)
        df = df[
            (df["average_salary"] >= lower_thr)
            & (df["average_salary"] <= upper_thr)
        ].copy()

        st.info(
            f"Filtered salary outliers outside [1%, 99%]. "
            f"Rows kept: {len(df):,} "
            f"({100 * len(df) / original_len:.1f}% of original)."
        )
        
    return df
