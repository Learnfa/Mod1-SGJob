# streamlit_app/pages/3_Salary_Insights.py
# Interactive salary comparison by category + filters for experience & employment type.

import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import matplotlib.pyplot as plt
import seaborn as sns

from utils.data import get_job_data
from utils.filters import apply_base_filters
from utils.charts import salary_by_sector_bar, salary_by_title_bar
from utils.dark_theme import DarkCatplotTheme

def main():
    st.title("💰 Salary Insights")

    # 1) Load + base filters
    df = get_job_data()
    df_filt, top_n = apply_base_filters(df)

    if df_filt.empty:
        st.info("No job postings match the current global filters.")
        return

    if "average_salary" not in df_filt.columns:
        st.warning("Salary information (average_salary) not available.")
        return

    # Work on a copy to avoid chained assignment issues
    df_work = df_filt.copy()

    # Ensure average_salary is numeric and drop rows without it
    df_work["average_salary"] = pd.to_numeric(
        df_work["average_salary"], errors="coerce"
    )
    df_work = df_work.dropna(subset=["average_salary"])

    if df_work.empty:
        st.info("No valid salary data available after cleaning.")
        return

    # 2) Additional filters: experience & employment type (local to this page)
    st.subheader("Filters (Salary-specific)")
    c1, c2 = st.columns(2)

    # -------------------------
    # Experience filter
    # -------------------------
    with c1:
        if "minimumYearsExperience" in df_work.columns:
            exp_series = pd.to_numeric(
                df_work["minimumYearsExperience"], errors="coerce"
            )

            valid_exp = exp_series.dropna()
            if not valid_exp.empty:
                min_exp = int(valid_exp.min())
                max_exp = int(valid_exp.max())

                # Safety: ensure slider has a valid range
                if min_exp > max_exp:
                    min_exp, max_exp = max_exp, min_exp

                exp_range = st.slider(
                    "Minimum years of experience",
                    min_value=min_exp,
                    max_value=max_exp,
                    value=(min_exp, max_exp),
                )

                mask = (exp_series >= exp_range[0]) & (exp_series <= exp_range[1])
                df_work = df_work[mask]

    # -------------------------
    # Employment type filter
    # -------------------------
    with c2:
        emp_col = None
        if "employment_type" in df_work.columns:
            emp_col = "employment_type"
        elif "employmentTypes" in df_work.columns:
            emp_col = "employmentTypes"

        if emp_col:
            emp_series = df_work[emp_col].dropna()
            if not emp_series.empty:
                emp_options = sorted(emp_series.unique().tolist())
                selected_emp = st.multiselect(
                    "Employment Type (local filter)",
                    options=emp_options,
                    default=emp_options,
                )
                if selected_emp:
                    df_work = df_work[df_work[emp_col].isin(selected_emp)]

    if df_work.empty:
        st.info("No data after applying salary-specific filters.")
        return

    # ================================
    # 1) Salary by sector chart (using top_n)
    # ================================
    st.markdown(f"### Salary by Sector (Top {top_n} Sectors)")

    if "primary_category" not in df_work.columns:
        st.warning("Sector (primary_category) not available; cannot draw salary-by-sector chart.")
    elif not pd.api.types.is_numeric_dtype(df_work["average_salary"]):
        st.warning("Average salary is not numeric; cannot draw salary charts.")
    else:
        # Determine top_n sectors by unique job postings (within the locally filtered df_work)
        sector_counts = (
            df_work.groupby("primary_category")["metadata_jobPostId"]
            .nunique()
            .sort_values(ascending=False)
        )

        if sector_counts.empty:
            st.info("No sector data available to build salary chart.")
        else:
            top_sector_names = sector_counts.head(top_n).index
            df_sector = df_work[df_work["primary_category"].isin(top_sector_names)].copy()

            metric_title = st.radio("Metric", ["median", "mean"], horizontal=True, key="metric_by_title",)   # <-- unique key here

            try:
                chart = salary_by_sector_bar(df_sector, metric=metric_title)
            except Exception as e:
                # Defensive: if the chart function blows up, don't hang the page
                st.error("Unable to build salary-by-sector chart. Please adjust filters.")
                st.exception(e)
            else:
                st.altair_chart(chart, width="stretch")

    # ================================
    # 2) Salary distribution by category (sorted by mean, catplot)
    # ================================
    st.markdown(f"### Salary Distribution by Category (Top {top_n})")

    if "primary_category" in df_work.columns:
        # Top N categories by posting count (to limit noise)
        cat_counts = (
            df_work.groupby("primary_category")["metadata_jobPostId"]
            .nunique()
            .sort_values(ascending=False)
        )

        if not cat_counts.empty:
            top_for_box = min(top_n, len(cat_counts))
            top_cat_names = cat_counts.head(top_for_box).index
            df_box = df_work[df_work["primary_category"].isin(top_cat_names)].copy()

            # clip outliers
            lower = df_box["average_salary"].quantile(0.01)
            upper = df_box["average_salary"].quantile(0.99)
            df_box = df_box[
                (df_box["average_salary"] >= lower)
                & (df_box["average_salary"] <= upper)
            ]

            if not df_box.empty:
                # order by mean salary
                mean_salary_order = (
                    df_box.groupby("primary_category")["average_salary"]
                    .mean()
                    .sort_values(ascending=True)
                    .index
                )
                df_box["primary_category"] = pd.Categorical(
                    df_box["primary_category"],
                    categories=list(mean_salary_order),
                    ordered=True,
                )

                n_cats = len(mean_salary_order)
                height = max(4, 0.35 * n_cats + 1)

                theme = DarkCatplotTheme()
                fig, ax = theme.salary_catplot(
                    df=df_box,
                    order=mean_salary_order.tolist(),
                    height=height,
                    top_n=top_for_box,
                    x_col="average_salary",
                    y_col="primary_category",
#                    title="Salary Distribution by Category",
                )
                st.pyplot(fig, width="stretch")
        else:
            st.info("No category data available to build the distribution chart.")
    else:
        st.warning("Sector (primary_category) not available; cannot draw category distribution chart.")

    # ================================
    # 3) Salary by Job Title chart (using top_n)
    # ================================
    st.markdown(f"### Salary by Job Title (Top {top_n} Titles)")

    if "title" not in df_work.columns:
        st.warning("Title (title) not available; cannot draw salary-by-title chart.")
    elif not pd.api.types.is_numeric_dtype(df_work["average_salary"]):
        st.warning("Average salary is not numeric; cannot draw salary charts.")
    else:
        # Determine top_n titles by unique job postings (within the locally filtered df_work)
        title_counts = (
            df_work.groupby("title")["metadata_jobPostId"]
            .nunique()
            .sort_values(ascending=False)
        )

        if title_counts.empty:
            st.info("No job title data available to build salary chart.")
        else:
            top_title_names = title_counts.head(top_n).index
            df_title = df_work[df_work["title"].isin(top_title_names)].copy()

            metric = st.radio("Metric", ["median", "mean"], horizontal=True)

            try:
                chart = salary_by_title_bar(df_title, metric=metric)
            except Exception as e:
                # Defensive: if the chart function blows up, don't hang the page
                st.error("Unable to build salary-by-title chart. Please adjust filters.")
                st.exception(e)
            else:
                st.altair_chart(chart, width="stretch")

    # ================================
    # 4) Overall salary distribution
    # ================================
    st.markdown("### Salary Distribution (Overall)")

    salary_series = df_work["average_salary"]

    if salary_series.empty or not np.isfinite(salary_series).any():
        st.info("No valid salary data available to display the distribution.")
        return

    # Clean infinities / NaNs
    salary_series = salary_series.replace([np.inf, -np.inf], np.nan).dropna()
    if salary_series.empty:
        st.info("No valid salary data available to display the distribution.")
        return

    # Optional: clip extreme outliers for nicer viz (e.g., 1st–99th percentile)
    lower = salary_series.quantile(0.01)
    upper = salary_series.quantile(0.99)
    salary_clipped = salary_series[(salary_series >= lower) & (salary_series <= upper)]

    if salary_clipped.empty:
        salary_clipped = salary_series  # fall back if clipping nuked everything

    # Build a histogram with Altair instead of raw bar_chart over individual rows
    hist_df = pd.DataFrame({"average_salary": salary_clipped})

    hist = (
        alt.Chart(hist_df)
        .mark_bar()
        .encode(
            x=alt.X(
                "average_salary:Q",
                bin=alt.Bin(maxbins=40),
                title="Average Salary (SGD)",
            ),
            y=alt.Y("count():Q", title="Number of Postings"),
            tooltip=[alt.Tooltip("count():Q", title="Count")],
        )
        .properties(height=400)
    )

    st.altair_chart(hist, width="stretch")


if __name__ == "__main__":
    main()
