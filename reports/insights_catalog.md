# 📘 Singapore Job Market – Insights Catalog
**Phase 4: Insight Generation**

---

## 🎯 Purpose
This document summarizes the analytical findings derived from the Singapore Job Postings dataset.  
Each insight connects quantitative evidence from the cleaned dataset (`df_clean`) to a clear business narrative.  
These insights will serve as the content foundation for the interactive Streamlit dashboard.

---

## 1️⃣ Demand & Hiring Landscape

| ID | Insight Title | Description | Key Metrics / Computation | Visual Suggestion |
|----|----------------|--------------|----------------------------|-------------------|
| D1 | **Hiring concentrated in top 5 sectors** | IT, Professional Services, Healthcare, Manufacturing and Finance together account for > 50 % of postings. | `groupby(primary_category).nunique()` | Horizontal bar (top 10 sectors) |
| D2 | **Heavy recruiters vs long-tail employers** | A few companies post many ads; most hire rarely → Enterprise vs SME behavior. | `groupby(postedCompany_name)` → Top 20 | Bar / Pareto chart |
| D3 | **Executive-level roles dominate** | Market skews toward Executive/Associate roles; few C-suite positions. | `positionLevels.value_counts()` | Stacked bar (sector × level) |
| D4 | **Seasonal posting volume** | Spikes around April–May → mid-year hiring wave. | Count by month (`metadata_originalPostingDate`) | Line trend |

---

## 2️⃣ Salary & Benchmarking

| ID | Insight Title | Description | Key Metrics / Computation | Visual Suggestion |
|----|----------------|--------------|----------------------------|-------------------|
| S1 | **IT & Consulting pay the most** | Median salaries 20–30 % above market average. | `groupby(primary_category)['average_salary'].median()` | Box/Bar chart by sector |
| S2 | **Top-paying job titles** | Data Scientist, AI Engineer, Solutions Architect lead salary ranking. | `groupby(title)` (min 5 postings) | Horizontal bar (top 20 titles) |
| S3 | **Experience vs salary curve** | Pay rises steeply to ≈ 8 yrs experience, then plateaus. | `groupby(minimumYearsExperience)` | Line chart |
| S4 | **Seniority premium within sectors** | Manager/Senior roles earn 25–60 % more than Executives. | `groupby(primary_category, positionLevels)` | Clustered bar / heatmap |

---

## 3️⃣ Competition & Market Tightness

| ID | Insight Title | Description | Key Metrics / Computation | Visual Suggestion |
|----|----------------|--------------|----------------------------|-------------------|
| C1 | **High applicant pressure in IT** | IT roles receive the most applications per vacancy. | `metadata_totalNumberJobApplication / numberOfVacancies` | Bar (sector × median apps/vacancy) |
| C2 | **Hard-to-fill specialized roles** | AI/Cyber positions stay open longer and get reposted. | `days_open`, `metadata_repostCount` | Scatter / bar (top 20 titles) |
| C3 | **Quick-fill admin roles** | Admin & Ops close faster → oversupply of candidates. | Median `days_open` by sector | Box plot |

---

## 4️⃣ Skills & Emerging Trends

| ID | Insight Title | Description | Key Metrics / Computation | Visual Suggestion |
|----|----------------|--------------|----------------------------|-------------------|
| K1 | **Rise of Data & AI roles** | Month-on-month increase in postings containing “Data”, “AI”, “ML”. | `title.str.contains('Data|AI|ML')` trend | Dual line (total vs AI) |
| K2 | **AI talent spread across sectors** | Data/AI roles exist in Finance, Healthcare, Manufacturing too. | Share of AI titles per sector | Bar chart (% share) |
| K3 | **Digital transformation beyond IT** | Non-tech industries actively hire for analytics/automation skills. | Keyword freq in `title`/`categories` | Treemap / word cloud |

---

## 5️⃣ Operational / Posting Dynamics

| ID | Insight Title | Description | Key Metrics / Computation | Visual Suggestion |
|----|----------------|--------------|----------------------------|-------------------|
| O1 | **Average posting lifespan ≈ 30 days** | Typical listing open ~1 month; longer = scarce skills. | `(expiryDate – postingDate).mean()` | Histogram / violin |
| O2 | **Reposting signals hiring friction** | ≥ 2 reposts common for technical or leadership roles. | `metadata_repostCount` | Bar (# reposts × role) |
| O3 | **Mid-year peak, late-year slowdown** | Postings drop after June → seasonal pattern. | Monthly count trend | Line chart |

---

## 6️⃣ Dashboard KPI Summary

| Metric | Description | Formula |
|---------|--------------|----------|
| **Total Postings** | Count of unique job IDs | `nunique(metadata_jobPostId)` |
| **Hiring Companies** | Count of unique companies | `nunique(postedCompany_name)` |
| **Sectors Represented** | Distinct primary categories | `nunique(primary_category)` |
| **Median Salary (Overall)** | Benchmark pay level | `median(average_salary)` |
| **Avg Applications per Vacancy** | Competitiveness index | `mean(apps_per_vacancy)` |
| **Avg Days Open per Posting** | Hiring duration indicator | `mean(days_open)` |

---

## 📊 Dashboard Mapping (Phase 5 Preview)

| Dashboard Page | Related Insights | Example Visuals |
|----------------|-----------------|-----------------|
| **Overview** | D1–D3 + KPI set | KPI cards, Top Sectors, Top Companies |
| **Industry Trends** | D1, C1–C3 | Sector demand & competition plots |
| **Salary Insights** | S1–S4 | Salary benchmark charts |
| **Experience & Roles** | S3–S4, O1–O2 | Experience vs salary, seniority heatmap |
| **Skills Trends (optional)** | K1–K3 | AI/Data time-series + sector distribution |

---

## 🧾 Files Generated from Phase 4
- `notebooks/insights.ipynb` – reproducible computations  
- `reports/data/*.csv` – aggregated tables for dashboard  
- `reports/figures/*.png` – exported visual assets  
- `reports/insights_catalog.md` – this document  

---

**Prepared by:** Data Analytics Team  
**Date:** _{{ auto-generated }}_  
**Project:** Interactive Data Storytelling Dashboard – Singapore Job Market
