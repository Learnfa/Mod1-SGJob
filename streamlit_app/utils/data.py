# -----------------------------
# streamlit_app/utils/data.py
# loader for the cleaned CSV (Phase 2/3 output) 
# a few helper columns.
# ------------------------------

from pathlib import Path
import sys

# Ensure project root (sgjob_v2) is on sys.path
# This file lives at: sgjob_v2/streamlit_app/utils/data.py
ROOT = Path(__file__).resolve().parents[2]  # → sgjob_v2
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

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
    
    # --- Salary & minyrexp outlier removal (consistent with EDA) ----------------------
    if remove_outliers and "average_salary" in df.columns:
        lower_thr = df["average_salary"].quantile(0.01)
        upper_thr = df["average_salary"].quantile(0.99)

        # Ensure experience is numeric for clean filtering
        if "minimumYearsExperience" in df.columns:
            df["minimumYearsExperience"] = pd.to_numeric(
                df["minimumYearsExperience"], errors="coerce"
            )

        original_len = len(df)
        df = df[
            (df["average_salary"] >= lower_thr)
            & (df["average_salary"] <= upper_thr)
            & (
                ~df["minimumYearsExperience"].isna()
                & df["minimumYearsExperience"].between(0, 30, inclusive="both")
            )
        ].copy()

        st.info(
            f"Filtered salary outliers (outside [1%, 99%]) and "
            f"experience anomalies (<0 or >30 years). "
            f"Rows kept: {len(df):,} "
            f"({100 * len(df) / original_len:.1f}% of original)."
        )
        
    return df
