# 🇸🇬 Singapore Job Market Dashboard

**Interactive Data Storytelling Dashboard** built with **Python + Streamlit**, using real job-posting data to reveal trends in industries, roles, salaries, and demand across Singapore.

---

## 🧭 Project Overview

This project demonstrates a full **data-science lifecycle** — from raw data ingestion through cleaning, analysis, and interactive visualization.  
It is structured for reproducibility and can be extended for other labor-market datasets.

### Objectives
- Collect, clean, and structure raw job-posting data.
- Perform Exploratory Data Analysis (EDA) to uncover insights.
- Build an interactive **Streamlit** dashboard for stakeholders.

---

## 🏗️ Architecture & Tech Stack

| Stage | Technology | Purpose |
|--------|-------------|----------|
| Environment | **uv + pyproject.toml** | Lightweight Python dependency & venv management |
| Data Processing | **pandas, numpy** | Ingestion, cleaning, feature engineering |
| Visualization | **matplotlib, seaborn** | Statistical & exploratory plots |
| Dashboard | **Streamlit** | Interactive data storytelling |
| Storage | **CSV / Parquet** | Processed dataset artifacts |
| Version Control | **Git** | Source control & reproducibility |

---

## 📂 Folder Structure
## 📂 Folder Structure

```text
sg-job-market-dashboard/
├── data/
│   ├── raw/
│   │   └── job_market.csv
│   └── processed/
│       ├── job_market_structured.parquet     # from Phase 1
│       └── job_market_clean.csv              # from Phase 2
├── notebooks/
│   └── eda.ipynb                             # Phase 3 EDA analysis
├── reports/
│   └── figures/                              # exported charts (png)
├── src/
│   ├── config.py
│   ├── data_ingestion.py                     # Phase 1: ingestion & structuring
│   └── data_cleaning.py                      # Phase 2: cleaning & transformation
├── streamlit_app/
│   ├── app.py                                # Streamlit entrypoint
│   ├── pages/
│   │   ├── 1_Overview.py
│   │   ├── 2_Industry_Trends.py
│   │   ├── 3_Salary_Insights.py
│   │   └── 4_Experience_and_Roles.py
│   └── utils/
│       ├── charts.py
│       └── filters.py
├── pyproject.toml
├── uv.lock
└── README.md
```
---

## ⚙️ Setup

### 1️⃣ Create / activate environment

```bash
uv init        # only once if starting fresh
uv sync        # install dependencies from pyproject.toml
```

### 2️⃣ Run data-processing phases

```bash
# Phase 1 – Data Ingestion
uv run python -m src.data_ingestion

# Phase 2 – Data Cleaning & Transformation
uv run python -m src.data_cleaning
```

### 3️⃣ Run EDA notebook
- Open notebooks/eda.ipynb in VS Code or Jupyter and execute all cells.
- Figures are saved automatically under reports/figures/.

---

## 📊 Data-Processing Phases

### Phase 1 – Data Ingestion
- Load raw CSV into pandas.
- Parse JSON-like categories field into lists (categories_list, primary_category).
- Normalize booleans, dates, and salary fields.
- Save structured dataset as job_market_structured.parquet.

### Phase 2 – Data Cleaning & Transformation
- Remove duplicates by metadata_jobPostId.
- Drop all-NaN columns and invalid rows (missing title, zero salary).
- Fill NaN numeric values with 0.
- Standardize employmentTypes.
- Derive new columns:
    - average_salary = (salary_minimum + salary_maximum)/2
    - posting_duration = expiry − original_posting_date
    - num_categories = len(categories_list)
    - posting_month (YYYY-MM)
- Save cleaned dataset → data/processed/job_market_clean.csv.

### Phase 3 – Exploratory Data Analysis (EDA)
- Descriptive statistics & correlations.
- Salary and experience scatterplots.
- Outlier detection (1st & 99th percentile) + filtered visualization dataset.
- Trend analysis: postings by month & category.
- Export static charts to reports/figures/.

## 🖼️ Example Visualizations
**Boxplot:** Salary distribution by industry

**Heatmap:** Correlation matrix

**Scatterplot:** Experience vs Average Salary

**Line chart:** Job postings over time

**Countplot:** Employment type breakdown

All generated via Matplotlib / Seaborn and saved in reports/figures/.

💡 Next Phases

Phase 4 – Insight Generation
Translate analytical findings into business insights (e.g., sectors with highest salary growth).

Phase 5 – Streamlit Dashboard
Interactive filters, salary comparisons, and category trends.

Phase 6 – Deployment
uv Dockerized image → deploy to Streamlit Cloud or container host.