"""Notes M2: pandas Series/DataFrame, indexing, filtering, missing values and the traps."""
import warnings

import numpy as np
import pandas as pd

pd.set_option("display.width", 100)

print("--- Series: labelled array, alignment on the index ---")
s1 = pd.Series([10, 20, 30], index=["a", "b", "c"])
s2 = pd.Series([1, 2, 3], index=["b", "c", "d"])
print("s1 + s2 aligns by label (not position):\n", s1 + s2, sep="")
print("s1.add(s2, fill_value=0):", s1.add(s2, fill_value=0).tolist())
print("dtype:", s1.dtype, "| s1['b']:", s1["b"], "| s1.iloc[1]:", s1.iloc[1], "| s1[s1 > 15].index.tolist():", s1[s1 > 15].index.tolist())

df = pd.DataFrame({"name": ["Asha", "Ravi", "Meena", "Kabir", "Sneha"], "age": [22, 31, 27, 35, 24],
                   "city": ["Chennai", "Delhi", "Pune", "Delhi", "Chennai"], "score": [88.5, 72.0, np.nan, 65.5, 91.0]})
print("\n--- DataFrame basics ---")
print(df)
print("shape", df.shape, "| dtypes:", df.dtypes.astype(str).to_dict())
print("describe (numeric):\n", df.describe().round(2), sep="")
print("value_counts:", df["city"].value_counts().to_dict(), "| nunique:", df["city"].nunique())

print("\n--- selecting: [], loc, iloc, boolean masks ---")
print("df['age'] is a", type(df["age"]).__name__, "| df[['age']] is a", type(df[["age"]]).__name__)
print("loc[1:2] rows:", df.loc[1:2, "name"].tolist(), "| iloc[1:2] rows:", df.iloc[1:2, 0].tolist())
print("age>25 and Delhi:", df[(df.age > 25) & (df.city == "Delhi")]["name"].tolist())
try:
    df[df.age > 25 and df.city == "Delhi"]
except ValueError as err:
    print("using 'and' instead of '&' ->", str(err)[:60], "...")
print("isin:", df[df.city.isin(["Pune", "Delhi"])]["name"].tolist(), "| between:", df[df.age.between(24, 31)]["name"].tolist(),
      "| query:", df.query("age > 30 and city == 'Delhi'")["name"].tolist())

print("\n--- chained assignment trap ---")
d2 = df.copy()
with warnings.catch_warnings(record=True) as w:
    warnings.simplefilter("always")
    d2[d2.age > 30]["score"] = 0           # assigns to a temporary copy
    print("chained d2[mask]['score'] = 0 changed the data?", (d2["score"] == 0).any(),
          "| warning:", w[0].category.__name__ if w else "none")
d2.loc[d2.age > 30, "score"] = 0           # the correct way: one .loc call
print("d2.loc[mask, 'score'] = 0 changed the data?", (d2["score"] == 0).any())

print("\n--- missing values ---")
print("NaN == NaN:", np.nan == np.nan, "| isna count:", df["score"].isna().sum(), "| mean skips NaN:", round(df["score"].mean(), 2),
      "| sum of [1, NaN]:", pd.Series([1, np.nan]).sum())
print("fillna(mean):", df["score"].fillna(df["score"].mean()).round(2).tolist())
print("ffill:", df["score"].ffill().tolist(), "| interpolate:", df["score"].interpolate().round(2).tolist())
print("dropna(subset=['score']) keeps", len(df.dropna(subset=["score"])), "of", len(df), "rows | dropna(thresh=4) keeps", len(df.dropna(thresh=4)))
print("int column with NaN becomes float:", pd.Series([1, 2, np.nan]).dtype, "| nullable Int64:", pd.Series([1, 2, None], dtype="Int64").tolist())
print("df.replace / where:", df["age"].where(df["age"] > 25, other=0).tolist())

print("\n--- add / drop / rename / sort / apply ---")
d3 = df.assign(grade=lambda x: pd.cut(x.score, [0, 70, 85, 100], labels=["C", "B", "A"]))
print(d3[["name", "score", "grade"]].sort_values("score", ascending=False, na_position="last").to_string(index=False))
print("rename:", list(df.rename(columns={"name": "student"}).columns), "| drop:", list(df.drop(columns=["city"]).columns))
print("map:", df["city"].map({"Chennai": "TN", "Delhi": "DL"}).tolist(), "(unmapped -> NaN)")
print("apply row-wise:", df.apply(lambda r: f"{r['name']}:{r['age']}", axis=1).tolist()[:2], "| axis=0 means down the columns")
print("astype:", df["age"].astype("float").dtype, "| to_numeric(errors='coerce'):", pd.to_numeric(pd.Series(["1", "x", "3"]), errors="coerce").tolist())
print("datetime:", pd.to_datetime("2026-07-06").day_name(), "|", pd.to_datetime(pd.Series(["2026-01-31", "2026-02-28"])).dt.month.tolist())
