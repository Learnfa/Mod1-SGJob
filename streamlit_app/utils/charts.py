# streamlit_app/utils/charts.py
# Reusable Altair charts (simple, interactive).

import altair as alt
import pandas as pd


def top_sectors_bar(df: pd.DataFrame, top_n: int = 10) -> alt.Chart:
    data = (
        df.groupby("primary_category")["metadata_jobPostId"]
          .nunique()
          .reset_index(name="job_count")
          .sort_values("job_count", ascending=False)
          .head(top_n)
    )

    chart = (
        alt.Chart(data)
        .mark_bar()
        .encode(
            x=alt.X("job_count:Q", title="Number of postings"),
            y=alt.Y("primary_category:N", sort="-x", title="Sector"),
            tooltip=["primary_category", "job_count"],
        )
    )
    return chart


def postings_over_time_by_sector(df: pd.DataFrame) -> alt.Chart:
    if "posting_month" not in df.columns:
        return alt.Chart(pd.DataFrame({"x": [], "y": []})).mark_line()

    data = (
        df.groupby(["posting_month", "primary_category"])["metadata_jobPostId"]
          .nunique()
          .reset_index(name="job_count")
    )

    chart = (
        alt.Chart(data)
        .mark_line()
        .encode(
            x=alt.X("posting_month:T", title="Month"),
            y=alt.Y("job_count:Q", title="Number of postings"),
            color=alt.Color("primary_category:N", title="Sector"),
            tooltip=["posting_month", "primary_category", "job_count"],
        )
    )
    return chart


def salary_by_sector_bar(df: pd.DataFrame, metric: str = "median") -> alt.Chart:
    data = (
        df.groupby("primary_category")["average_salary"]
          .agg(mean="mean", median="median", count="count")
          .reset_index()
    )

    chart = (
        alt.Chart(data)
        .mark_bar()
        .encode(
            x=alt.X(f"{metric}:Q", title=f"{metric.capitalize()} average salary"),
            y=alt.Y("primary_category:N", sort="-x", title="Sector"),
            tooltip=[
                "primary_category",
                "mean",
                "median",
                "count",
            ],
        )
    )
    return chart
