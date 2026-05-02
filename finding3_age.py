import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("cs-training-cleaned.csv")


def age_bucket(age):
    if age < 30:
        return "Under 30"
    elif age < 45:
        return "30-45"
    elif age < 60:
        return "45-60"
    else:
        return "60+"


df["age_group"] = df["age"].apply(age_bucket)

order = ["Under 30", "30-45", "45-60", "60+"]
colors = ["#8b0000", "#d4541a", "#e6a817", "steelblue"]

default_rates = df.groupby("age_group")["SeriousDlqin2yrs"].mean().reindex(order) * 100

fig, ax = plt.subplots(figsize=(9, 5))
fig.patch.set_facecolor("white")
ax.set_facecolor("white")

bars = ax.bar(order, default_rates.values, color=colors, width=0.55, edgecolor="none")

# Annotate bars
for bar, rate in zip(bars, default_rates.values):
    ax.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height() + 0.15,
        f"{rate:.2f}%",
        ha="center",
        va="bottom",
        fontsize=11,
        fontweight="bold",
        color="#333333",
    )

# Title + subtitle
ax.set_title(
    "Younger Borrowers Default at Nearly 4x the Rate of Older Borrowers",
    fontsize=13,
    fontweight="bold",
    pad=30,
    loc="left",
    color="#1a1a1a",
)
ax.text(
    0.0,
    1.07,
    "Under-30 borrowers: 11.73% default vs 3.10% for age 60+",
    transform=ax.transAxes,
    fontsize=10,
    color="#666666",
    va="bottom",
)

ax.set_xlabel("Age Group", fontsize=11, color="#444444")
ax.set_ylabel("Default Rate (%)", fontsize=11, color="#444444")
ax.set_ylim(0, default_rates.max() * 1.25)

# Clean style
ax.yaxis.grid(True, color="#e0e0e0", linewidth=0.8)
ax.xaxis.grid(False)
ax.set_axisbelow(True)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.tick_params(axis="x", length=0, labelsize=11)
ax.tick_params(axis="y", labelsize=10, color="#888888")

plt.tight_layout()
plt.subplots_adjust(top=0.82)
plt.savefig("visuals/finding3_age.png", dpi=300, bbox_inches="tight")
print("Saved: visuals/finding3_age.png")
