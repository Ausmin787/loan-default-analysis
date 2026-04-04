import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

df = pd.read_csv("cs-training-cleaned.csv")

# Cap at 99th percentile
cap = df["RevolvingUtilizationOfUnsecuredLines"].quantile(0.99)
df["util_capped"] = df["RevolvingUtilizationOfUnsecuredLines"].clip(upper=cap)

non_defaulters = df[df["SeriousDlqin2yrs"] == 0]["util_capped"]
defaulters = df[df["SeriousDlqin2yrs"] == 1]["util_capped"]

fig, ax = plt.subplots(figsize=(8, 6))
fig.patch.set_facecolor("white")
ax.set_facecolor("white")

colors = ["steelblue", "#8b0000"]
labels = ["Non-Defaulters", "Defaulters"]
data = [non_defaulters, defaulters]

bp = ax.boxplot(
    data,
    patch_artist=True,
    widths=0.45,
    medianprops=dict(color="white", linewidth=2.5),
    whiskerprops=dict(linewidth=1.4, color="#555555"),
    capprops=dict(linewidth=1.4, color="#555555"),
    flierprops=dict(marker="o", markersize=2, alpha=0.3, linestyle="none"),
    boxprops=dict(linewidth=1.2),
)

for patch, color in zip(bp["boxes"], colors):
    patch.set_facecolor(color)
    patch.set_alpha(0.85)

for flier, color in zip(bp["fliers"], colors):
    flier.set(markerfacecolor=color, markeredgecolor=color)

# Annotate medians
for i, (d, color) in enumerate(zip(data, colors), start=1):
    median_val = np.median(d)
    ax.text(
        i,
        median_val + 0.015,
        f"Median: {median_val:.2f}",
        ha="center",
        va="bottom",
        fontsize=10,
        fontweight="bold",
        color="white" if median_val > 0.1 else "#333333",
    )

# 50% threshold line
ax.axhline(y=0.5, color="#444444", linestyle="--", linewidth=1.2, zorder=3)
ax.text(
    2.38,
    0.502,
    "50% utilization threshold",
    va="bottom",
    ha="right",
    fontsize=9,
    color="#444444",
)

# Title + subtitle
ax.set_title(
    "Credit Utilization Separates Defaulters from Non-Defaulters",
    fontsize=14,
    fontweight="bold",
    pad=16,
    loc="left",
    color="#1a1a1a",
)
ax.text(
    0.0,
    1.10,
    "Median utilization: 84% for defaulters vs 13% for non-defaulters",
    transform=ax.transAxes,
    fontsize=10,
    color="#666666",
    va="bottom",
)

ax.set_ylabel("Revolving Credit Utilization Rate", fontsize=11, color="#444444")
ax.set_xticks([1, 2])
ax.set_xticklabels(labels, fontsize=12)

# Clean style
ax.yaxis.grid(True, color="#e0e0e0", linewidth=0.8)
ax.xaxis.grid(False)
ax.set_axisbelow(True)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.tick_params(axis="x", length=0)
ax.tick_params(axis="y", labelsize=10, color="#888888")

plt.tight_layout()
plt.subplots_adjust(top=0.82)
plt.savefig("visuals/finding2_utilization.png", dpi=300, bbox_inches="tight")
print("Saved: visuals/finding2_utilization.png")
