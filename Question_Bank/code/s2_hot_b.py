"""Sample HOT questions, Module 2 - questions 3, 4 and 5 (web mining and merge, house-price ML, smart-city dashboard)."""
import re

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
from scipy import stats
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import LeaveOneOut, cross_val_predict
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.tree import DecisionTreeRegressor

pd.set_option("display.width", 110)

# =============================================================== Question 3
site1 = """<table id="books"><tr><th>BookID</th><th>Title</th><th>Price</th></tr>
<tr><td>B101</td><td>Python Basics</td><td>Rs. 450</td></tr>
<tr><td>B102</td><td>Data Science</td><td>Rs. 700</td></tr>
<tr><td>B103</td><td>AI Fundamentals</td><td>Rs. 850</td></tr></table>"""
site2 = """<ul class="ratings"><li data-id="B101"><span class="r">4.5</span></li><li data-id="B102"><span class="r">4.8</span></li>
<li data-id="B103"><span class="r">4.2</span></li><li data-id="B104"><span class="r">3.9</span></li></ul>"""
print("--- Q3 step 1: collect with Beautiful Soup (the same selectors go into a Scrapy spider's parse method) ---")
s1 = BeautifulSoup(site1, "html.parser")
rows = [[td.get_text(strip=True) for td in tr.find_all("td")] for tr in s1.select("#books tr")[1:]]
A = pd.DataFrame(rows, columns=["BookID", "Title", "Price"])
A["Price"] = A.Price.str.extract(r"(\d+)", expand=False).astype(int)               # 'Rs. 450' -> 450
s2 = BeautifulSoup(site2, "html.parser")
B = pd.DataFrame([{"BookID": li["data-id"], "Rating": float(li.select_one("span.r").text)} for li in s2.select("ul.ratings li")])
print("Dataset A (website 1):\n", A.to_string(index=False), "\nDataset B (website 2):\n", B.to_string(index=False), sep="")

print("\n--- Q3 step 2: merge with pandas and inspect mismatches ---")
M = pd.merge(A, B, on="BookID", how="outer", indicator=True, validate="one_to_one")
print(M.to_string(index=False))
print("inner merge rows:", len(pd.merge(A, B, on="BookID")), "| rows present on only one site:", M[M._merge != "both"].BookID.tolist(), "(example of an inconsistency: B104 has a rating but no price)")

print("\n--- Q3 step 3: cleaning problems and fixes ---")
dirty = pd.Series(["Rs. 450", "₹ 1,200", "450.00", None, "N/A"])
naive = pd.to_numeric(dirty.str.replace(r"[^\d.]", "", regex=True), errors="coerce")
print("naive clean (delete everything except digits and dots):", naive.tolist(), "<- 'Rs. 450' became 0.45 because the dot of 'Rs.' survived: a silent error")
safe = pd.to_numeric(dirty.str.extract(r"(\d[\d,]*(?:\.\d+)?)", expand=False).str.replace(",", "", regex=False), errors="coerce")
print("safer clean (extract the number, then drop commas)     :", safe.tolist(), "(failures become NaN: then decide to drop or impute)")
print("duplicate keys check:", A.BookID.is_unique, B.BookID.is_unique, "| key as text vs number mismatch raises ValueError (see section 2.6)")

print("\n--- Q3 step 4: which books are most valuable (rating and price together) ---")
V = pd.merge(A, B, on="BookID").copy()
V["rating_per_100_rs"] = (V.Rating / V.Price * 100).round(3)
r_n = (V.Rating - V.Rating.min()) / (V.Rating.max() - V.Rating.min())
p_n = (V.Price.max() - V.Price) / (V.Price.max() - V.Price.min())
V["score"] = (0.5 * r_n + 0.5 * p_n).round(3)
print(V.sort_values("score", ascending=False).to_string(index=False))
print("highest rating:", V.loc[V.Rating.idxmax(), "Title"], "| best rating per rupee:", V.loc[V.rating_per_100_rs.idxmax(), "Title"], "| best 50/50 score:", V.loc[V.score.idxmax(), "Title"])
print("weights are a business choice: change 0.5/0.5 to 0.8/0.2 and re-rank:", V.assign(s=0.8 * r_n + 0.2 * p_n).sort_values("s", ascending=False).Title.tolist())

# =============================================================== Question 4
h = pd.DataFrame({"HouseSize": [1200, 1500, 1800, 2200, 2500], "Bedrooms": [2, 3, 3, 4, 4], "Age": [10, 8, 5, 3, 2], "Price": [45, 60, 75, 95, 110]})
X, y = h[["HouseSize", "Bedrooms", "Age"]], h.Price
print("\n\n--- Q4 step 1: variables and relationships (NumPy, SciPy, pandas) ---")
print("independent (features):", list(X.columns), "| dependent (target):", y.name)
print("correlation matrix:\n", h.corr().round(3), sep="")
r, p = stats.pearsonr(h.HouseSize, h.Price)
lr = stats.linregress(h.HouseSize, h.Price)
print(f"SciPy pearsonr(size, price): r={r:.4f}, p={p:.4f} | linregress: price = {lr.intercept:.2f} + {lr.slope:.4f} x size, R^2={lr.rvalue ** 2:.4f}")
print("NumPy: np.corrcoef(size, age)[0,1] =", round(np.corrcoef(h.HouseSize, h.Age)[0, 1], 4), "-> features are almost collinear (multicollinearity)")
print("missing values:", int(h.isna().sum().sum()), "| duplicate rows:", int(h.duplicated().sum()), "| only", len(h), "rows for", X.shape[1], "features -> high overfitting risk")

print("\n--- Q4 step 2: compare candidate algorithms with leave-one-out validation ---")
models = {"Linear regression (size only)": (LinearRegression(), ["HouseSize"]),
          "Linear regression (all 3)": (LinearRegression(), ["HouseSize", "Bedrooms", "Age"]),
          "Ridge, scaled (all 3)": (make_pipeline(StandardScaler(), Ridge(alpha=1.0)), ["HouseSize", "Bedrooms", "Age"]),
          "Decision tree (all 3)": (DecisionTreeRegressor(random_state=0), ["HouseSize", "Bedrooms", "Age"]),
          "Random forest (all 3)": (RandomForestRegressor(n_estimators=100, random_state=0), ["HouseSize", "Bedrooms", "Age"])}
print(f"{'model':<32}{'MAE':>6}{'RMSE':>7}{'R2':>8}")
for name, (m, cols) in models.items():
    pred = cross_val_predict(m, h[cols], y, cv=LeaveOneOut())
    print(f"{name:<32}{mean_absolute_error(y, pred):>6.2f}{mean_squared_error(y, pred) ** 0.5:>7.2f}{r2_score(y, pred):>8.3f}")

print("\n--- Q4 step 3: extrapolation, the weakness of tree models ---")
new = pd.DataFrame({"HouseSize": [3000], "Bedrooms": [5], "Age": [1]})
lin = LinearRegression().fit(X[["HouseSize"]], y)
tree = DecisionTreeRegressor(random_state=0).fit(X, y)
rf = RandomForestRegressor(n_estimators=100, random_state=0).fit(X, y)
print(f"3000 sq ft: linear (size only) predicts {lin.predict(new[['HouseSize']])[0]:.1f} lakhs | decision tree {tree.predict(new)[0]:.1f} | random forest {rf.predict(new)[0]:.1f} | largest training price {y.max()}")
print(f"linear model: price = {lin.intercept_:.2f} + {lin.coef_[0]:.4f} x size  -> every extra 100 sq ft adds about {100 * lin.coef_[0]:.1f} lakhs")
all3 = LinearRegression().fit(X, y)
print("all-3 linear coefficients:", dict(zip(X.columns, all3.coef_.round(4))), "(size alone explains price exactly here, so the others get 0)")
vif = {}
for col in X.columns:
    others = X.drop(columns=col)
    r2 = LinearRegression().fit(others, X[col]).score(others, X[col])
    vif[col] = round(1 / (1 - r2), 1) if r2 < 0.99999 else float("inf")
print("variance inflation factors (VIF > 10 signals multicollinearity):", vif)

# =============================================================== Question 5
z = pd.DataFrame({"Zone": ["North", "South", "East", "West", "Central"], "Temp": [35, 30, 33, 29, 37], "AQI": [180, 120, 150, 100, 220],
                  "Rain": [20, 35, 25, 40, 15], "Green": [18, 30, 22, 35, 12]}).set_index("Zone")
print("\n\n--- Q5 step 1: what needs immediate attention ---")
bands = [0, 50, 100, 200, 300, 400, 500]
labels = ["Good", "Satisfactory", "Moderately polluted", "Poor", "Very Poor", "Severe"]
z["AQI_category"] = pd.cut(z.AQI, bands, labels=labels)
print(z[["AQI", "AQI_category"]].to_string())
print("(CPCB India bands: Good 0-50, Satisfactory 51-100, Moderately polluted 101-200, Poor 201-300, Very Poor 301-400, Severe 401-500)")
num = z[["Temp", "AQI", "Rain", "Green"]]
bad = (num - num.min()) / (num.max() - num.min())
bad["Rain"], bad["Green"] = 1 - bad["Rain"], 1 - bad["Green"]               # low rainfall and low green cover are the bad direction
z["risk_score"] = bad.mean(axis=1).round(3)
print("composite risk (mean of min-max scaled stress factors; 1 = worst):\n", z.risk_score.sort_values(ascending=False).to_string(), sep="")
print("correlations with AQI:", num.corr()["AQI"].drop("AQI").round(3).to_dict())

print("\n--- Q5 step 2: a first model and zone grouping (ML applications) ---")
g = stats.linregress(z.Green, z.AQI)
print(f"AQI = {g.intercept:.1f} + ({g.slope:.2f}) x green cover%, R^2 = {g.rvalue ** 2:.3f} -> each extra 1% of green cover goes with about {abs(g.slope):.1f} lower AQI points (association in 5 zones, not proof of cause)")
from sklearn.cluster import KMeans
km = KMeans(2, n_init=10, random_state=0).fit(StandardScaler().fit_transform(num))
print("K-means (k=2) on standardised factors groups the zones as:", {int(k): z.index[km.labels_ == k].tolist() for k in sorted(set(km.labels_))})

fig, ax = plt.subplots(1, 3, figsize=(11, 3.3))
cmap = {"Moderately polluted": "#f0ad4e", "Satisfactory": "#5cb85c", "Poor": "#d9534f"}
ax[0].bar(z.index, z.AQI, color=[cmap[str(c)] for c in z.AQI_category]); ax[0].set_title("AQI by zone (colour = CPCB category)"); ax[0].tick_params(axis="x", labelsize=8)
ax[1].scatter(z.Green, z.AQI, s=60, color="#2f6db5"); xs = np.linspace(10, 37, 10); ax[1].plot(xs, g.intercept + g.slope * xs, "--", color="grey")
for zone, r_ in z.iterrows():
    ax[1].annotate(zone, (r_.Green, r_.AQI), textcoords="offset points", xytext=(4, 4), fontsize=8)
ax[1].set_xlabel("Green cover (%)"); ax[1].set_ylabel("AQI"); ax[1].set_title("Green cover vs AQI")
cm = num.corr(); ax[2].imshow(cm, cmap="RdBu_r", vmin=-1, vmax=1); ax[2].set_xticks(range(4)); ax[2].set_yticks(range(4)); ax[2].set_xticklabels(cm.columns, fontsize=8); ax[2].set_yticklabels(cm.columns, fontsize=8)
for i in range(4):
    for j in range(4):
        ax[2].text(j, i, f"{cm.iloc[i, j]:.2f}", ha="center", va="center", fontsize=7)
ax[2].set_title("Correlation heatmap")
fig.tight_layout(); fig.savefig("hot_m2_q5.png", dpi=140)

print("\n--- Q5 step 3: interactive and geographic outputs (files written) ---")
import plotly.express as px
fp = px.scatter(z.reset_index(), x="Green", y="AQI", size="Temp", color="AQI_category", hover_name="Zone", title="Zones: green cover vs AQI")
fp.write_html("hot_m2_q5_plotly.html", include_plotlyjs="cdn")
from bokeh.models import ColumnDataSource, HoverTool
from bokeh.plotting import figure, output_file, save
src = ColumnDataSource(z.reset_index())
pb = figure(x_range=list(z.index), height=300, width=450, title="AQI by zone")
pb.vbar(x="Zone", top="AQI", width=0.6, source=src); pb.add_tools(HoverTool(tooltips=[("zone", "@Zone"), ("AQI", "@AQI"), ("green %", "@Green")]))
output_file("hot_m2_q5_bokeh.html"); save(pb)
import folium
coords = {"North": (13.20, 80.25), "South": (12.90, 80.22), "East": (13.05, 80.30), "West": (13.05, 80.12), "Central": (13.05, 80.21)}      # illustrative
mp = folium.Map(location=[13.05, 80.21], zoom_start=11)
for zone, (la, lo) in coords.items():
    folium.CircleMarker([la, lo], radius=8 + z.loc[zone, "AQI"] / 20, color="#d9534f" if z.loc[zone, "AQI"] > 200 else "#2f6db5", fill=True, popup=f"{zone}: AQI {z.loc[zone, 'AQI']}").add_to(mp)
mp.save("hot_m2_q5_map.html")
print("written: hot_m2_q5_plotly.html, hot_m2_q5_bokeh.html, hot_m2_q5_map.html (the zone coordinates are made up for the demo; real ones come from the municipality)")
print("saved hot_m2_q5.png")
