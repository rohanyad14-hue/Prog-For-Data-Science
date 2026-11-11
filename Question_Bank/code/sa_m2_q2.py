"""Sample answer M2-Q2: filtering, text operations and insights for the customer purchase table."""
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

df = pd.DataFrame({
    "CustomerID": ["C101", "C102", "C103", "C104", "C105"],
    "Age": [22, 35, 28, 42, 30],
    "City": ["Chennai", "Bangalore", "Chennai", "Hyderabad", "Chennai"],
    "Product": ["Laptop", "Mobile", "Laptop", "Tablet", "Mobile"],
    "Amount": [65000, 25000, 70000, 18000, 22000]})

print("--- 1. the premium-product segment ---")
threshold = df["Amount"].quantile(0.75)                       # top quarter of the order values
premium = df[df["Amount"] >= threshold]
print("threshold:", threshold)
print(premium[["CustomerID", "Age", "City", "Product", "Amount"]])
print("same result with query():", df.query("Amount >= @threshold")["CustomerID"].tolist())
print("segment profile: mean age", premium["Age"].mean(), "| cities", premium["City"].unique().tolist(), "| products", premium["Product"].unique().tolist())
print("laptop buyers by extraction:", df.loc[df["Product"] == "Laptop", ["CustomerID", "City"]].values.tolist())

print("\n--- 2. text operations ---")
messy = pd.Series([" chennai", "CHENNAI ", "Bangalore", "bengaluru", "hyderabad"])
tidy = messy.str.strip().str.title().replace({"Bengaluru": "Bangalore"})
print(tidy.tolist())
print("starts with Chen:", df["City"].str.contains("^Chen", case=False, regex=True).tolist())
reviews = pd.Series(["Great laptop, fast delivery in Chennai", "Mobile screen cracked, Bangalore store", "Tablet is fine"])
print("mentions laptop:", reviews.str.contains("laptop", case=False).tolist())
print("city found in text:", reviews.str.extract(r"(Chennai|Bangalore|Hyderabad)")[0].tolist())
print(pd.crosstab(df["City"], df["Product"]))
print("most bought product per city:")
print(df.groupby("City")["Product"].agg(lambda s: s.mode().iat[0]))

print("\n--- 3. business insights ---")
by_city = df.groupby("City")["Amount"].agg(orders="count", revenue="sum", average="mean")
by_product = df.groupby("Product")["Amount"].sum().sort_values(ascending=False)
print(by_city)
print((by_product / by_product.sum() * 100).round(1).to_dict(), "(% of revenue)")
print("average order value:", df["Amount"].mean(), "| Chennai share of customers:", round((df["City"] == "Chennai").mean() * 100), "%")
print("correlation age vs amount:", round(df["Age"].corr(df["Amount"]), 2), "(only 5 rows, treat as a hint)")

fig, ax = plt.subplots(1, 3, figsize=(11, 3.2))
by_product.plot.bar(ax=ax[0], color="steelblue", rot=0)
ax[0].set_title("Revenue by product")
pd.crosstab(df["City"], df["Product"]).plot.bar(stacked=True, ax=ax[1], rot=0)
ax[1].set_title("Orders by city and product")
for product, g in df.groupby("Product"):
    ax[2].scatter(g["Age"], g["Amount"], s=60, label=product)
ax[2].set_xlabel("Age")
ax[2].set_ylabel("Amount")
ax[2].set_title("Age vs amount")
ax[2].legend()
plt.tight_layout()
plt.savefig("sa_m2_q2.png", dpi=110)
print("\nsaved sa_m2_q2.png")
