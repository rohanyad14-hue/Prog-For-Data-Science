"""Sample HOT questions, Module 2 - questions 1 and 2 (student performance, customer purchase patterns)."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

pd.set_option("display.width", 110)

# =============================================================== Question 1
df = pd.DataFrame({"StudentID": ["S101", "S102", "S103", "S104", "S105"], "Name": ["Arun", "Priya", "Kiran", "Meena", "Ravi"],
                   "Department": ["CSE", "ECE", "CSE", "IT", "CSE"], "Attendance": [92, 85, np.nan, 78, 95],
                   "Internal": [45, 38, 42, np.nan, 48], "Final": [78, 72, 80, 68, 88]})
print("--- Q1 step 1: inspect the data and the missing values ---")
print(df.dtypes.astype(str).to_dict())
print("missing per column:", df.isna().sum().to_dict(), "| rows with any missing:", df[df.isna().any(axis=1)].Name.tolist())
print("NaN trap: (Attendance < 80) for Kiran is", bool((df.Attendance < 80)[2]), "-> a missing value is silently NOT flagged")

print("\n--- Q1 step 2: missing-value strategies compared ---")
overall_mean_att, overall_med_int = df.Attendance.mean(), df.Internal.median()
dept_att = df.groupby("Department")["Attendance"].transform("mean")
print(f"Kiran attendance: overall mean {overall_mean_att:.2f} | CSE mean {dept_att[2]:.2f} (Arun 92, Ravi 95)")
print(f"Meena internal  : overall median {overall_med_int:.2f} | IT has no other student, so a department statistic is impossible -> fall back to the overall median")
clean = df.copy()
clean["Attendance_missing"] = clean.Attendance.isna().astype(int)
clean["Internal_missing"] = clean.Internal.isna().astype(int)
clean["Attendance"] = clean.Attendance.fillna(clean.groupby("Department")["Attendance"].transform("mean"))
clean["Internal"] = clean.Internal.fillna(clean.groupby("Department")["Internal"].transform("median")).fillna(df.Internal.median())
print(clean[["Name", "Department", "Attendance", "Internal", "Final", "Attendance_missing", "Internal_missing"]].to_string(index=False))

print("\n--- Q1 step 3: built-in functions for statistical analysis ---")
num = clean[["Attendance", "Internal", "Final"]]
print(num.describe().round(2).loc[["count", "mean", "std", "min", "50%", "max"]])
print("mean by department:\n", clean.groupby("Department")[["Attendance", "Internal", "Final"]].mean().round(2), sep="")
print("correlation with Final marks:", num.corr()["Final"].drop("Final").round(3).to_dict())

print("\n--- Q1 step 4: academic-risk rule (any trigger) ---")
rules = pd.DataFrame({"low_attendance (<80)": clean.Attendance < 80, "low_internal (<40)": clean.Internal < 40, "low_final (<70)": clean.Final < 70})
clean["risk_flags"] = rules.sum(axis=1)
clean["at_risk"] = clean.risk_flags >= 1
print(pd.concat([clean[["Name"]], rules, clean[["risk_flags"]]], axis=1).to_string(index=False))
print("students at academic risk:", clean.loc[clean.at_risk, "Name"].tolist())

print("\n--- Q1 step 5: prepare for predictive modelling ---")
X = pd.get_dummies(clean[["Department", "Attendance", "Internal"]], columns=["Department"], dtype=int)
Xs = (X[["Attendance", "Internal"]] - X[["Attendance", "Internal"]].min()) / (X[["Attendance", "Internal"]].max() - X[["Attendance", "Internal"]].min())
print("features after one-hot encoding Department and min-max scaling the numbers:\n", pd.concat([Xs.round(2), X.drop(columns=["Attendance", "Internal"])], axis=1).to_string(index=False), sep="")
print("drop identifiers (StudentID, Name) before modelling; target = Final")

fig, ax = plt.subplots(1, 3, figsize=(11, 3.3))
colors = ["#d9534f" if r else "#2f6db5" for r in clean.at_risk]
ax[0].bar(clean.Name, clean.Final, color=colors); ax[0].axhline(70, ls="--", color="grey"); ax[0].set_title("Final marks (red = at risk)"); ax[0].set_ylim(50, 95)
ax[1].scatter(clean.Attendance, clean.Final, c=colors, s=50)
for _, r in clean.iterrows():
    ax[1].annotate(r.Name, (r.Attendance, r.Final), textcoords="offset points", xytext=(4, 4), fontsize=8)
ax[1].axvline(80, ls="--", color="grey"); ax[1].set_xlabel("Attendance (%)"); ax[1].set_ylabel("Final marks"); ax[1].set_title("Attendance vs final marks")
im = ax[2].imshow(num.corr(), cmap="Blues", vmin=0, vmax=1); ax[2].set_xticks(range(3)); ax[2].set_yticks(range(3))
ax[2].set_xticklabels(num.columns, fontsize=7, rotation=20); ax[2].set_yticklabels(num.columns, fontsize=7); ax[2].set_title("Correlation heatmap")
for i in range(3):
    for j in range(3):
        ax[2].text(j, i, f"{num.corr().iloc[i, j]:.2f}", ha="center", va="center", fontsize=8)
fig.tight_layout(); fig.savefig("hot_m2_q1.png", dpi=140)
print("saved hot_m2_q1.png")

# =============================================================== Question 2
c = pd.DataFrame({"CustomerID": ["C101", "C102", "C103", "C104", "C105"], "Age": [22, 35, 28, 42, 30],
                  "City": ["Chennai", "Bangalore", "Chennai", "Hyderabad", "Chennai"], "Product": ["Laptop", "Mobile", "Laptop", "Tablet", "Mobile"],
                  "Amount": [65000, 25000, 70000, 18000, 22000]})
print("\n\n--- Q2 step 1: premium-product segment by filtering ---")
premium = c[c.Amount >= 50000]
print("Amount >= 50000:", premium.CustomerID.tolist(), "| threshold from data, 75th percentile =", c.Amount.quantile(0.75), "->", c[c.Amount >= c.Amount.quantile(0.75)].CustomerID.tolist())
seg = c[(c.Product == "Laptop") & (c.Age.between(20, 35))]
print("combined filter Product == Laptop and Age 20..35:", seg[["CustomerID", "Age", "City", "Amount"]].to_dict("records"))
print("loc extraction of just the contact fields:", c.loc[c.Amount >= 50000, ["CustomerID", "City"]].values.tolist())
print("query form:", c.query("Product == 'Laptop' and Amount > 60000").CustomerID.tolist())

print("\n--- Q2 step 2: text-data operations for city-wise preferences ---")
messy = pd.Series([" chennai", "CHENNAI ", "Bangalore", "bengaluru", "hyderabad"])
print("standardise with .str.strip().str.title():", messy.str.strip().str.title().tolist(), "| 'bengaluru' still differs from 'Bangalore': map synonyms with .replace")
c["City"] = c.City.str.strip().str.title()
print("contains 'chen':", c[c.City.str.contains("chen", case=False)].CustomerID.tolist(), "| city name lengths:", c.City.str.len().tolist())
print("city x product counts:\n", pd.crosstab(c.City, c.Product), sep="")

print("\n--- Q2 step 3: business insights ---")
by_city = c.groupby("City").agg(customers=("CustomerID", "count"), revenue=("Amount", "sum"), avg_spend=("Amount", "mean")).sort_values("revenue", ascending=False)
by_city["share_%"] = (100 * by_city.revenue / by_city.revenue.sum()).round(1)
print(by_city.round({"avg_spend": 0}).to_string())
by_prod = c.groupby("Product").Amount.agg(["count", "sum", "mean"]).sort_values("sum", ascending=False)
by_prod["share_%"] = (100 * by_prod["sum"] / by_prod["sum"].sum()).round(1)
print(by_prod.round({"mean": 0}).to_string())
c["AgeGroup"] = pd.cut(c.Age, [17, 25, 35, 60], labels=["18-25", "26-35", "36+"])
print("average spend by age group:", c.groupby("AgeGroup", observed=True).Amount.mean().round(0).to_dict())
print("total revenue:", c.Amount.sum(), "| premium customers' share of revenue: %.1f%%" % (100 * premium.Amount.sum() / c.Amount.sum()))

fig, ax = plt.subplots(1, 3, figsize=(11, 3.3))
by_city.revenue.plot.bar(ax=ax[0], color="#2f6db5", rot=20); ax[0].set_title("Revenue by city")
pd.crosstab(c.City, c.Product).plot.bar(stacked=True, ax=ax[1], rot=20); ax[1].set_title("Products bought per city"); ax[1].legend(fontsize=7)
ax[2].scatter(c.Age, c.Amount, c=["#d9534f" if a >= 50000 else "#2f6db5" for a in c.Amount], s=60)
for _, r in c.iterrows():
    ax[2].annotate(r.CustomerID, (r.Age, r.Amount), textcoords="offset points", xytext=(4, 4), fontsize=8)
ax[2].set_xlabel("Age"); ax[2].set_ylabel("Amount"); ax[2].set_title("Age vs amount (red = premium)")
fig.tight_layout(); fig.savefig("hot_m2_q2.png", dpi=140)
print("saved hot_m2_q2.png")
