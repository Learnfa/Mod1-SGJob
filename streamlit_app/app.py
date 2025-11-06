# streamlit_app/app.py
# Main entry; Streamlit will auto-discover the pages/ folder.

import streamlit as st

st.set_page_config(
    page_title="Singapore Job Market Dashboard",
    page_icon="💼",
    layout="wide",
)

st.title("Singapore Job Market – Interactive Dashboard")

st.markdown(
    """
Use the navigation in the sidebar to explore:

- **Overview** – high-level KPIs and top sectors/companies  
- **Industry Trends** – how hiring evolves over time and across sectors  
- **Salary Insights** – salary benchmarks by sector and experience  
- **Experience & Roles** – how role levels and experience relate to pay  

Global filters (Employment Type, Position Level, Category, Salary)
are available on each page via the sidebar.
"""
)
