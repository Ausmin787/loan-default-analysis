# Loan Default Risk Analysis

Credit risk analysis identifying the behavioral and demographic drivers of borrower default across 150,000 accounts. Using Kaggle's Give Me Some Credit dataset, the analysis pinpoints delinquency history and revolving utilization as the strongest predictors of default — with income alone proving too weak to use standalone.

---

## Key Findings

1. **90-Days-Late Dominant Predictor:** 60.45% default rate at 3+ late payments vs 4.63% for clean records — a 13x difference that makes payment history the clearest early warning signal available.
2. **Revolving Utilization Gap:** Defaulters median 84% utilization vs 13% for non-defaulters. Near-maximum balances signal financial stress and limited buffer against income shocks.
3. **Age Effect:** Under-30 group 11.73% default rate vs 3.10% for 60+ age group — a monotonic decline reflecting shorter credit histories and less financial stability.
4. **Income Weak Standalone:** Income alone is a poor predictor without behavioral signals. Defaulters skew lower-income but distributions overlap too heavily for reliable separation.

---

## Dataset

| Field | Detail |
|-------|--------|
| Source | Kaggle — Give Me Some Credit competition |
| Rows | 150,000 borrowers |
| Columns | 11 (10 features + 1 target) |
| Target | `SeriousDlqin2yrs` — 90+ day delinquency within 2 years |
| Default rate | 6.68% |

---

## Tech Stack

- **Analysis:** Python (pandas, matplotlib, seaborn, numpy)
- **Environment:** SQLite for structured querying
- **CI:** GitHub Actions (analysis reproducibility workflow)

---

## Project Structure

```
loan-default-analysis/
├── finding1_delinquency.py      # Chart: delinquency vs default rate
├── finding2_utilization.py      # Chart: revolving utilization boxplot
├── finding3_age.py              # Chart: default rate by age group
├── finding4_income.py           # Chart: income KDE overlay
├── visuals/
│   ├── finding1_delinquency.png
│   ├── finding2_utilization.png
│   ├── finding3_age.png
│   └── finding4_income.png
├── cs-training.csv              # Raw dataset (excluded from git)
├── cs-training-cleaned.csv      # Cleaned dataset (excluded from git)
├── CLAUDE.md                    # Project context and session notes
└── README.md
```

---

## Visualizations

- `finding1_delinquency.png` — Default rate by number of 90-days-late payments
- `finding2_utilization.png` — Revolving utilization distribution: defaulters vs non-defaulters
- `finding3_age.png` — Default rate by age group
- `finding4_income.png` — Monthly income KDE overlay: defaulters vs non-defaulters

---

## How to Run

1. Clone the repo: `git clone https://github.com/Ausmin787/loan-default-analysis.git`
2. Install dependencies: `pip install pandas matplotlib seaborn numpy`
3. Run each analysis script:
   ```bash
   python finding1_delinquency.py
   python finding2_utilization.py
   python finding3_age.py
   python finding4_income.py
   ```
4. Charts saved to `visuals/`

---

## Author

Data Analyst Portfolio Project | [github.com/Ausmin787/loan-default-analysis](https://github.com/Ausmin787/loan-default-analysis)

**Ausmin** — Data Analytics, Finance minor | DBS Global University  
LinkedIn: [ausmindeb](https://www.linkedin.com/in/ausmindeb) | Email: ausmindeb32@gmail.com  
Open to internship opportunities in data analytics, credit risk, and financial modeling.
