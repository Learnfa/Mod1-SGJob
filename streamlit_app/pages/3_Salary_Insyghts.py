# streamlit_app/pages/3_Salary_Insights.py
# Interactive salary comparison by category + filters for experience & employment type.

import streamlit as st
import pandas as pd

from utils.data import get_job_data
from utils.filters import apply_base_filters
from utils.charts import salary_by_sector_bar


def main():
    st.title("💰 Salary Insights")

    df = get_job_data()
    df_filt = apply_base_filters(df)

    if "average_salary" not in df_filt.columns:
        st.warning("Salary information (average_salary) not available.")
        return

    # Additional filters: experience & employment type (local to this page)
    st.subheader("Filters (Salary-specific)")

    c1, c2 = st.columns(2)

    with c1:
        if "minimumYearsExperience" in df_filt.columns:
            min_exp = int(df_filt["minimumYearsExperience"].min())
            max_exp = int(df_filt["minimumYearsExperience"].max())
            exp_range = st.slider(
                "Minimum years of experience",
                min_value=min_exp,
                max_value=max_exp,
                value=(min_exp, max_exp),
            )
            df_filt = df_filt[
                (df_filt["minimumYearsExperience"] >= exp_range[0])
                & (df_filt["minimumYearsExperience"] <= exp_range[1])
            ]

    with c2:
        if "employmentTypes" in df_filt.columns:
            emp_options = sorted(
                df_filt["employmentTypes"].dropna().unique().tolist()
            )
            selected_emp = st.multiselect(
                "Employment Type (local filter)",
                options=emp_options,
                default=emp_options,
            )
            if selected_emp:
                df_filt = df_filt[df_filt["employmentTypes"].isin(selected_emp)]

    st.markdown("### Salary by Sector")

    metric = st.radio("Metric", ["median", "mean"], horizontal=True)
    st.altair_chart(
        salary_by_sector_bar(df_filt, metric=metric),
        use_container_width=True,
    )

    st.markdown("### Salary distribution (overall)")
    st.bar_chart(df_filt["average_salary"])


if __name__ == "__main__":
    main()
