# Project Plan: Interactive Data Storytelling Dashboard for the Singapore Job Market

## Objectives
1. Collect, clean, and transform raw job postings data from available sources (CSV, API, or SQL).
2. Conduct exploratory data analysis (EDA) to uncover key trends and insights about the job market — industries, roles, salaries, demand, etc.
3. Build interactive visual narratives to help stakeholders understand employment patterns.
4. Deploy a Streamlit-based dashboard for users to explore and filter insights dynamically.

---

## Tech Stack

| Stage | Technology | Purpose |
|-------|-------------|----------|
| Environment | uv | Lightweight Python environment and dependency management |
| Data Processing | pandas, numpy | Data ingestion, cleaning, feature engineering |
| Analysis | pandas, numpy, scipy (optional) | EDA, correlation, statistical summaries |
| Visualization | matplotlib, seaborn | Exploratory and static charting |
| Dashboard | Streamlit | Interactive dashboard deployment |
| Storage | CSV / SQLite (optional) | Intermediate cleaned dataset storage |
| Version Control | Git | Source control and reproducibility |

---

## Dataset Overview

Each row represents a job posting with fields such as:

- categories (JSON list of categories)
- employmentTypes
- posting dates (`metadata_originalPostingDate`, `metadata_newPostingDate`, `metadata_expiryDate`)
- organization, salary range, experience, vacancies, position level
- title (job title)
- status (Open/Closed)

### Enables Analysis on
- Industry trends (via `categories`)
- Salary distribution per sector and level
- Hiring patterns over time
- Demand vs supply indicators
- Correlation between experience and salary

---

## Project Phases

### Phase 1: Data Ingestion
**Goal:** Load and structure the dataset for processing.

**Tasks**
1. Read CSV into pandas (`pd.read_csv()`).
2. Parse JSON-like `categories` column:
   ```python
   df["categories"] = df["categories"].str.findall(r'"category":"([^"]+)"')
3. Handle mixed data types (e.g., convert metadata_isPostedOnBehalf to boolean).
4. Normalize date columns using pd.to_datetime.
5. Convert salary fields to numeric (salary_minimum, salary_maximum).

**Deliverable:** Clean, structured Pandas DataFrame.

---

## Phase 2: Data Cleaning & Transformation
**Goal:** Prepare the dataset for analysis.

**Tasks**
- Remove duplicates and invalid rows (e.g., missing job title, salary = 0).
- Remove any columns that have all NaN
- Drop the original categories (JSON list of categories)
- Fill missing values (e.g., replace NaN in experience with 0).
- Standardize `employmentTypes` (“Full Time”, “Permanent”, etc.).
- Derive new columns:
  - `average_salary = (salary_minimum + salary_maximum) / 2`
  - `posting_duration = expiry_date - original_posting_date`
  - `num_categories = df["categories"].apply(len)`
  - Extract year-month for trend analysis.
- Save the cleaned dataset to `/data/processed/job_market_clean.csv`.

**Deliverable:** Transformed dataset ready for EDA.

---

### Phase 3: Exploratory Data Analysis (EDA)
**Goal:** Understand key data characteristics and uncover insights.

**Tasks**
- Descriptive statistics: job counts, salary summary, min/max/mean by sector.
- Correlations: experience ↔ salary, position level ↔ salary.
- Anomaly detection: unrealistic salaries or posting dates.
- Trend analysis: job postings by month and category.
- Visuals (Matplotlib/Seaborn):
  - `sns.boxplot` for salary distribution by category
  - `sns.countplot` for employment type
  - `sns.heatmap` for correlation matrix
  - Line chart of job posting volume over time

**Deliverable:**  
EDA notebook (`notebooks/eda.ipynb`) and exported static charts (`/reports/figures/`).

---

### Phase 4: Insight Generation
**Goal:** Translate analysis into meaningful business insights.

**Example Insights**
- which skills and roles are in high demand.
- which companies are hiring aggressively in tech
- Top 20 list:
  - company by job posting
  - sectors by ave salary
  - titles by ave salary
  - etc
- Salary Analysis & Market Benchmarking
- IT, Professional Services, and Consulting have the highest average salary ranges.
- Non-Executive roles dominate Admin and Secretarial categories.
- High competition in IT sector — more postings but slower closure rate.
- Demand for Data and AI-related roles increased steadily from April to May.
- Top Job, Company etc

Each insight will correspond to one or more visualizations in the dashboard.

---

### Phase 5: Dashboard Development (Streamlit)

**Goal:** Create an interactive web dashboard for data storytelling.

**Streamlit Folder Structure**
```text
streamlit_app/
│
├── app.py
├── pages/
│   ├── 1_Overview.py
│   ├── 2_Industry_Trends.py
│   ├── 3_Salary_Insights.py
│   ├── 4_Experience_and_Roles.py
│
├── data/
│   ├── job_market_clean.csv
│
└── utils/
    ├── charts.py
    ├── filters.py
```

**Dashboard Features**

#### Overview Page
- Total postings, avg salary, top hiring industries.
- Filters: Employment Type, Position Level, Category.

#### Industry Trends
- Line chart of job postings over time by sector.
- Heatmap of category vs position level.

#### Salary Insights
- Interactive salary comparison by category.
- Adjustable filters for Experience and Employment Type.

#### Experience & Roles
- Scatter plot: experience vs salary.
- Countplot: roles by level and experience.

#### Export Options
- Download filtered dataset as CSV.

**Deliverable:** Fully functional interactive dashboard.

---

### Phase 6: Deployment

**Goal:** Make the dashboard accessible to stakeholders.

**Tasks**

1. Setup `uv` environment:
   ```bash
   uv venv
   uv add pandas numpy matplotlib seaborn streamlit

2. Create .env (optional) for configurations.

3. Run locally:
    ```bash
    streamlit run app.py

4. For production deployment:

    ```dockerfile
    FROM python:3.11-slim
    WORKDIR /app
    COPY . .
    RUN uv pip install -r requirements.txt
    CMD ["streamlit", "run", "app.py", "--server.port=8501"]
    ```

5. Host on Streamlit Cloud.

**Deliverable:** Live dashboard URL or Dockerized container.

---

### Expected Visualizations

| Chart        | Purpose                           |
| ------------ | --------------------------------- |
| Bar Chart    | Top 10 industries by job postings |
| Boxplot      | Salary distribution by category   |
| Line Chart   | Job postings trend over months    |
| Heatmap      | Correlation of numeric features   |
| Scatter Plot | Experience vs Salary              |
| Pie Chart    | Employment type breakdown         |

### Deliverables Summary

| Deliverable                         | Description                  |
| ----------------------------------- | ---------------------------- |
| data/raw/job_market.csv             | Raw dataset                  |
| data/processed/job_market_clean.csv | Cleaned dataset              |
| notebooks/eda.ipynb                 | EDA with visualizations      |
| streamlit_app/                      | Streamlit dashboard code     |
| requirements.txt or uv.lock         | Dependencies                 |
| README.md                           | Setup and usage instructions |
| Dockerfile (optional)               | Containerized deployment     |

### Timeline (Estimated 4 Weeks)

| Week   | Milestone                                |
| ------ | ---------------------------------------- |
| Week 1 | Data ingestion, cleaning, transformation |
| Week 2 | EDA & visualization prototyping          |
| Week 3 | Insight synthesis, dashboard design      |
| Week 4 | Streamlit development & deployment       |
