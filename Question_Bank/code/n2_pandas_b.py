"""Notes M2: groupby, merge traps, pivot, concat and text data."""
import pandas as pd

sales = pd.DataFrame({"region": ["S", "S", "N", "N", "N", "W"], "cat": ["Tech", "Books", "Tech", "Tech", "Books", "Books"],
                      "amount": [100, 40, 70, 30, 60, 20]})

print("--- groupby: agg vs transform vs apply ---")
g = sales.groupby("region")["amount"]
print("agg   (one row per group):", g.sum().to_dict())
print("transform (same length as input):", g.transform("sum").tolist())
sales["share"] = (sales.amount / g.transform("sum")).round(2)
print("share of region total:", sales["share"].tolist())
print(sales.groupby(["region", "cat"]).agg(total=("amount", "sum"), n=("amount", "count"), avg=("amount", "mean")).reset_index().to_string(index=False))
print("size() counts rows incl. NaN; count() counts non-NaN:", sales.groupby("region").size().to_dict())
print("pivot_table:\n", sales.pivot_table(index="region", columns="cat", values="amount", aggfunc="sum", fill_value=0), sep="")
print("groupby result index is the group key unless reset_index():", sales.groupby("region")["amount"].sum().index.name)

print("\n--- merge: how, keys, traps ---")
cust = pd.DataFrame({"cid": [1, 2, 3], "name": ["Asha", "Ravi", "Meena"]})
orders = pd.DataFrame({"oid": [10, 11, 12, 13], "cid": [1, 1, 2, 9], "amt": [5, 7, 3, 4]})
for how in ("inner", "left", "right", "outer"):
    print(f"{how:<6} -> {len(pd.merge(cust, orders, on='cid', how=how))} rows")
print(pd.merge(cust, orders, on="cid", how="outer", indicator=True)[["cid", "name", "oid", "_merge"]].to_string(index=False))
a = pd.DataFrame({"k": [1, 1], "x": ["a1", "a2"]})
b = pd.DataFrame({"k": [1, 1], "y": ["b1", "b2"]})
print("many-to-many join: 2 x 2 matching keys ->", len(pd.merge(a, b, on="k")), "rows (row explosion)")
try:
    pd.merge(a, b, on="k", validate="one_to_one")
except pd.errors.MergeError as err:
    print("validate='one_to_one' catches it:", str(err)[:55], "...")
l = pd.DataFrame({"id": [1, 2], "v": [10, 20]}); r = pd.DataFrame({"id": [1, 2], "v": [1, 2]})
print("same column name in both -> suffixes:", list(pd.merge(l, r, on="id").columns), "| custom:", list(pd.merge(l, r, on="id", suffixes=("_l", "_r")).columns))
print("different key names: left_on/right_on ->", list(pd.merge(cust, orders.rename(columns={"cid": "customer"}), left_on="cid", right_on="customer").columns))
print("key dtype mismatch (text '1' vs number 1):")
try:
    pd.merge(cust.assign(cid=cust.cid.astype(str)), orders, on="cid")
except ValueError as err:
    print("   ->", str(err)[:70], "...")

print("\n--- concat and join ---")
x = pd.DataFrame({"a": [1, 2]}, index=[0, 1]); y = pd.DataFrame({"a": [3, 4]}, index=[0, 1])
print("concat axis=0 keeps duplicate index labels:", pd.concat([x, y]).index.tolist(), "| ignore_index:", pd.concat([x, y], ignore_index=True).index.tolist())
print("concat axis=1 shape:", pd.concat([x, y], axis=1).shape, "| join on index:", list(cust.set_index("cid").join(orders.set_index("cid"), how="left").columns))

print("\n--- text data (.str) ---")
t = pd.Series(["  asha NAIR ", "ravi.kumar@vit.ac.in", None, "Meena Rao"])
print("strip/title:", t.str.strip().str.title().tolist())
print("contains (NaN stays NaN):", t.str.contains("vit", case=False).tolist())
print("na=False:", t.str.contains("vit", na=False).tolist())
print("extract domain:", t.str.extract(r"@([\w.]+)", expand=False).tolist())
print("split + expand:", t.dropna().str.strip().str.split(expand=True).shape, "| len:", t.str.len().tolist())
print("replace regex:", t.str.replace(r"\s+", " ", regex=True).tolist()[:1], "| lower+startswith:", t.str.lower().str.startswith("r").tolist())
