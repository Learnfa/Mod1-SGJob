# streamlit_app/pages/1_Overview.py
# KPIs + top sectors + top companies + side-by-side Employment Type & Position Level pies

import streamlit as st
import altair as alt
import pandas as pd

from utils.data import get_job_data
from utils.filters import apply_base_filters


def main():
    st.title("📊 Overview")

    df = get_job_data()
    df_filt, top_n = apply_base_filters(df)

    # --- Matrics ---
    total_posts = df_filt["metadata_jobPostId"].nunique()
    total_companies = df_filt["postedCompany_name"].nunique()
    total_sectors = df_filt["primary_category"].nunique()
    avg_salary = (
        df_filt["average_salary"].mean()
        if "average_salary" in df_filt.columns
        else None
    )

    # ================================
    # --- Matrics ---
    # ================================
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Job postings", f"{total_posts:,}")
    c2.metric("Hiring companies", f"{total_companies:,}")
    c3.metric("Sectors", f"{total_sectors:,}")
    c4.metric("Avg salary (SGD)", f"{avg_salary:,.0f}" if avg_salary else "N/A")

    # ================================
    # --- Top Hiring Sectors ---
    # ================================
    st.subheader("Top Hiring Sectors")

    if "primary_category" in df_filt.columns:
        sector_counts = (
            df_filt.groupby("primary_category")["metadata_jobPostId"]
            .nunique()
            .sort_values(ascending=False)
        )

        top_sector_counts = sector_counts.head(top_n)
        other_count = sector_counts.iloc[top_n:].sum()

        top_sector_counts.index.name = "Sector"
        bar_df = top_sector_counts.reset_index(name="job_count")

        pie_counts = top_sector_counts.copy()
        if other_count > 0:
            pie_counts = pd.concat([pie_counts, pd.Series({"Others": other_count})])
        pie_counts.index.name = "Sector"
        pie_df = pie_counts.reset_index(name="job_count")
        pie_df["pct"] = (pie_df["job_count"] / pie_df["job_count"].sum()) * 100
        pie_df["label"] = pie_df["Sector"] + " (" + pie_df["pct"].round(1).astype(str) + "%)"

        col1, col2 = st.columns([2, 1])

        # Bar
        max_jobs = bar_df["job_count"].max()
        bar_chart = (
            alt.Chart(bar_df)
            .mark_bar()
            .encode(
                x=alt.X(
                    "job_count:Q",
                    title="Number of Job Postings",
                    axis=alt.Axis(format="~s"),
                    scale=alt.Scale(domain=(0, max_jobs * 1.1)),
                ),
                y=alt.Y("Sector:N", sort="-x", title="Sector"),
                tooltip=["Sector", "job_count"],
            )
            .properties(height=400)
        )
        col1.altair_chart(bar_chart, width="stretch")

        # Pie
        pie_chart = (
            alt.Chart(pie_df)
            .mark_arc(innerRadius=40)
            .encode(
                theta=alt.Theta("job_count:Q", stack=True),
                color=alt.Color("label:N", title="Sector (%)", scale=alt.Scale(scheme="category20")),
                tooltip=["Sector", "job_count", alt.Tooltip("pct:Q", format=".1f", title="%")],
            )
            .properties(height=400, width=400)
        )
        col2.altair_chart(pie_chart, width="stretch")

    st.caption(f"Top {top_n} sectors (remaining aggregated as 'Others' in pie).")

    # ================================
    # --- Top Hiring Companies ---
    # ================================
    st.subheader("Top Hiring Companies")

    if "postedCompany_name" in df_filt.columns:
        company_counts = (
            df_filt.groupby("postedCompany_name")["metadata_jobPostId"]
            .nunique()
            .sort_values(ascending=False)
        )

        top_company_counts = company_counts.head(top_n)
        other_count = company_counts.iloc[top_n:].sum()

        top_company_counts.index.name = "Company"
        bar_df = top_company_counts.reset_index(name="job_count")

        pie_counts = top_company_counts.copy()
        if other_count > 0:
            pie_counts = pd.concat([pie_counts, pd.Series({"Others": other_count})])
        pie_counts.index.name = "Company"
        pie_df = pie_counts.reset_index(name="job_count")
        pie_df["pct"] = (pie_df["job_count"] / pie_df["job_count"].sum()) * 100
        pie_df["label"] = pie_df["Company"] + " (" + pie_df["pct"].round(1).astype(str) + "%)"

        col1, col2 = st.columns([2, 1])

        bar_chart = (
            alt.Chart(bar_df)
            .mark_bar()
            .encode(
                x=alt.X("job_count:Q", title="Number of Job Postings", axis=alt.Axis(format="~s")),
                y=alt.Y("Company:N", sort="-x", title="Company"),
                tooltip=["Company", "job_count"],
            )
            .properties(height=400)
        )
        col1.altair_chart(bar_chart, width="stretch")

        pie_chart = (
            alt.Chart(pie_df)
            .mark_arc(innerRadius=40)
            .encode(
                theta=alt.Theta("job_count:Q", stack=True),
                color=alt.Color("label:N", title="Company (%)", scale=alt.Scale(scheme="category20")),
                tooltip=["Company", "job_count", alt.Tooltip("pct:Q", format=".1f", title="%")],
            )
            .properties(height=400, width=400)
        )
        col2.altair_chart(pie_chart, width="stretch")

    st.caption(f"Top {top_n} companies (remaining aggregated as 'Others' in pie).")


    # ================================
    # --- Top Hiring Job Titles ---
    # ================================
    st.subheader("Top Hiring Job Titles")

    if "title" in df_filt.columns:
        title_counts = (
            df_filt.groupby("title")["metadata_jobPostId"]
            .nunique()
            .sort_values(ascending=False)
        )

        top_title_counts = title_counts.head(top_n)
        other_count = title_counts.iloc[top_n:].sum()
 
        top_title_counts.index.name = "Title"
        bar_df = top_title_counts.reset_index(name="job_count")

        pie_counts = top_title_counts.copy()
        if other_count > 0:
            pie_counts = pd.concat([pie_counts, pd.Series({"Others": other_count})])
        pie_counts.index.name = "Title"
        pie_df = pie_counts.reset_index(name="job_count")
        pie_df["pct"] = (pie_df["job_count"] / pie_df["job_count"].sum()) * 100
        pie_df["label"] = pie_df["Title"] + " (" + pie_df["pct"].round(1).astype(str) + "%)"

        col1, col2 = st.columns([2, 1])

        # Bar
        max_jobs = bar_df["job_count"].max()
        bar_chart = (
            alt.Chart(bar_df)
            .mark_bar()
            .encode(
                x=alt.X(
                    "job_count:Q",
                    title="Number of Job Postings",
                    axis=alt.Axis(format="~s"),
                    scale=alt.Scale(domain=(0, max_jobs * 1.1)),
                ),
                y=alt.Y("Title:N", sort="-x", title="Title"),
                tooltip=["Title", "job_count"],
            )
            .properties(height=400)
        )
        col1.altair_chart(bar_chart, width="stretch")

        # Pie
        pie_chart = (
            alt.Chart(pie_df)
            .mark_arc(innerRadius=40)
            .encode(
                theta=alt.Theta("job_count:Q", stack=True),
                color=alt.Color("label:N", title="Job Title (%)", scale=alt.Scale(scheme="category20")),
                tooltip=["Title", "job_count", alt.Tooltip("pct:Q", format=".1f", title="%")],
            )
            .properties(height=400, width=400)
        )
        col2.altair_chart(pie_chart, width="stretch")

    st.caption(f"Top {top_n} Job Titles (remaining aggregated as 'Others' in pie).")
        

    # ================================
    # --- Employment Types & Position Levels (side-by-side pies) ---
    # ================================
    st.subheader("Employment Types & Position Levels")

    col1, col2 = st.columns(2)

    # --- Employment Type Pie ---
    emp_col = "employment_type" if "employment_type" in df_filt.columns else (
        "employmentTypes" if "employmentTypes" in df_filt.columns else None
    )

    if emp_col:
        emp_counts = (
            df_filt.groupby(emp_col)["metadata_jobPostId"]
            .nunique()
            .sort_values(ascending=False)
        )
        pie_df = emp_counts.reset_index(name="job_count")
        pie_df["pct"] = (pie_df["job_count"] / pie_df["job_count"].sum()) * 100
        pie_df["label"] = pie_df[emp_col] + " (" + pie_df["pct"].round(1).astype(str) + "%)"

        emp_chart = (
            alt.Chart(pie_df)
            .mark_arc(innerRadius=40)
            .encode(
                theta=alt.Theta("job_count:Q", stack=True),
                color=alt.Color(
                    "label:N", title="Employment Type (%)", scale=alt.Scale(scheme="category20")
                ),
                tooltip=[emp_col, "job_count", alt.Tooltip("pct:Q", format=".1f", title="%")],
            )
            .properties(height=350, width=350)
        )

        with col1:
            st.markdown("### 🧑‍💼 Employment Types")
            st.altair_chart(emp_chart, width="stretch")
    else:
        with col1:
            st.info("Employment type field not available.")

    # --- Position Level Pie ---
    pos_col = "position_level" if "position_level" in df_filt.columns else (
        "positionLevels" if "positionLevels" in df_filt.columns else None
    )

    if pos_col:
        pos_counts = (
            df_filt.groupby(pos_col)["metadata_jobPostId"]
            .nunique()
            .sort_values(ascending=False)
        )
        pie_df = pos_counts.reset_index(name="job_count")
        pie_df["pct"] = (pie_df["job_count"] / pie_df["job_count"].sum()) * 100
        pie_df["label"] = pie_df[pos_col] + " (" + pie_df["pct"].round(1).astype(str) + "%)"

        pos_chart = (
            alt.Chart(pie_df)
            .mark_arc(innerRadius=40)
            .encode(
                theta=alt.Theta("job_count:Q", stack=True),
                color=alt.Color(
                    "label:N", title="Position Level (%)", scale=alt.Scale(scheme="category20")
                ),
                tooltip=[pos_col, "job_count", alt.Tooltip("pct:Q", format=".1f", title="%")],
            )
            .properties(height=350, width=350)
        )

        with col2:
            st.markdown("### 🪜 Position Levels")
            st.altair_chart(pos_chart, width="stretch")
    else:
        with col2:
            st.info("Position level field not available.")


if __name__ == "__main__":
    main()
