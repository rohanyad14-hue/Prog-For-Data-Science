"""Sample answer M2-Q5: priority zones and dashboard building blocks for the smart-city table."""
import os
import tempfile
from pathlib import Path

import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import folium
from bokeh.models import ColumnDataSource, HoverTool
from bokeh.plotting import figure, output_file, save

OUT = Path.cwd()                                   # the PNG goes here, the HTML dashboards into a temporary folder
os.chdir(tempfile.mkdtemp(prefix="sa_city_"))

df = pd.DataFrame({"Zone": ["North", "South", "East", "West", "Central"], "Temperature": [35, 30, 33, 29, 37],
                   "AQI": [180, 120, 150, 100, 220], "Rainfall": [20, 35, 25, 40, 15], "GreenCover": [18, 30, 22, 35, 12]})

print("--- 1. which factors need immediate attention? ---")
df["AQI_category"] = pd.cut(df["AQI"], bins=[0, 50, 100, 200, 300, 400, 500],
                            labels=["Good", "Satisfactory", "Moderate", "Poor", "Very Poor", "Severe"])
print(df[["Zone", "AQI", "AQI_category"]])
num = ["Temperature", "AQI", "Rainfall", "GreenCover"]
print(df[num].corr().round(2))
z = (df[num] - df[num].mean()) / df[num].std(ddof=0)
df["priority_score"] = (z["AQI"] + z["Temperature"] - z["GreenCover"] - z["Rainfall"]).round(2)    # high AQI/heat, low green/rain
print(df.sort_values("priority_score", ascending=False)[["Zone", "priority_score"]].to_string(index=False))

print("\n--- 2. static charts (Matplotlib + Seaborn) ---")
fig, ax = plt.subplots(1, 2, figsize=(10, 3.6))
colors = df["AQI"].map(lambda v: "#c0392b" if v > 200 else "#e69f00" if v > 100 else "#2e8b57")
ax[0].bar(df["Zone"], df["AQI"], color=colors)
ax[0].axhline(200, color="grey", linestyle="--")
ax[0].text(4.45, 203, "Poor above 200", ha="right", fontsize=8)
ax[0].set_ylabel("AQI")
ax[0].set_title("AQI by zone")
sns.heatmap(df[num].corr(), annot=True, fmt=".2f", cmap="coolwarm", vmin=-1, vmax=1, ax=ax[1])
ax[1].set_title("Correlation of the four factors")
plt.tight_layout()
plt.savefig(OUT / "sa_m2_q5.png", dpi=110)
print("saved sa_m2_q5.png")

print("\n--- 3. interactive pieces (Plotly, Bokeh) and a map (Folium) ---")
fig2 = px.scatter(df, x="GreenCover", y="AQI", size="Temperature", color="Zone", hover_data=["Rainfall"], title="AQI against green cover")
fig2.write_html("dashboard_plotly.html", include_plotlyjs="cdn")
src = ColumnDataSource(df)
p = figure(title="AQI against rainfall", x_axis_label="Rainfall (mm)", y_axis_label="AQI", width=420, height=300, tools="pan,wheel_zoom,reset")
p.scatter("Rainfall", "AQI", source=src, size=14)
p.add_tools(HoverTool(tooltips=[("Zone", "@Zone"), ("AQI", "@AQI"), ("Green cover", "@GreenCover%")]))
output_file("dashboard_bokeh.html")
save(p)
coords = {"North": (13.12, 80.25), "South": (12.93, 80.24), "East": (13.03, 80.31), "West": (13.04, 80.17), "Central": (13.04, 80.24)}   # illustrative
m = folium.Map(location=[13.03, 80.24], zoom_start=11)
for _, r in df.iterrows():
    colour = "red" if r["AQI"] > 200 else "orange" if r["AQI"] > 100 else "green"
    folium.CircleMarker(coords[r["Zone"]], radius=r["AQI"] / 12, color=colour, fill=True,
                        tooltip=f"{r['Zone']}: AQI {r['AQI']} ({r['AQI_category']})").add_to(m)
m.save("dashboard_map.html")
print("written:", sorted(f for f in os.listdir(".") if f.endswith(".html")))
