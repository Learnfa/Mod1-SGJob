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

## Phase 4 – Insight Generation

**Goal:**  
Translate analytical findings from the EDA into clear, data-driven insights that reveal Singapore’s job-market dynamics and prepare them for interactive visualization.

**Deliverables**
- `notebooks/insights.ipynb` – Reproducible notebook computing key metrics and generating static charts.  
- `reports/data/*.csv` – Aggregated datasets (e.g., top sectors, top titles, salary statistics).  
- `reports/figures/*.png` – Exported figures for each insight (ready for dashboard or report use).  
- `reports/insights_catalog.md` – Narrative catalog describing each insight and corresponding visualization.

**Key Analytical Themes**
1. **Demand & Hiring Landscape**  
   - Top hiring sectors and companies  
   - Executive-level dominance in job postings  
   - Posting seasonality and volume trends  

2. **Salary Analysis & Benchmarking**  
   - Average and median salary by sector  
   - Top-paying job titles (≥ 5 postings)  
   - Experience–salary relationships  
   - Seniority premiums within each sector  

3. **Competition & Market Tightness**  
   - Applications per vacancy by sector  
   - Hard-to-fill roles (median days open, repost frequency)  
   - Quick-fill administrative positions  

4. **Skills & Emerging Trends**  
   - Growth in Data & AI-related roles over time  
   - Sectoral spread of AI/Data positions  

5. **Operational Insights**  
   - Average posting lifespan (`days_open`)  
   - Reposting frequency as indicator of hiring friction  

6. **Market Concentration (Example Findings)**  
   - Top 20 companies account for only ~30 % of postings, confirming a **long-tail hiring** pattern.  
   - Herfindahl–Hirschman Index (HHI) ≈ 90 → **Highly competitive / fragmented market**.  

**Outputs are consumed by:**  
Phase 5 – Interactive Dashboard (Streamlit), where users can dynamically filter and explore these insights.

---

### Phase 5 – Dashboard Development (Streamlit)

**Goal:**  
Create an interactive web dashboard for **data storytelling** that allows users to explore Singapore’s job-market insights dynamically.

**Dashboard Features**

#### 🧭 Overview Page
- Displays total job postings, average salary, and top hiring industries.
- Interactive filters: **Employment Type**, **Position Level**, **Category**.

#### 📈 Industry Trends
- Line chart showing job-posting trends over time by sector.
- Heatmap illustrating **category vs. position level** relationships.

#### 💰 Salary Insights
- Interactive comparison of average and median salaries by category.
- Adjustable filters for **Years of Experience** and **Employment Type**.

#### 👩‍💼 Experience & Roles
- Scatter plot: **Experience vs. Salary** to highlight market benchmarks.
- Countplot: role distribution by **Level** and **Experience Range**.

#### 📤 Export Options
- Allow users to **download filtered datasets as CSV** for offline analysis.

**Deliverable:**  
A fully functional **Streamlit dashboard** that integrates outputs from Phase 4 (`/reports/data` and `/reports/figures`) to enable interactive exploration and storytelling of Singapore’s job-market dynamics.

### Phase 6 – Deployment & Presentation

**Goal:**  
Deploy the Streamlit dashboard to a live environment and prepare materials for stakeholder presentation and demonstration.

**Deployment Options**
- **Streamlit Community Cloud:** Simple deployment with automatic GitHub integration.  
- **Internal Server / VM:** Containerized deployment via Docker Compose for production-grade hosting.  
- **Cloud Provider (AWS / GCP / Azure):** Managed hosting with HTTPS, authentication, and usage tracking.

**Deployment Steps**
1. Finalize environment configuration (`requirements.txt` / `Dockerfile`).  
2. Set up environment variables (e.g., data paths, access keys).  
3. Deploy Streamlit app using `streamlit run app.py` or via CI/CD pipeline.  
4. Configure reverse proxy and HTTPS (if self-hosted).  
5. Validate interactive features and ensure dataset auto-refresh (optional via cron or API).  

**Presentation Materials**
- Demo walkthrough highlighting dashboard features and insights.  
