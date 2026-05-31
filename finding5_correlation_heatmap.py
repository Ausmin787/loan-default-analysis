import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv("cs-training-cleaned.csv")

rename = {
    "SeriousDlqin2yrs": "Defaulted",
    "RevolvingUtilizationOfUnsecuredLines": "Revolving Util",
    "age": "Age",
    "NumberOfTime30-59DaysPastDueNotWorse": "Late 30-59",
    "DebtRatio": "Debt Ratio",
    "MonthlyIncome": "Monthly Income",
    "NumberOfOpenCreditLinesAndLoans": "Open Credits",
    "NumberOfTimes90DaysLate": "Late 90+",
    "NumberRealEstateLoansOrLines": "RE Loans",
    "NumberOfTime60-89DaysPastDueNotWorse": "Late 60-89",
    "NumberOfDependents": "Dependents",
}

df = df.rename(columns=rename)
corr = df.corr()

fig, ax = plt.subplots(figsize=(11, 9))
fig.patch.set_facecolor("white")

sns.heatmap(
    corr,
    annot=True,
    fmt=".2f",
    cmap="RdBu_r",
    center=0,
    vmin=-1,
    vmax=1,
    linewidths=0.5,
    linecolor="#e0e0e0",
    annot_kws={"size": 9},
    ax=ax,
    cbar_kws={"shrink": 0.8, "label": "Pearson r"},
)

ax.set_title(
    "Feature Correlation Matrix — All 10 Variables + Target",
    fontsize=14,
    fontweight="bold",
    pad=16,
    loc="left",
    color="#1a1a1a",
)

ax.tick_params(axis="x", labelsize=10, rotation=45)
ax.tick_params(axis="y", labelsize=10, rotation=0)

plt.tight_layout()
plt.savefig("visuals/correlation_heatmap.png", dpi=300, bbox_inches="tight")
print("Saved: visuals/correlation_heatmap.png")
