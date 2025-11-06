# streamlit_app/utils/filters.py
# Global sidebar filters: Employment Type, Position Level, 
# Category, plus optional salary slider.

import streamlit as st
import pandas as pd


def apply_base_filters(df: pd.DataFrame) -> pd.DataFrame:
    """
    Sidebar filters shared across pages:
    - Employment Type
    - Position Level
    - Category (primary_category)
    - Optional salary range if average_salary exists
    """
    filtered = df.copy()

    st.sidebar.header("Global Filters")

    # Employment Type
    if "employmentTypes" in filtered.columns:
        emp_options = sorted(
            filtered["employmentTypes"].dropna().unique().tolist()
        )
        selected_emp = st.sidebar.multiselect(
            "Employment Type",
            options=emp_options,
            default=emp_options,
        )
        if selected_emp:
            filtered = filtered[filtered["employmentTypes"].isin(selected_emp)]

    # Position Level
    if "positionLevels" in filtered.columns:
        lvl_options = sorted(
            filtered["positionLevels"].dropna().unique().tolist()
        )
        selected_lvls = st.sidebar.multiselect(
            "Position Level",
            options=lvl_options,
            default=lvl_options,
        )
        if selected_lvls:
            filtered = filtered[filtered["positionLevels"].isin(selected_lvls)]

    # Category / Sector
    if "primary_category" in filtered.columns:
        cat_options = sorted(
            filtered["primary_category"].dropna().unique().tolist()
        )
        selected_cats = st.sidebar.multiselect(
            "Category / Sector",
            options=cat_options,
            default=cat_options,
        )
        if selected_cats:
            filtered = filtered[filtered["primary_category"].isin(selected_cats)]

    # Salary range (optional)
    if "average_salary" in filtered.columns:
        min_sal = float(filtered["average_salary"].min())
        max_sal = float(filtered["average_salary"].max())
        sel_min, sel_max = st.sidebar.slider(
            "Average Salary Range (SGD)",
            min_value=int(min_sal),
            max_value=int(max_sal),
            value=(int(min_sal), int(max_sal)),
            step=100,
        )
        filtered = filtered[
            (filtered["average_salary"] >= sel_min)
            & (filtered["average_salary"] <= sel_max)
        ]

    st.sidebar.caption(f"{len(filtered):,} records after filtering")
    return filtered
