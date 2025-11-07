# streamlit_app/utils/filters.py 
# Global sidebar filters: Sector, Experience, Position Level,
# Salary range, Employment Type – with styled sidebar.

import streamlit as st
import pandas as pd


def apply_base_filters(df: pd.DataFrame) -> tuple[pd.DataFrame, int]:
    """
    Sidebar filters shared across pages, using the new styled layout:
    - Top N selector for charts/lists
    - Sector (primary_category)
    - Experience band (experienceTypes)
    - Position (positionLevels)
    - Salary range (average_salary, 1st–99th percentile, padded to ≥ 15k)
    - Employment Type (employmentTypes)
    """

    df_raw = df.copy()
    filtered = df.copy()

    # Default Top N (used if widget not rendered for some reason)
    top_n = 20

    # ------------- Sidebar UI -------------
    with st.sidebar:
        st.markdown('<div class="sidebar-title">Dataset Filters</div><div></div>', unsafe_allow_html=True)
        st.markdown('<div class="sidebar-title"> </div>', unsafe_allow_html=True)

        # -------- Top N (for charts & lists) --------
        top_n = st.number_input(
            "Top N to display",
            min_value=5,
            max_value=100,
            value=15,
            step=5,
            help="Controls how many top items charts/lists will show (e.g. Top N sectors, roles, etc.)",
        )

        # -------- Sector (primary_category) --------
        if "primary_category" in df_raw.columns:
            cat_series = df_raw["primary_category"].dropna()
            if not cat_series.empty:
                sector_options = ["All"] + sorted(cat_series.unique().tolist())
                sel_sector = st.selectbox("Sector", sector_options, index=0)
            else:
                sel_sector = "All"
        else:
            sel_sector = "All"

        # -------- Experience band (experienceTypes) --------
        if "experienceTypes" in df_raw.columns:
            exp_series = df_raw["experienceTypes"].dropna()
            if not exp_series.empty:
                exp_options = ["All"] + sorted(exp_series.astype(str).unique().tolist())
                sel_exp = st.selectbox("Experience Band", exp_options, index=0)
            else:
                sel_exp = "All"
        else:
            sel_exp = "All"

        # -------- Position level (positionLevels) --------
        pos_col = "positionLevels" if "positionLevels" in df_raw.columns else None
        if pos_col:
            pos_series = df_raw[pos_col].dropna()
            if not pos_series.empty:
                pos_options = ["All"] + sorted(pos_series.unique().tolist())
                sel_pos = st.selectbox("Position Level", pos_options, index=0)
            else:
                sel_pos = "All"
        else:
            sel_pos = "All"

        # -------- Salary range (average_salary) --------
        sel_salary = None
        if "average_salary" in df_raw.columns:
            sal_series = pd.to_numeric(df_raw["average_salary"], errors="coerce").dropna()
            if not sal_series.empty:
                salary_min = int(sal_series.quantile(0.01))
                salary_max = int(sal_series.quantile(0.99))
                max_slider = max(15000, salary_max)

                st.markdown("Monthly Salary Range (SGD)")
                sel_salary = st.slider(
                    "",
                    min_value=0,
                    max_value=max_slider,
                    value=(0, max_slider),
                    step=250,
                )

        # -------- Employment type (employmentTypes) --------
        emp_col = "employmentTypes" if "employmentTypes" in df_raw.columns else None
        if emp_col:
            emp_series = df_raw[emp_col].dropna()
            if not emp_series.empty:
                emp_options = ["All"] + sorted(emp_series.unique().tolist())
                sel_emp = st.selectbox("Employment Type", emp_options, index=0)
            else:
                sel_emp = "All"
        else:
            sel_emp = "All"

    # ------------- Apply filters -------------
    # Sector
    if sel_sector != "All" and "primary_category" in filtered.columns:
        filtered = filtered[filtered["primary_category"] == sel_sector]

    # Experience band
    if sel_exp != "All" and "experienceTypes" in filtered.columns:
        filtered = filtered[filtered["experienceTypes"].astype(str) == sel_exp]

    # Position level
    if sel_pos != "All" and pos_col and pos_col in filtered.columns:
        filtered = filtered[filtered[pos_col] == sel_pos]

    # Salary range
    if sel_salary is not None and "average_salary" in filtered.columns:
        min_sal, max_sal = sel_salary
        sal_series_f = pd.to_numeric(filtered["average_salary"], errors="coerce")
        filtered = filtered[
            (sal_series_f >= min_sal) & (sal_series_f <= max_sal)
        ]

    # Employment type
    if sel_emp != "All" and emp_col and emp_col in filtered.columns:
        filtered = filtered[filtered[emp_col] == sel_emp]

    st.sidebar.caption(f"{len(filtered):,} records after filtering")
    return filtered, int(top_n)
