"""Sample answer M2-Q1: preprocessing, statistics and risk detection for the student performance table."""
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from sklearn.impute import SimpleImputer

df = pd.DataFrame({
    "StudentID": ["S101", "S102", "S103", "S104", "S105"],
    "Name": ["Arun", "Priya", "Kiran", "Meena", "Ravi"],
    "Department": ["CSE", "ECE", "CSE", "IT", "CSE"],
    "Attendance": [92, 85, np.nan, 78, 95],
    "InternalMarks": [45, 38, 42, np.nan, 48],
    "FinalMarks": [78, 72, 80, 68, 88]})
raw = df.copy()

print("--- 1. inspect the missing values first ---")
print(df.isna().sum().to_dict(), "| share of rows with a gap:", round(df.isna().any(axis=1).mean(), 2))

# keep a flag so that nobody forgets which numbers were filled in
for col in ["Attendance", "InternalMarks"]:
    df[col + "_filled"] = df[col].isna()
    dept_median = df.groupby("Department")[col].transform("median")      # median of the same department
    df[col] = df[col].fillna(dept_median).fillna(df[col].median())        # fall back to the overall median
print(df[["StudentID", "Department", "Attendance", "InternalMarks"]])

print("\n--- the same idea inside a modelling pipeline (fit on training rows only) ---")
imp = SimpleImputer(strategy="median").fit(raw.loc[:3, ["Attendance", "InternalMarks"]])     # rows 0-3 play the training set
print(imp.transform(raw[["Attendance", "InternalMarks"]]))

print("\n--- 2. built-in functions for statistical analysis ---")
num = ["Attendance", "InternalMarks", "FinalMarks"]
print(df[num].describe().round(2))
print(df[num].corr().round(2))
print(df.groupby("Department")["FinalMarks"].agg(["count", "mean", "max"]))

print("\n--- 3. who is at academic risk? (example thresholds, set them with the faculty) ---")
df["risk_points"] = (df["Attendance"] < 80).astype(int) + (df["InternalMarks"] < 40).astype(int) + (df["FinalMarks"] < 70).astype(int)
df["status"] = pd.cut(df["risk_points"], bins=[-1, 0, 1, 3], labels=["ok", "watch", "at risk"])
print(df[["Name", "Attendance", "InternalMarks", "FinalMarks", "risk_points", "status"]])

fig, ax = plt.subplots(1, 2, figsize=(9, 3.4))
for dept, g in df.groupby("Department"):
    ax[0].scatter(g["Attendance"], g["FinalMarks"], s=60, label=dept)
for _, r in df[df["risk_points"] > 0].iterrows():
    ax[0].annotate(r["Name"], (r["Attendance"], r["FinalMarks"]), textcoords="offset points", xytext=(6, 4))
ax[0].set_xlabel("Attendance (%)")
ax[0].set_ylabel("Final marks")
ax[0].set_title("Attendance vs final marks")
ax[0].legend()
df.groupby("Department")["FinalMarks"].mean().plot.bar(ax=ax[1], color="steelblue", rot=0)
ax[1].set_ylabel("Mean final marks")
ax[1].set_title("Mean final marks by department")
plt.tight_layout()
plt.savefig("sa_m2_q1.png", dpi=110)
print("\nsaved sa_m2_q1.png")
