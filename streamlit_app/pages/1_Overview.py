# streamlit_app/pages/1_Overview.py
# KPIs + top sectors + top companies.

import streamlit as st

from utils.data import get_job_data
from utils.filters import apply_base_filters
from utils.charts import top_sectors_bar


def main():
    st.title("📊 Overview")

    df = get_job_data()
    df_filt = apply_base_filters(df)

    # --- KPIs ---
    total_posts = df_filt["metadata_jobPostId"].nunique()
    total_companies = df_filt["postedCompany_name"].nunique()
    total_sectors = df_filt["primary_category"].nunique()
    avg_salary = (
        df_filt["average_salary"].mean()
        if "average_salary" in df_filt.columns
        else None
    )

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Job postings", f"{total_posts:,}")
    c2.metric("Hiring companies", f"{total_companies:,}")
    c3.metric("Sectors", f"{total_sectors:,}")
    if avg_salary is not None:
        c4.metric("Avg salary (SGD)", f"{avg_salary:,.0f}")
    else:
        c4.metric("Avg salary (SGD)", "N/A")

    # --- Top sectors ---
    st.subheader("Top Hiring Sectors")
    st.altair_chart(top_sectors_bar(df_filt, top_n=10), 
                    use_container_width=True)

    # --- Top companies ---
    st.subheader("Top Hiring Companies")
    if "postedCompany_name" in df_filt.columns:
        top_n = 20
        company_counts = (
            df_filt.groupby("postedCompany_name")["metadata_jobPostId"]
                  .nunique()
                  .sort_values(ascending=False)
                  .head(top_n)
        )
        top_df = (
            company_counts
            .reset_index(name="job_count")
            .sort_values("job_count", ascending=True)
        )

        st.bar_chart(
            data=top_df,
            x="postedCompany_name",
            y="job_count",
        )
        st.caption("Top 20 companies by number of job postings.")
    else:
        st.info("Company field not available in the dataset.")


if __name__ == "__main__":
    main()
