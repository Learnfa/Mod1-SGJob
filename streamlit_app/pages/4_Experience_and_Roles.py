# streamlit_app/pages/4_Experience_and_Roles.py
# Scatter: experience vs salary, plus countplot-style bar for roles by level & experience.

import streamlit as st
import pandas as pd
import altair as alt

from utils.data import get_job_data
from utils.filters import apply_base_filters


def main():
    st.title("👩‍💼 Experience & Roles")

    df = get_job_data()
    df_filt = apply_base_filters(df)

    if {"minimumYearsExperience", "average_salary"} - set(df_filt.columns):
        st.warning("Experience or salary columns are missing.")
        return

    df_exp = df_filt.dropna(subset=["minimumYearsExperience", "average_salary"])

    # Scatter: experience vs salary, colored by position level
    st.subheader("Experience vs Salary")

    scatter = (
        alt.Chart(df_exp)
        .mark_circle(size=60, opacity=0.5)
        .encode(
            x=alt.X("minimumYearsExperience:Q", title="Minimum years of experience"),
            y=alt.Y("average_salary:Q", title="Average salary (SGD)"),
            color=alt.Color("positionLevels:N", title="Position level"),
            tooltip=[
                "title",
                "primary_category",
                "minimumYearsExperience",
                "average_salary",
                "positionLevels",
            ],
        )
    )
    st.altair_chart(scatter, use_container_width=True)

    # Roles by level and experience bucket
    st.subheader("Roles by Level and Experience bucket")

    # Simple bucketing for display
    bins = [-1, 2, 5, 10, 100]
    labels = ["0–2", "3–5", "6–10", "10+"]
    df_exp["experience_band"] = pd.cut(
        df_exp["minimumYearsExperience"], bins=bins, labels=labels
    )

    crosstab = (
        pd.crosstab(df_exp["positionLevels"], df_exp["experience_band"])
        .reset_index()
        .melt(id_vars="positionLevels", var_name="experience_band", value_name="count")
    )

    bar = (
        alt.Chart(crosstab)
        .mark_bar()
        .encode(
            x=alt.X("experience_band:N", title="Experience band (years)"),
            y=alt.Y("count:Q", title="Number of postings"),
            color=alt.Color("positionLevels:N", title="Position level"),
            tooltip=["positionLevels", "experience_band", "count"],
        )
    )
    st.altair_chart(bar, use_container_width=True)

    st.markdown("### Download filtered dataset")
    st.download_button(
        "Download as CSV",
        data=df_filt.to_csv(index=False).encode("utf-8"),
        file_name="filtered_job_data.csv",
        mime="text/csv",
    )


if __name__ == "__main__":
    main()
