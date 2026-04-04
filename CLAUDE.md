# Project: Loan Default Risk Analysis
MBA Finance portfolio project — credit risk analysis using 
Kaggle's Give Me Some Credit dataset (150,000 borrowers).

## Project Goal
Identify which borrower characteristics most strongly predict 
loan default. Business audience: banking/credit risk recruiters.

## Files
- `cs-training.csv` — original raw dataset (149,999 rows, 11 cols)
- `cs-training-cleaned.csv` — cleaned dataset, ready for analysis
- All scripts go in project root

## Progress Log
- Data exploration: complete
- Data cleaning: complete (median imputation, 99th pct capping, 
  removed age=0 row)
- Core analysis: complete
  - Times 90-days late = dominant predictor (60.45% default at 3+)
  - Revolving utilization: defaulters 69% vs non-defaulters 29%
  - Age under 30: 11.73% default vs 60+ at 3.10%
  - Income alone: monthly income shows directional correlation (defaulters 
    skew lower) but poor group separation — too much overlap to use as 
    standalone predictor. Useful in combination with behavioral variables.

## Next Steps
1. Build visualizations (PNG charts for each key finding)
2. Write README business narrative
3. Push to GitHub: github.com/Ausmin787/loan-default-analysis

## Rules
- Always save outputs as files, not just terminal output
- Use pandas and matplotlib only — no unnecessary libraries
- Every chart must have a title, axis labels, and saved as PNG
- Run /clear between sessions to preserve token budget