"""M2-Q5  Interactive visualisation: Plotly, Bokeh, Folium (Lab experiments 6-10).
Each chart is written to an HTML file; open the files in a browser to interact.
"""
import numpy as np
import pandas as pd
import plotly.express as px
from bokeh.models import ColumnDataSource, HoverTool
from bokeh.plotting import figure, output_file, save
from sklearn.datasets import load_iris
import folium

# ---- Lab 6: Plotly interactive bar chart ------------------------------------
cities = pd.DataFrame({"city": ["Mumbai", "Delhi", "Bengaluru", "Chennai", "Hyderabad"],
                       "population_m": [12.4, 11.0, 8.4, 7.1, 6.8]})        # illustrative values
fig_bar = px.bar(cities, x="city", y="population_m", title="Population of cities (millions)",
                 hover_data={"population_m": ":.1f"})
fig_bar.write_html("plotly_bar.html", include_plotlyjs="cdn")

# ---- Lab 7: Plotly scatter, house size vs price -----------------------------
rng = np.random.default_rng(1)
size = rng.integers(500, 3000, 40)
house = pd.DataFrame({"size_sqft": size, "price_lakh": size * 0.03 + rng.normal(0, 8, 40)})
fig_sc = px.scatter(house, x="size_sqft", y="price_lakh", trendline="ols",   # 'ols' needs statsmodels
                    title="House size vs price")
fig_sc.write_html("plotly_scatter.html", include_plotlyjs="cdn")

# ---- Lab 8: Bokeh line plot, daily temperature ------------------------------
days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
temps = [31, 33, 32, 35, 34, 30, 29]
src = ColumnDataSource(dict(day=days, temp=temps))
p1 = figure(x_range=days, title="Daily temperature", height=300, width=500,
            tools="pan,wheel_zoom,reset,save")
p1.line("day", "temp", source=src, line_width=2)
p1.scatter("day", "temp", source=src, size=8)
p1.add_tools(HoverTool(tooltips=[("day", "@day"), ("temp", "@temp °C")]))
output_file("bokeh_line.html")
save(p1)

# ---- Lab 9: Bokeh bar chart, product sales ----------------------------------
products = ["Laptop", "Phone", "Tablet", "Watch"]
sales = [120, 300, 90, 150]
p2 = figure(x_range=products, title="Sales by product", height=300, width=500)
p2.vbar(x=products, top=sales, width=0.6)
output_file("bokeh_bar.html")
save(p2)

# ---- Lab 10: Bokeh scatter, Iris petal length vs width ----------------------
iris = load_iris(as_frame=True).frame
p3 = figure(title="Iris: petal length vs width", height=300, width=500)
p3.scatter(iris["petal length (cm)"], iris["petal width (cm)"], size=6, alpha=0.6)
output_file("bokeh_scatter.html")
save(p3)

# ---- Folium: map with a marker ----------------------------------------------
m = folium.Map(location=[12.9692, 79.1559], zoom_start=12)                # Vellore
folium.Marker([12.9692, 79.1559], popup="VIT Vellore").add_to(m)
m.save("folium_map.html")

for name in ["plotly_bar", "plotly_scatter", "bokeh_line", "bokeh_bar", "bokeh_scatter", "folium_map"]:
    with open(f"{name}.html", encoding="utf-8") as f:
        text = f.read()
    print(f"{name + '.html':<20} written, {len(text):>9,} characters")
print("\nPlotly bar trace type  :", fig_bar.data[0].type, "with", len(fig_bar.data[0].x), "bars")
print("Plotly scatter traces  :", [t.mode for t in fig_sc.data])
print("Iris points plotted    :", len(iris))
