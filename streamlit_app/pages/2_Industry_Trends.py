# streamlit_app/pages/2_Industry_Trends.py
# Line chart over time + heatmap category vs position level.

import streamlit as st
import pandas as pd
import altair as alt

from utils.data import get_job_data
from utils.filters import apply_base_filters
from utils.charts import postings_over_time_by_sector


def main():
    st.title("🏭 Industry Trends")

    df = get_job_data()
    df_filt = apply_base_filters(df)

    st.subheader("Job postings over time by sector")

    if "posting_month" not in df_filt.columns:
        st.warning("No posting date information available.")
    else:
        chart = postings_over_time_by_sector(df_filt)
        st.altair_chart(chart, use_container_width=True)

    st.subheader("Category vs Position Level")
    if {"primary_category", "positionLevels"} <= set(df_filt.columns):
        cross = pd.crosstab(
            df_filt["primary_category"],
            df_filt["positionLevels"]
        ).reset_index().melt(
            id_vars="primary_category",
            var_name="positionLevels",
            value_name="count"
        )

        heat = (
            alt.Chart(cross)
            .mark_rect()
            .encode(
                x=alt.X("positionLevels:N", title="Position Level"),
                y=alt.Y("primary_category:N", title="Sector"),
                color=alt.Color("count:Q", title="Number of postings"),
                tooltip=["primary_category", "positionLevels", "count"],
            )
        )
        st.altair_chart(heat, use_container_width=True)
    else:
        st.info("Required fields (primary_category, positionLevels) are missing.")


if __name__ == "__main__":
    main()
