"""M2-Q2  Merging, split-apply-combine, text data (FAT top-10 question 1)."""
import pandas as pd

customers = pd.DataFrame({
    "cust_id": [1, 2, 3, 4],
    "name": ["  asha NAIR", "ravi kumar ", "Meena Rao", "kabir shah"],
    "region": ["South", "North", "West", "South"],
})
orders = pd.DataFrame({
    "order_id": [101, 102, 103, 104, 105],
    "cust_id": [1, 1, 2, 3, 9],                 # 9 has no matching customer; 4 has no orders
    "category": ["Books", "Tech", "Tech", "Books", "Tech"],
    "sales": [500, 1200, 800, 300, 400],
    "profit": [50, 240, 120, 30, 40],
})

print("inner merge (only matching keys)")
print(pd.merge(customers, orders, on="cust_id", how="inner")[["cust_id", "order_id", "sales"]])
print("\nleft merge (all customers, NaN where no orders)")
print(pd.merge(customers, orders, on="cust_id", how="left")[["cust_id", "order_id", "sales"]])
print("\nouter merge row count:", len(pd.merge(customers, orders, on="cust_id", how="outer")))

print("\nconcat axis=0 (stack rows) shape:",
      pd.concat([orders.iloc[:2], orders.iloc[2:]], axis=0).shape,
      "| concat axis=1 (side by side) shape:",
      pd.concat([orders[["order_id"]], orders[["sales"]]], axis=1).shape)

# split -> apply -> combine
merged = pd.merge(customers, orders, on="cust_id", how="inner")
summary = (merged.groupby(["region", "category"])
                 .agg(total_sales=("sales", "sum"),
                      avg_profit=("profit", "mean"),
                      orders=("order_id", "count"))
                 .reset_index())
print("\ngroupby(region, category).agg(...)\n", summary, sep="")

# working with text data via the .str accessor
customers["name"] = customers["name"].str.strip().str.title()
print("\nCleaned names:", customers["name"].tolist())
print("Names containing 'sh' (case-insensitive):",
      customers.loc[customers["name"].str.contains("sh", case=False), "name"].tolist())
print("First names:", customers["name"].str.split().str[0].tolist())
