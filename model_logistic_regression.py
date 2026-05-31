import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    roc_auc_score,
    roc_curve,
    classification_report,
)
from sklearn.preprocessing import StandardScaler

df = pd.read_csv("cs-training-cleaned.csv")

features = [
    "NumberOfTimes90DaysLate",
    "RevolvingUtilizationOfUnsecuredLines",
    "age",
]
target = "SeriousDlqin2yrs"

X = df[features]
y = df[target]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# class_weight="balanced" compensates for the imbalanced dataset (~6.7% default rate)
model = LogisticRegression(class_weight="balanced", max_iter=1000, random_state=42)
model.fit(X_train_scaled, y_train)

y_pred = model.predict(X_test_scaled)
y_prob = model.predict_proba(X_test_scaled)[:, 1]

accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred)
recall = recall_score(y_test, y_pred)
roc_auc = roc_auc_score(y_test, y_prob)

print("--- Model Performance ---")
print(f"Accuracy:  {accuracy:.4f}")
print(f"Precision: {precision:.4f}")
print(f"Recall:    {recall:.4f}")
print(f"ROC-AUC:   {roc_auc:.4f}")
print("\n--- Classification Report ---")
print(classification_report(y_test, y_pred, target_names=["No Default", "Default"]))

print("--- Feature Coefficients (scaled) ---")
for feat, coef in zip(features, model.coef_[0]):
    print(f"  {feat}: {coef:.4f}")

# ROC Curve
fpr, tpr, _ = roc_curve(y_test, y_prob)

fig, ax = plt.subplots(figsize=(8, 6))
fig.patch.set_facecolor("white")
ax.set_facecolor("white")

ax.plot(fpr, tpr, color="#4682B4", lw=2.5, label=f"Logistic Regression (AUC = {roc_auc:.3f})")
ax.plot([0, 1], [0, 1], color="#aaaaaa", lw=1.5, linestyle="--", label="Random Classifier")

ax.set_title(
    "ROC Curve — Logistic Regression Default Prediction",
    fontsize=14,
    fontweight="bold",
    loc="left",
    color="#1a1a1a",
    pad=16,
)
ax.set_xlabel("False Positive Rate", fontsize=11, color="#444444")
ax.set_ylabel("True Positive Rate (Recall)", fontsize=11, color="#444444")
ax.legend(fontsize=11, loc="lower right")
ax.xaxis.grid(True, color="#e0e0e0", linewidth=0.8)
ax.yaxis.grid(True, color="#e0e0e0", linewidth=0.8)
ax.set_axisbelow(True)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.set_xlim(0, 1)
ax.set_ylim(0, 1.02)

plt.tight_layout()
plt.savefig("visuals/roc_curve.png", dpi=300, bbox_inches="tight")
print("\nSaved: visuals/roc_curve.png")
