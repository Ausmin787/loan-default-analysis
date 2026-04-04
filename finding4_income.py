import pandas as pd
import matplotlib.pyplot as plt
from numpy import exp
import numpy as np

df = pd.read_csv("cs-training-cleaned.csv")

# Cap at 99th percentile, drop NaN
cap = df["MonthlyIncome"].quantile(0.99)
df["income_capped"] = df["MonthlyIncome"].clip(upper=cap)
df = df.dropna(subset=["income_capped"])

non_def = df[df["SeriousDlqin2yrs"] == 0]["income_capped"]
defaulters = df[df["SeriousDlqin2yrs"] == 1]["income_capped"]

x = np.linspace(0, cap, 500)

def kde(data, x, bw=None):
    data = np.asarray(data)
    n = len(data)
    if bw is None:
        bw = 1.06 * data.std() * n ** (-0.2)
    diff = (x[:, None] - data[None, :]) / bw
    return exp(-0.5 * diff ** 2).sum(axis=1) / (n * bw * np.sqrt(2 * np.pi))

y_non = kde(non_def, x)
y_def = kde(defaulters, x)

fig, ax = plt.subplots(figsize=(9, 5))
fig.patch.set_facecolor("white")
ax.set_facecolor("white")

ax.fill_between(x, y_non, alpha=0.6, color="steelblue", label="Non-Defaulters")
ax.plot(x, y_non, color="steelblue", linewidth=1.8)

ax.fill_between(x, y_def, alpha=0.6, color="#8b0000", label="Defaulters")
ax.plot(x, y_def, color="#8b0000", linewidth=1.8)

# Overlap annotation — point to mid-low income range where curves overlap
ax.annotate(
    "Heavy overlap = weak separation",
    xy=(3500, kde(non_def, np.array([3500]))[0] * 0.55),
    xytext=(6500, kde(non_def, np.array([3500]))[0] * 0.75),
    fontsize=10,
    color="#333333",
    arrowprops=dict(arrowstyle="->", color="#555555", lw=1.2),
    bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="#cccccc", lw=0.8),
)

# Legend
ax.legend(fontsize=10, frameon=False, loc="upper right")

# Title + subtitle
ax.set_title(
    "Monthly Income Alone Is a Weak Default Predictor",
    fontsize=13,
    fontweight="bold",
    pad=30,
    loc="left",
    color="#1a1a1a",
)
ax.text(
    0.0,
    1.07,
    "Distributions overlap too heavily for income to be a reliable standalone predictor",
    transform=ax.transAxes,
    fontsize=10,
    color="#666666",
    va="bottom",
)

ax.set_xlabel("Monthly Income (USD)", fontsize=11, color="#444444")
ax.set_ylabel("Density", fontsize=11, color="#444444")

ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"${x:,.0f}"))

# Clean style
ax.yaxis.grid(True, color="#e0e0e0", linewidth=0.8)
ax.xaxis.grid(False)
ax.set_axisbelow(True)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.tick_params(axis="x", labelsize=10, color="#888888")
ax.tick_params(axis="y", labelsize=10, color="#888888")

plt.tight_layout()
plt.subplots_adjust(top=0.82)
plt.savefig("visuals/finding4_income.png", dpi=300, bbox_inches="tight")
print("Saved: visuals/finding4_income.png")
