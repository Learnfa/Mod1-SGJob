# streamlit_app/pages/4_Experience_and_Roles.py
# Scatter: experience vs salary, plus countplot-style bar for roles by level & experience.

import streamlit as st
import pandas as pd
import altair as alt

from utils.data import get_job_data
from utils.filters import apply_base_filters


MAX_SCATTER_POINTS = 25_000  # cap points sent to browser for scatter


def main():
    st.title("👩‍💼 Experience & Roles")

    df = get_job_data()
    df_filt, _ = apply_base_filters(df)

    required_cols = {
        "minimumYearsExperience",
        "average_salary",
        "positionLevels",
        "title",
        "primary_category",
    }
    missing = required_cols - set(df_filt.columns)
    if missing:
        st.warning(f"Missing columns: {', '.join(sorted(missing))}")
        return

    df_exp = (
        df_filt[list(required_cols)]
        .dropna(subset=["minimumYearsExperience", "average_salary"])
        .copy()
    )

    if df_exp.empty:
        st.info("No records with both experience and salary available after filtering.")
        return

    # --- Clean and filter numeric values ---
    df_exp["minimumYearsExperience"] = pd.to_numeric(
        df_exp["minimumYearsExperience"], errors="coerce"
    )
    df_exp = df_exp[
        (df_exp["minimumYearsExperience"] >= 0)
        & (df_exp["minimumYearsExperience"] <= 20)
    ]

    # Clip salary outliers (1–99 percentile)
    sal_low, sal_high = df_exp["average_salary"].quantile([0.01, 0.99])
    df_exp = df_exp[
        (df_exp["average_salary"] >= sal_low)
        & (df_exp["average_salary"] <= sal_high)
    ]

    if df_exp.empty:
        st.info("No data left after removing outliers.")
        return

    # ---------------------------------------------
    # Scatter: Experience vs Salary (integer X-axis)
    # ---------------------------------------------
    st.subheader("Experience vs Salary (0–20 Years)")

    if len(df_exp) > MAX_SCATTER_POINTS:
        df_scatter = df_exp.sample(n=MAX_SCATTER_POINTS, random_state=42)
        st.caption(
            f"Showing a sample of {MAX_SCATTER_POINTS:,} postings "
            f"out of {len(df_exp):,} to keep the scatter responsive."
        )
    else:
        df_scatter = df_exp

    scatter = (
        alt.Chart(df_scatter)
        .mark_circle(size=60, opacity=0.5)
        .encode(
            x=alt.X(
                "minimumYearsExperience:Q",
                title="Years of Experience",
                scale=alt.Scale(domain=[0, 20]),
                axis=alt.Axis(
                    tickMinStep=1,
                    values=list(range(0, 21)),
                    labelExpr="datum.value == floor(datum.value) ? datum.label : ''",
                ),
            ),
            y=alt.Y("average_salary:Q", title="Average Salary (SGD)"),
            color=alt.Color("positionLevels:N", title="Position Level"),
            tooltip=[
                "title",
                "primary_category",
                "minimumYearsExperience",
                "average_salary",
                "positionLevels",
            ],
        )
        .interactive()
    )

    st.altair_chart(scatter, width="stretch")

    # --------------------------------------------
    # Roles by level and experience bucket (bar)
    # --------------------------------------------
    st.subheader("Roles by Level and Experience Band")

    bins = [-1, 2, 5, 10, 20]
    labels = ["0–2", "3–5", "6–10", "11–20"]
    df_exp["experience_band"] = pd.cut(
        df_exp["minimumYearsExperience"], bins=bins, labels=labels
    )

    crosstab = (
        pd.crosstab(df_exp["positionLevels"], df_exp["experience_band"])
        .reset_index()
        .melt(
            id_vars="positionLevels",
            var_name="experience_band",
            value_name="count",
        )
    )

    bar = (
        alt.Chart(crosstab)
        .mark_bar()
        .encode(
            x=alt.X("experience_band:N", title="Experience Band (Years)", sort=labels),
            y=alt.Y("count:Q", title="Number of Postings"),
            color=alt.Color("positionLevels:N", title="Position Level"),
            tooltip=["positionLevels", "experience_band", "count"],
        )
    )

    st.altair_chart(bar, width="stretch")

    # -----------------------------
    # Download filtered dataset
    # -----------------------------
    st.markdown("### Download filtered dataset")
    st.download_button(
        "Download as CSV",
        data=df_filt.to_csv(index=False).encode("utf-8"),
        file_name="filtered_job_data.csv",
        mime="text/csv",
    )


if __name__ == "__main__":
    main()
