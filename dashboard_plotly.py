import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

df = pd.read_csv("cs-training-cleaned.csv")

# --- Chart 1: Default rate by delinquency bucket ---
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
order_late = ["0", "1", "2", "3+"]
bar_colors = ["#4682B4", "#e6a817", "#d4541a", "#8b0000"]
default_rates_late = df.groupby("late_bucket")["SeriousDlqin2yrs"].mean().reindex(order_late) * 100
counts_late = df.groupby("late_bucket")["SeriousDlqin2yrs"].count().reindex(order_late)

# --- Chart 2: Revolving utilization boxplot (cap at 1.5 for display) ---
df_util = df[df["RevolvingUtilizationOfUnsecuredLines"] <= 1.5].copy()
util_defaulted = df_util[df_util["SeriousDlqin2yrs"] == 1]["RevolvingUtilizationOfUnsecuredLines"]
util_retained = df_util[df_util["SeriousDlqin2yrs"] == 0]["RevolvingUtilizationOfUnsecuredLines"]

# --- Chart 3: Default rate by age group ---
bins = [0, 29, 39, 49, 59, 69, 120]
labels = ["<30", "30-39", "40-49", "50-59", "60-69", "70+"]
df["age_group"] = pd.cut(df["age"], bins=bins, labels=labels)
age_dr = df.groupby("age_group", observed=True)["SeriousDlqin2yrs"].mean() * 100
age_count = df.groupby("age_group", observed=True)["SeriousDlqin2yrs"].count()

# --- Build dashboard ---
fig = make_subplots(
    rows=2,
    cols=2,
    subplot_titles=(
        "Default Rate by Delinquency History",
        "Revolving Utilization by Default Status",
        "Default Rate by Age Group",
        "",
    ),
    specs=[
        [{"type": "bar"}, {"type": "box"}],
        [{"type": "scatter", "colspan": 2}, None],
    ],
    vertical_spacing=0.18,
    horizontal_spacing=0.1,
)

# Chart 1 — Bar: delinquency vs default rate
fig.add_trace(
    go.Bar(
        x=order_late,
        y=default_rates_late.values,
        marker_color=bar_colors,
        text=[f"{r:.1f}%" for r in default_rates_late.values],
        textposition="outside",
        hovertemplate="<b>%{x} late payments</b><br>Default rate: %{y:.1f}%<br>Borrowers: "
        + "<br>".join([f"{c:,}" for c in counts_late.values])
        + "<extra></extra>",
        customdata=counts_late.values,
        showlegend=False,
    ),
    row=1,
    col=1,
)

# Fix hover to show per-bar count
fig.data[-1].hovertemplate = (
    "<b>%{x} late payments</b><br>"
    "Default rate: %{y:.1f}%<br>"
    "Borrowers: %{customdata:,}<extra></extra>"
)

# Chart 2 — Box: revolving utilization
fig.add_trace(
    go.Box(
        y=util_retained,
        name="Did Not Default",
        marker_color="#4682B4",
        boxmean=True,
        hovertemplate="<b>Did Not Default</b><br>Utilization: %{y:.2f}<extra></extra>",
    ),
    row=1,
    col=2,
)
fig.add_trace(
    go.Box(
        y=util_defaulted,
        name="Defaulted",
        marker_color="#8b0000",
        boxmean=True,
        hovertemplate="<b>Defaulted</b><br>Utilization: %{y:.2f}<extra></extra>",
    ),
    row=1,
    col=2,
)

# Chart 3 — Line: default rate by age group
fig.add_trace(
    go.Scatter(
        x=labels,
        y=age_dr.values,
        mode="lines+markers",
        line=dict(color="#4682B4", width=2.5),
        marker=dict(size=9, color="#4682B4"),
        customdata=age_count.values,
        hovertemplate=(
            "<b>Age group: %{x}</b><br>"
            "Default rate: %{y:.1f}%<br>"
            "Borrowers: %{customdata:,}<extra></extra>"
        ),
        showlegend=False,
    ),
    row=2,
    col=1,
)

fig.update_layout(
    title=dict(
        text="Loan Default Risk — Interactive Analysis Dashboard",
        font=dict(size=18, color="#1a1a1a"),
        x=0,
        xanchor="left",
    ),
    paper_bgcolor="white",
    plot_bgcolor="white",
    font=dict(family="Arial", size=12, color="#333333"),
    height=750,
    legend=dict(x=0.57, y=0.47, bgcolor="rgba(255,255,255,0.8)"),
)

fig.update_xaxes(showgrid=False)
fig.update_yaxes(gridcolor="#e0e0e0", gridwidth=0.8)
fig.update_yaxes(title_text="Default Rate (%)", row=1, col=1)
fig.update_yaxes(title_text="Revolving Utilization", row=1, col=2)
fig.update_yaxes(title_text="Default Rate (%)", row=2, col=1)
fig.update_xaxes(title_text="Times 90+ Days Late", row=1, col=1)
fig.update_xaxes(title_text="Age Group", row=2, col=1)

fig.write_html("visuals/loan_risk_dashboard.html", include_plotlyjs="cdn")
print("Saved: visuals/loan_risk_dashboard.html")
