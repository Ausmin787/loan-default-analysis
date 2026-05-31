import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("cs-training-cleaned.csv")

# Score each borrower on three signals
df["score"] = (
    (df["NumberOfTimes90DaysLate"] >= 3).astype(int) * 3
    + (df["RevolvingUtilizationOfUnsecuredLines"] > 0.75).astype(int) * 2
    + (df["age"] < 30).astype(int) * 1
)


def assign_tier(score):
    if score >= 5:
        return "High"
    elif score >= 3:
        return "Medium"
    else:
        return "Low"


df["risk_tier"] = df["score"].apply(assign_tier)

order = ["Low", "Medium", "High"]
colors = {"Low": "steelblue", "Medium": "#e6a817", "High": "#8b0000"}
bar_colors = [colors[t] for t in order]

tier_counts = df["risk_tier"].value_counts().reindex(order)
tier_pcts = tier_counts / len(df) * 100
default_rates = df.groupby("risk_tier")["SeriousDlqin2yrs"].mean().reindex(order) * 100

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
fig.patch.set_facecolor("white")

# Panel 1: Borrower distribution by tier
bars1 = ax1.bar(order, tier_pcts.values, color=bar_colors, width=0.55, edgecolor="none")

for bar, pct, count in zip(bars1, tier_pcts.values, tier_counts.values):
    ax1.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height() + 0.8,
        f"{pct:.1f}%\n({count:,})",
        ha="center",
        va="bottom",
        fontsize=10,
        fontweight="bold",
        color="#333333",
    )

ax1.set_title(
    "Borrower Distribution by Risk Tier",
    fontsize=13,
    fontweight="bold",
    loc="left",
    color="#1a1a1a",
    pad=12,
)
ax1.set_ylabel("% of Borrowers", fontsize=11, color="#444444")
ax1.set_xlabel("Risk Tier", fontsize=11, color="#444444")
ax1.set_ylim(0, max(tier_pcts.values) * 1.25)
ax1.yaxis.grid(True, color="#e0e0e0", linewidth=0.8)
ax1.set_axisbelow(True)
ax1.spines["top"].set_visible(False)
ax1.spines["right"].set_visible(False)
ax1.spines["left"].set_visible(False)
ax1.tick_params(axis="y", length=0, labelsize=11)
ax1.tick_params(axis="x", labelsize=11)

# Panel 2: Default rate per tier
bars2 = ax2.bar(order, default_rates.values, color=bar_colors, width=0.55, edgecolor="none")

for bar, rate in zip(bars2, default_rates.values):
    ax2.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height() + 0.5,
        f"{rate:.1f}%",
        ha="center",
        va="bottom",
        fontsize=11,
        fontweight="bold",
        color="#333333",
    )

ax2.set_title(
    "Default Rate by Risk Tier",
    fontsize=13,
    fontweight="bold",
    loc="left",
    color="#1a1a1a",
    pad=12,
)
ax2.set_ylabel("Default Rate (%)", fontsize=11, color="#444444")
ax2.set_xlabel("Risk Tier", fontsize=11, color="#444444")
ax2.set_ylim(0, max(default_rates.values) * 1.25)
ax2.yaxis.grid(True, color="#e0e0e0", linewidth=0.8)
ax2.set_axisbelow(True)
ax2.spines["top"].set_visible(False)
ax2.spines["right"].set_visible(False)
ax2.spines["left"].set_visible(False)
ax2.tick_params(axis="y", length=0, labelsize=11)
ax2.tick_params(axis="x", labelsize=11)

plt.tight_layout()
plt.savefig("visuals/risk_tier_distribution.png", dpi=300, bbox_inches="tight")
print("Saved: visuals/risk_tier_distribution.png")

# Print tier summary for README update
print("\nTier Summary:")
for tier in order:
    mask = df["risk_tier"] == tier
    count = mask.sum()
    pct = count / len(df) * 100
    dr = df.loc[mask, "SeriousDlqin2yrs"].mean() * 100
    print(f"  {tier}: {count:,} borrowers ({pct:.1f}%) — default rate {dr:.1f}%")
