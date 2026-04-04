import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("cs-training-cleaned.csv")

# Group: 0, 1, 2, 3+
def bucket(x):
    if x == 0:
        return "0"
    elif x == 1:
        return "1"
    elif x == 2:
        return "2"
    else:
        return "3+"

df["late_bucket"] = df["NumberOfTimes90DaysLate"].apply(bucket)

order = ["0", "1", "2", "3+"]
default_rates = (
    df.groupby("late_bucket")["SeriousDlqin2yrs"]
    .mean()
    .reindex(order) * 100
)

colors = ["steelblue", "#e6a817", "#d4541a", "#8b0000"]

fig, ax = plt.subplots(figsize=(9, 5))
fig.patch.set_facecolor("white")
ax.set_facecolor("white")

bars = ax.barh(order, default_rates.values, color=colors, height=0.55, edgecolor="none")

# Annotate bars
for bar, rate in zip(bars, default_rates.values):
    ax.text(
        bar.get_width() + 0.8,
        bar.get_y() + bar.get_height() / 2,
        f"{rate:.2f}%",
        va="center",
        ha="left",
        fontsize=11,
        fontweight="bold",
        color="#333333",
    )

# Title + subtitle
ax.set_title(
    "Delinquency History Drives Default Risk",
    fontsize=15,
    fontweight="bold",
    pad=18,
    loc="left",
    color="#1a1a1a",
)
ax.text(
    0,
    4.35,
    "60.45% of borrowers with 3+ late payments defaulted",
    fontsize=10,
    color="#666666",
    transform=ax.get_yaxis_transform(),
)

ax.set_xlabel("Default Rate (%)", fontsize=11, color="#444444")
ax.set_ylabel("Times 90+ Days Late", fontsize=11, color="#444444")

# Clean style
ax.xaxis.grid(True, color="#e0e0e0", linewidth=0.8)
ax.yaxis.grid(False)
ax.set_axisbelow(True)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.spines["left"].set_visible(False)
ax.tick_params(axis="y", length=0, labelsize=11)
ax.tick_params(axis="x", labelsize=10, color="#888888")
ax.set_xlim(0, 75)


plt.tight_layout()
plt.savefig("visuals/finding1_delinquency.png", dpi=300, bbox_inches="tight")
print("Saved: visuals/finding1_delinquency.png")
