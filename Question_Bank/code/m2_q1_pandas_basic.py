"""M2-Q1  Pandas basics, cleaning and scaling (Lab experiments 1 and 2)."""
import numpy as np
import pandas as pd

# ---------------------------------------------------------------- Lab 1
df = pd.DataFrame({
    "Name": ["Asha", "Ravi", "Meena", "Kabir", "Sneha"],
    "Age": [22, 31, 27, 35, 24],
    "City": ["Chennai", "Delhi", "Pune", "Mumbai", "Chennai"],
})
print("1. select Name and Age\n", df[["Name", "Age"]], sep="")
print("\n2. filter Age > 25\n", df[df["Age"] > 25], sep="")
df["Country"] = "India"
print("\n3. add Country, sort by Age (descending)\n", df.sort_values("Age", ascending=False), sep="")
print("\n4. average age:", df["Age"].mean())
print("\n.loc (label) vs .iloc (position)")
print("   df.loc[1:2, 'Name'] ->", df.loc[1:2, "Name"].tolist(), "   (end label INCLUDED)")
print("   df.iloc[1:2, 0]     ->", df.iloc[1:2, 0].tolist(), "           (end position EXCLUDED)")

# ---------------------------------------------------------------- Lab 2
raw = pd.DataFrame({
    "Name": ["Asha", None, "Meena", "Kabir", "Sneha"],
    "Age": [22, 31, np.nan, 35, 40],
    "City": ["Chennai", "Delhi", "Pune", None, "Chennai"],
})
print("\n\nRaw data with missing values\n", raw, sep="")
print("\nmissing per column\n", raw.isna().sum(), sep="")

clean = raw.copy()
clean["Age"] = clean["Age"].fillna(clean["Age"].mean())         # mean of 22, 31, 35, 40 = 32.0
clean = clean.dropna(subset=["Name", "City"])                    # drop rows missing Name or City
clean["Age"] = clean["Age"].round().astype(int)                  # float -> int
print("\nAfter fillna / dropna / astype(int)\n", clean, sep="")

a = clean["Age"]
clean["Age_scaled"] = (a - a.min()) / (a.max() - a.min())        # min-max scaling to [0, 1]
print("\nMin-max scaled Age\n", clean, sep="")
