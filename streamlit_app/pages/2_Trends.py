# streamlit_app/pages/2_Industry_Trends.py
# Comprehensive industry trends dashboard:
# - Job postings over time by sector
# - Salary trend over time (by sector)
# - Application interest trend
# - Vacancy vs postings trend (hiring intensity)
# - Monthly heatmap (sector vs month)
# - Category vs position level heatmap

import streamlit as st
import pandas as pd
import altair as alt

from utils.data import get_job_data
from utils.filters import apply_base_filters
from utils.charts import postings_over_time_by_sector


def main():
    st.title("🏭 Industry Trends")

    df = get_job_data()
    df_filt, top_n = apply_base_filters(df)

    # Identify top N sectors
    if "primary_category" in df_filt.columns:
        top_sectors = (
            df_filt["primary_category"]
            .value_counts()
            .head(top_n)
            .index
        )
        df_top = df_filt[df_filt["primary_category"].isin(top_sectors)]
    else:
        st.warning("No primary_category field found.")
        return

    # ================================
    # --- Job postings over time ---
    # ================================
    st.subheader(f"📈 Job Postings Over Time (Top {top_n} Sectors)")

    if "posting_month" in df_top.columns:
        chart = postings_over_time_by_sector(df_top)
        st.altair_chart(chart, width="stretch")
    else:
        st.info("No posting date information available.")

    # ================================
    # --- Salary trend over time ---
    # ================================
    if "average_salary" in df_top.columns and "posting_month" in df_top.columns:
        st.subheader(f"💰 Average Salary Trend Over Time (Top {top_n} Sectors)")

        salary_trend = (
            df_top.groupby(["posting_month", "primary_category"])["average_salary"]
            .mean()
            .reset_index()
        )

        line = (
            alt.Chart(salary_trend)
            .mark_line(point=True)
            .encode(
                x=alt.X("posting_month:T", title="Month"),
                y=alt.Y("average_salary:Q", title="Average Salary (SGD)", scale=alt.Scale(zero=False)),
                color=alt.Color("primary_category:N", title="Sector"),
                tooltip=[
                    alt.Tooltip("primary_category:N", title="Sector"),
                    alt.Tooltip("posting_month:T", title="Month"),
                    alt.Tooltip("average_salary:Q", title="Avg Salary", format=",.0f"),
                ],
            )
            .properties(height=400)
        )
        st.altair_chart(line, width="stretch")
    else:
        st.info("Salary data not available for trend analysis.")

    # ================================
    # --- Application interest trend ---
    # ================================
    if {
        "posting_month",
        "metadata_totalNumberJobApplication",
        "metadata_totalNumberOfView",
    } <= set(df_top.columns):
        st.subheader("👀 Application Interest Trend (Views & Applications per Posting)")

        interest = (
            df_top.groupby("posting_month")
            .agg(
                total_apps=("metadata_totalNumberJobApplication", "sum"),
                total_views=("metadata_totalNumberOfView", "sum"),
                postings=("metadata_jobPostId", "nunique"),
            )
            .reset_index()
        )
        interest["apps_per_post"] = interest["total_apps"] / interest["postings"]
        interest["views_per_post"] = interest["total_views"] / interest["postings"]

        # Melt for Altair long format
        interest_long = interest.melt(
            id_vars="posting_month",
            value_vars=["apps_per_post", "views_per_post"],
            var_name="metric",
            value_name="value",
        )
        metric_labels = {
            "apps_per_post": "Applications per Posting",
            "views_per_post": "Views per Posting",
        }

        line_interest = (
            alt.Chart(interest_long)
            .mark_line(point=True)
            .encode(
                x=alt.X("posting_month:T", title="Month"),
                y=alt.Y("value:Q", title="Average per Posting", scale=alt.Scale(zero=False)),
                color=alt.Color(
                    "metric:N",
                    title="Metric",
                    scale=alt.Scale(
                        domain=list(metric_labels.keys()),
                        range=["#1f77b4", "#ff7f0e"],
                    ),
                    legend=alt.Legend(labelExpr="datum.label"),
                ),
                tooltip=[
                    alt.Tooltip("posting_month:T", title="Month"),
                    alt.Tooltip("metric:N", title="Metric"),
                    alt.Tooltip("value:Q", title="Value", format=",.2f"),
                ],
            )
            .properties(height=350)
        )
        st.altair_chart(line_interest, width="stretch")
    else:
        st.info("Application or view data not available.")

    # ================================
    # --- Vacancy vs postings trend ---
    # ================================
    if {"posting_month", "numberOfVacancies"} <= set(df_top.columns):
        st.subheader("🏗️ Hiring Intensity: Vacancies vs Postings Trend")

        vac_trend = (
            df_top.groupby("posting_month")
            .agg(
                total_vacancies=("numberOfVacancies", "sum"),
                total_postings=("metadata_jobPostId", "nunique"),
            )
            .reset_index()
        )
        vac_trend["vacancies_per_posting"] = (
            vac_trend["total_vacancies"] / vac_trend["total_postings"]
        )

        line_vac = (
            alt.Chart(vac_trend)
            .transform_fold(
                ["total_postings", "total_vacancies"],
                as_=["metric", "value"],
            )
            .mark_line(point=True)
            .encode(
                x=alt.X("posting_month:T", title="Month"),
                y=alt.Y("value:Q", title="Count", scale=alt.Scale(zero=False)),
                color=alt.Color(
                    "metric:N",
                    title="Metric",
                    scale=alt.Scale(
                        domain=["total_postings", "total_vacancies"],
                        range=["#1f77b4", "#2ca02c"],
                    ),
                    legend=alt.Legend(
                        orient="top", title=None, labelExpr="datum.label"
                    ),
                ),
                tooltip=[
                    alt.Tooltip("posting_month:T", title="Month"),
                    alt.Tooltip("metric:N", title="Metric"),
                    alt.Tooltip("value:Q", title="Value", format=",.0f"),
                ],
            )
            .properties(height=350)
        )
        st.altair_chart(line_vac, width="stretch")
    else:
        st.info("Vacancy count not available.")

    # ================================
    # --- Posting Duration Trend ---
    # ================================
    if {"posting_month", "posting_duration"} <= set(df_top.columns):
        st.subheader("⏳ Average Posting Duration Over Time (Days)")

        # Filter out negative or unrealistically long durations
        df_dur = df_top[df_top["posting_duration"].between(0, 180)]

        # Average posting duration by month and sector (limit to top_n)
        dur_trend = (
            df_dur.groupby(["posting_month", "primary_category"])["posting_duration"]
            .mean()
            .reset_index()
        )
        dur_trend = dur_trend[dur_trend["primary_category"].isin(top_sectors)]

        chart = (
            alt.Chart(dur_trend)
            .mark_line(point=True)
            .encode(
                x=alt.X("posting_month:T", title="Month"),
                y=alt.Y(
                    "posting_duration:Q",
                    title="Average Posting Duration (Days)",
                    scale=alt.Scale(zero=False),
                ),
                color=alt.Color("primary_category:N", title="Sector"),
                tooltip=[
                    alt.Tooltip("primary_category:N", title="Sector"),
                    alt.Tooltip("posting_month:T", title="Month"),
                    alt.Tooltip("posting_duration:Q", format=".1f", title="Avg Days"),
                ],
            )
            .properties(height=400)
        )

        st.altair_chart(chart, width="stretch")
    else:
        st.info("Posting duration data not available in this dataset.")

    # ================================
    # --- Category vs Position Level heatmap ---
    # ================================
    st.subheader(f"📊 Sector vs Position Level (Top {top_n} Sectors)")

    if {"primary_category", "positionLevels"} <= set(df_top.columns):
        cross = (
            pd.crosstab(df_top["primary_category"], df_top["positionLevels"])
            .reset_index()
            .melt(
                id_vars="primary_category",
                var_name="positionLevels",
                value_name="count",
            )
        )

        heat = (
            alt.Chart(cross)
            .mark_rect()
            .encode(
                x=alt.X("positionLevels:N", title="Position Level"),
                y=alt.Y(
                    "primary_category:N", title="Sector", sort=top_sectors.tolist()
                ),
                color=alt.Color("count:Q", title="Number of Postings"),
                tooltip=["primary_category", "positionLevels", "count"],
            )
            .properties(height=500)
        )
        st.altair_chart(heat, width="stretch")
    else:
        st.info("Required fields (primary_category, positionLevels) are missing.")


if __name__ == "__main__":
    main()
