# streamlit_app/pages/3_Salary_Insights.py
# Interactive salary comparison by category + filters for experience & employment type.

import streamlit as st
import pandas as pd
import numpy as np

from utils.data import get_job_data
from utils.filters import apply_base_filters
from utils.charts import salary_by_sector_bar


def main():
    st.title("💰 Salary Insights")

    # 1) Load + base filters
    df = get_job_data()
    df_filt = apply_base_filters(df)

    if df_filt.empty:
        st.info("No job postings match the current global filters.")
        return

    if "average_salary" not in df_filt.columns:
        st.warning("Salary information (average_salary) not available.")
        return

    # Ensure average_salary is numeric and drop rows without it
    df_filt["average_salary"] = pd.to_numeric(
        df_filt["average_salary"], errors="coerce"
    )
    df_filt = df_filt.dropna(subset=["average_salary"])

    if df_filt.empty:
        st.info("No valid salary data available after cleaning.")
        return

    # 2) Additional filters: experience & employment type (local to this page)
    st.subheader("Filters (Salary-specific)")
    c1, c2 = st.columns(2)

    # Experience filter
    with c1:
        if "minimumYearsExperience" in df_filt.columns:
            exp_series = pd.to_numeric(
                df_filt["minimumYearsExperience"], errors="coerce"
            )

            if exp_series.notna().any():
                min_exp = int(exp_series.min())
                max_exp = int(exp_series.max())

                exp_range = st.slider(
                    "Minimum years of experience",
                    min_value=min_exp,
                    max_value=max_exp,
                    value=(min_exp, max_exp),
                )

                mask = (exp_series >= exp_range[0]) & (exp_series <= exp_range[1])
                df_filt = df_filt[mask]

    # Employment type filter
    with c2:
        if "employmentTypes" in df_filt.columns:
            emp_series = df_filt["employmentTypes"].dropna()
            if not emp_series.empty:
                emp_options = sorted(emp_series.unique().tolist())
                selected_emp = st.multiselect(
                    "Employment Type (local filter)",
                    options=emp_options,
                    default=emp_options,
                )
                if selected_emp:
                    df_filt = df_filt[df_filt["employmentTypes"].isin(selected_emp)]

    if df_filt.empty:
        st.info("No data after applying salary-specific filters.")
        return

    # 3) Salary by sector chart
    st.markdown("### Salary by Sector")

    if not pd.api.types.is_numeric_dtype(df_filt["average_salary"]):
        st.warning("Average salary is not numeric; cannot draw salary charts.")
    else:
        metric = st.radio("Metric", ["median", "mean"], horizontal=True)

        try:
            chart = salary_by_sector_bar(df_filt, metric=metric)
        except Exception as e:
            # Defensive: if the chart function blows up, don't hang the page
            st.error("Unable to build salary-by-sector chart. Please adjust filters.")
            st.exception(e)
        else:
            st.altair_chart(chart, use_container_width=True)

    # 4) Overall salary distribution
    st.markdown("### Salary distribution (overall)")

    salary_series = df_filt["average_salary"]
    if salary_series.empty or not np.isfinite(salary_series).any():
        st.info("No valid salary data available to display the distribution.")
    else:
        # Clean infinities just in case
        salary_series = salary_series.replace([np.inf, -np.inf], np.nan).dropna()
        if salary_series.empty:
            st.info("No valid salary data available to display the distribution.")
        else:
            st.bar_chart(salary_series)


if __name__ == "__main__":
    main()
