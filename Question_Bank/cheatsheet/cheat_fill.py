r"""Format-3 items: a numbered program with some whole lines blanked out.
Blank lines are marked in the source below with a trailing   #@@ justification   (Python)   or   //@@ justification   (Scala).
parse() returns the full program (markers removed), the numbered lines and the blanks (line no, missing code, justification).
verify_fill.py runs every complete program and stores the real output in fill_results.json.
"""
import re

MARK = re.compile(r"^(.*?)\s+(?:#|//)@@\s*(.*)$")

FILLS = []


def fill(fid, title, lang, labs, code, deps=(), task=""):
    FILLS.append(dict(id=fid, title=title, lang=lang, labs=labs, code=code.strip("\n"), deps=list(deps), task=task))


def parse(code):
    lines, blanks = [], []
    for no, raw in enumerate(code.split("\n"), 1):
        m = MARK.match(raw)
        if m:
            lines.append(m.group(1).rstrip())
            blanks.append((no, m.group(1).strip(), m.group(2).strip()))
        else:
            lines.append(raw.rstrip())
    return lines, blanks


# ------------------------------------------------------------------------------------------------ Python
fill("F1", "Employee table: create, filter, group, sort (pandas basics)", "python", "Programs 1, 2",
     task="Build a DataFrame of employees, add a bonus column, filter the IT department, find the average salary per department and list the top three earners.",
     code=r'''
import pandas as pd

data = {"Name": ["Asha", "Ravi", "Meena", "John", "Sara", "Kabir"],
        "Dept": ["HR", "IT", "IT", "HR", "Sales", "IT"],
        "Age": [28, 35, 41, 30, 26, 38],
        "Salary": [52000, 61000, 75000, 48000, 43000, 68000]}
df = pd.DataFrame(data)  #@@ pd.DataFrame turns the dict into a table: each key becomes a column, each list the column values.
print(df.shape)
print(df["Salary"].describe().round(1))

df["Bonus"] = df["Salary"] * 0.10  #@@ Assigning to a new column label creates it. The multiplication is vectorised, so no loop is needed.
it = df[df["Dept"] == "IT"]  #@@ A boolean mask inside [ ] keeps the rows where the condition is True. == compares, a single = would be a syntax error.
print(len(it), "IT employees")
avg = df.groupby("Dept")["Salary"].mean()  #@@ groupby splits by department, selecting ["Salary"] limits the work to one column, mean() aggregates each group.
print(avg.round(0))
top = df.sort_values("Salary", ascending=False).head(3)  #@@ sort_values orders by Salary, ascending=False (a boolean, not a string) puts the highest first, head(3) keeps three rows.
print(top[["Name", "Salary"]])
''')

fill("F2", "Cleaning a dirty table: duplicates, NaN, text, dates, outliers", "python", "Programs 3, 4",
     task="Remove duplicate rows, fill the missing age with the median, tidy the city text, convert the date column and drop the outlier with the IQR rule.",
     code=r'''
import pandas as pd
import numpy as np

df = pd.DataFrame({"id": [1, 2, 2, 3, 4, 5, 6],
                   "age": [25, 27, 27, np.nan, 220, 29, 26],
                   "city": ["Pune", "Delhi", "Delhi", None, "Goa", "pune ", "Delhi"],
                   "joined": ["2026-01-05", "2026-02-10", "2026-02-10", "2026-03-15",
                              "2026-04-20", "2026-05-25", "2026-06-30"]})
print(df.isnull().sum().to_dict())
df = df.drop_duplicates()  #@@ Rows 2 and 3 are identical, drop_duplicates keeps the first copy. The result must be assigned back because it returns a new frame.
df["age"] = df["age"].fillna(df["age"].median())  #@@ fillna replaces NaN. The median is preferred to the mean here because the outlier 220 would distort the mean.
df["city"] = df["city"].fillna("Unknown").str.strip().str.title()  #@@ Fill the missing value first, then .str.strip() removes the stray space and .str.title() fixes the case ('pune ' becomes 'Pune').
df["joined"] = pd.to_datetime(df["joined"])  #@@ The column holds strings. to_datetime converts it to datetime64 so that the .dt accessor works.
q1, q3 = df["age"].quantile([0.25, 0.75])
iqr = q3 - q1
clean = df[df["age"].between(q1 - 1.5 * iqr, q3 + 1.5 * iqr)]  #@@ IQR rule: keep values within 1.5 x IQR of the quartiles. between() builds the boolean mask, the outlier 220 is dropped.
print(clean[["id", "age", "city"]])
print(clean["joined"].dt.month.tolist())
''')

fill("F3", "Reshape, slice and broadcast an array (NumPy)", "python", "Programs 5, 6",
     task="Create the numbers 1 to 12, reshape them to 3 x 4, compute column statistics, centre the columns and multiply by a matrix.",
     code=r'''
import numpy as np

a = np.arange(1, 13)  #@@ arange(start, stop) excludes the stop value, so 1..12 needs stop = 13.
m = a.reshape(3, 4)  #@@ reshape needs 3 x 4 = 12 elements, the same count as a. It returns a view of the same data.
print(m.shape, m.ndim)
print(m[1, 2], m[:, 1], m[0:2, 1:3].tolist())
col_mean = m.mean(axis=0)  #@@ axis=0 runs down the rows, so the result has one mean per column (4 values).
row_sum = m.sum(axis=1)  #@@ axis=1 runs along each row, giving one total per row (3 values).
print(col_mean, row_sum)
centered = m - col_mean  #@@ Broadcasting: the (4,) vector is stretched across the 3 rows of the (3, 4) matrix, so every column is centred.
print(centered[0])
print(m[m % 2 == 0])
w = np.array([[1, 0], [0, 1], [1, 1], [0, 2]])
prod = m @ w  #@@ @ is the matrix product. The inner dimensions must match: (3, 4) @ (4, 2) gives (3, 2). * would be element-wise and fail.
print(prod)
''')

fill("F4", "Distribution, scatter and correlation heat-map (matplotlib and seaborn)", "python", "Programs 7, 8",
     task="Create study-hours and score data, print their correlation and draw three panels: histogram, scatter plot and correlation heat-map, then save the figure.",
     code=r'''
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

rng = np.random.default_rng(42)
df = pd.DataFrame({"hours": rng.uniform(1, 10, 60)})
df["score"] = 40 + 5 * df["hours"] + rng.normal(0, 4, 60)
print(df.corr().loc["hours", "score"].round(2))

fig, ax = plt.subplots(1, 3, figsize=(12, 3.5))  #@@ subplots(rows, cols) returns the figure and an array of axes, one per panel, so ax[0], ax[1], ax[2] exist.
ax[0].hist(df["score"], bins=8, color="steelblue", edgecolor="white")  #@@ hist bins the values into 8 intervals and draws the bar heights: the distribution of one numeric column.
ax[0].set_title("Score distribution")
sns.scatterplot(data=df, x="hours", y="score", ax=ax[1])  #@@ data=df lets seaborn look the column names up. ax=ax[1] draws into the second panel.
ax[1].set_title("Hours vs score")
sns.heatmap(df.corr(), annot=True, cmap="Blues", ax=ax[2])  #@@ heatmap colours the correlation matrix, annot=True writes the numbers in the cells.
plt.tight_layout()
plt.savefig("eda.png", dpi=100)  #@@ savefig writes the figure to a file. It must come before plt.show(), which clears the figure.
print("saved eda.png")
''')

fill("F5", "Scraping job cards with BeautifulSoup", "python", "Programs 9, 10",
     task="Parse the HTML, loop over every job card, extract title, location and link and put the result in a DataFrame.",
     code=r'''
from bs4 import BeautifulSoup
import pandas as pd

html = """<div class="job"><h2>Data Analyst</h2><span class="loc">Pune</span><a href="/j/1">Apply</a></div>
<div class="job"><h2>ML Engineer</h2><span class="loc">Delhi</span><a href="/j/2">Apply</a></div>
<div class="job"><h2>BI Developer</h2><span class="loc">Pune</span><a href="/j/3">Apply</a></div>"""
soup = BeautifulSoup(html, "html.parser")  #@@ Builds the parse tree from the HTML text. "html.parser" is the parser that ships with Python (no extra install).
rows = []
for card in soup.find_all("div", class_="job"):  #@@ find_all returns every matching tag. class_ (with underscore) because class is a reserved word in Python.
    title = card.find("h2").text.strip()  #@@ find returns the first match inside this card. .text gives the inner text and .strip() removes surrounding whitespace.
    loc = card.find("span", class_="loc").get_text()
    link = card.find("a")["href"]  #@@ An attribute is read like a dictionary key. Use .get("href") instead if the attribute may be missing.
    rows.append({"title": title, "location": loc, "link": link})
df = pd.DataFrame(rows)  #@@ A list of dictionaries becomes a table: one row per dict, the keys become the column names.
print(df)
print(df["location"].value_counts().to_dict())
''')

fill("F6", "Interactive bar chart and OLS trend line (Plotly Express)", "python", "Programs 11, 12",
     task="Compute revenue per fruit, draw a coloured bar chart with axis titles, save it as HTML, then fit an OLS trend line and print R-squared.",
     code=r'''
import pandas as pd
import plotly.express as px

df = pd.DataFrame({"fruit": ["Apple", "Banana", "Orange", "Mango", "Grape"],
                   "price": [120, 45, 80, 150, 95],
                   "qty": [250, 600, 320, 180, 210]})
df["revenue"] = df["price"] * df["qty"]
fig = px.bar(df, x="fruit", y="revenue", color="fruit", title="Revenue by fruit")  #@@ px.bar(data_frame, x, y): x and y are column names as strings, color maps a column to bar colours.
fig.update_layout(xaxis_title="Fruit", yaxis_title="Revenue (INR)", showlegend=False)  #@@ update_layout changes titles and legend after the figure exists. The property names are validated (a typo raises ValueError).
fig.write_html("revenue.html")  #@@ Saves a stand-alone interactive page. It needs no extra package, unlike write_image which needs kaleido.
sc = px.scatter(df, x="price", y="qty", trendline="ols", text="fruit")  #@@ trendline="ols" adds a least-squares line and requires statsmodels to be installed.
model = px.get_trendline_results(sc).iloc[0]["px_fit_results"]
print(round(model.rsquared, 3))  #@@ get_trendline_results returns the fitted statsmodels model, .rsquared is the share of variance in qty explained by price.
print(len(fig.data), len(sc.data))
''')

fill("F7", "Iris scatter with colours by species and hover (Bokeh)", "python", "Programs 13, 14, 15",
     task="Plot sepal length against petal length, colour the points by species with factor_cmap, add a hover tool and save the plot to an HTML file.",
     code=r'''
import pandas as pd
from bokeh.plotting import figure, output_file, save
from bokeh.models import ColumnDataSource, HoverTool
from bokeh.transform import factor_cmap
from sklearn.datasets import load_iris

iris = load_iris(as_frame=True)
df = iris.data
df["species"] = iris.target_names[iris.target]
src = ColumnDataSource(df)  #@@ A ColumnDataSource is Bokeh's data container. Plots and tools that use the same source stay linked (shared selection, hover).
colors = factor_cmap("species", palette=["#1f77b4", "#ff7f0e", "#2ca02c"], factors=list(iris.target_names))  #@@ factor_cmap maps each category in the 'species' column to one palette colour: three factors, three colours.
p = figure(width=500, height=400, title="Iris: sepal vs petal length")
p.scatter("sepal length (cm)", "petal length (cm)", source=src, color=colors, legend_field="species", size=7)  #@@ scatter draws the markers from source columns. legend_field builds one legend entry per species. (circle(size=...) is deprecated in Bokeh 3.4+.)
p.add_tools(HoverTool(tooltips=[("species", "@species"), ("petal", "@{petal length (cm)}")]))  #@@ @column reads a source value. Names that contain spaces or brackets need the @{...} form.
output_file("iris.html")  #@@ Chooses the HTML file that save() or show() writes. Without it, save() has no target file.
save(p)
print(len(p.renderers), p.title.text)
''')

fill("F8", "PCA on the iris data: scale, fit, variance ratio, loadings", "python", "Program 16",
     task="Standardise the four iris measurements, project them on two principal components, print the explained variance and the loadings.",
     code=r'''
import pandas as pd
from sklearn.datasets import load_iris
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import plotly.express as px

iris = load_iris(as_frame=True)
X = iris.data
Xs = StandardScaler().fit_transform(X)  #@@ PCA follows variance, so features must be on the same scale first. fit_transform learns the mean/std and applies them (returns an ndarray).
pca = PCA(n_components=2)  #@@ n_components must be at most min(n_samples, n_features) = 4. Two components allow a 2-D plot.
pcs = pca.fit_transform(Xs)  #@@ fit_transform learns the components and returns the projected data (150 x 2). Calling fit_transform on the scaled data, not on X.
ratio = pca.explained_variance_ratio_
print(ratio.round(4), ratio.sum().round(4))
df = pd.DataFrame(pcs, columns=["PC1", "PC2"])
df["species"] = iris.target_names[iris.target]
loadings = pd.DataFrame(pca.components_.T, index=X.columns, columns=["PC1", "PC2"])  #@@ components_ has one row per component, so transposing gives one row per original feature: the loadings.
print(loadings.round(2))
fig = px.scatter(df, x="PC1", y="PC2", color="species", title="Iris PCA")
print(fig.layout.title.text)
''')

fill("F9", "K-Means on the iris data: elbow, fit, silhouette", "python", "Program 17",
     task="Standardise the iris data, compute the inertia for k = 1 to 6 (elbow), fit k = 3 and report cluster sizes and the silhouette score.",
     code=r'''
import numpy as np
from sklearn.datasets import load_iris
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

X = load_iris(as_frame=True).data
Xs = StandardScaler().fit_transform(X)
inertia = []
for k in range(1, 7):
    inertia.append(KMeans(n_clusters=k, n_init=10, random_state=42).fit(Xs).inertia_)  #@@ inertia_ is the within-cluster sum of squares. Plotting it against k gives the elbow curve for choosing k.
print([round(i, 1) for i in inertia])
km = KMeans(n_clusters=3, n_init=10, random_state=42)  #@@ n_clusters=3 is the chosen k, random_state fixes the random start so that the result can be reproduced.
labels = km.fit_predict(Xs)  #@@ fit_predict fits the model and returns the cluster number (0, 1, 2) of every row.
print(sorted(np.bincount(labels).tolist()))
print(km.cluster_centers_.shape)  #@@ cluster_centers_ is a (k, n_features) array: one centroid per cluster.
sil = silhouette_score(Xs, labels)  #@@ Silhouette compares within-cluster and nearest-cluster distance, from -1 to 1. Higher means better separated clusters.
print(round(sil, 3))
''')

# ------------------------------------------------------------------------------------------------ Scala
fill("F10", "Arrays, lists, sets and maps", "scala", "Programs 18, 19, 20",
     task="Sum an array, square a list, intersect two character sets, merge two grade maps keeping the higher grade and overwrite a key of a mutable HashMap.",
     code=r'''
import scala.collection.mutable

object Experiment {
  def main(args: Array[String]): Unit = {
    val arr = Array(2, 5, 9, 14, 20)
    println(arr.sum)  //@@ sum is defined on every numeric collection. arr.sum returns 50 without a loop.
    val primes = List(2, 3, 5, 7, 11)
    val squares = primes.map(x => x * x)  //@@ map applies the function to each element and returns a NEW list: List(4, 9, 25, 49, 121).
    println(squares)
    val s1 = "hello world".toSet
    val s2 = "world wide web".toSet
    println((s1 & s2).toList.sorted.mkString)  //@@ & is intersection (also written intersect). A Set has no order, so sort before printing.
    val m1 = Map("Rohan" -> 92, "Vedant" -> 88)
    val m2 = Map("Rohan" -> 85, "Kalyan" -> 90)
    val merged = (m1.keySet ++ m2.keySet).map { k => k -> Math.max(m1.getOrElse(k, 0), m2.getOrElse(k, 0)) }.toMap  //@@ Union of the keys, then getOrElse(k, 0) avoids an exception for a missing key. The key -> value pairs are turned back into a Map with toMap.
    println(merged.toSeq.sortBy(_._1))
    val grades = mutable.HashMap("Alice" -> 85)
    grades.put("Alice", 95)  //@@ A duplicate key overwrites the old value (put returns the old one as an Option). This is the hash-collision rule for equal keys.
    println(grades)
  }
}
''')

fill("F11", "Functional combinators and a case class", "scala", "Programs 21, 22",
     task="Filter, map and fold a list of integers, then filter, group and rank a list of Person objects.",
     code=r'''
case class Person(name: String, age: Int, city: String)

object Experiment {
  def main(args: Array[String]): Unit = {
    val nums = (1 to 10).toList
    val evens = nums.filter(_ % 2 == 0)  //@@ filter keeps the elements for which the predicate is true. Underscore stands for the element.
    val tripled = nums.map(_ * 3)  //@@ map transforms every element and keeps the list length.
    val product = nums.foldLeft(1)(_ * _)  //@@ foldLeft(start)(op) combines left to right. The start value is 1 because it is the identity of multiplication (0 would give 0).
    println(s"$evens $tripled $product")
    val people = List(Person("Vedant", 24, "Mumbai"), Person("Ayush", 32, "Delhi"),
      Person("Priya", 35, "Mumbai"), Person("Sneha", 22, "Hyderabad"))
    val older = people.filter(_.age > 30)  //@@ Case-class fields are public vals, so _.age works. The result is a List[Person].
    val byCity = people.groupBy(_.city)  //@@ groupBy returns a Map from the key (city) to the list of people with that key.
    byCity.toSeq.sortBy(_._1).foreach { case (c, g) => println(s"$c: ${g.map(_.name).mkString(", ")}") }
    val ranked = people.sortBy(-_.age)
    ranked.zipWithIndex.foreach { case (p, i) => println(s"${i + 1}. ${p.name} (${p.age})") }
    println(older.map(_.name))
  }
}
''')

fill("F12", "Vectors, statistics and formatted output (Breeze)", "scala", "Program 24",
     deps=["org.scalanlp::breeze:2.1.0"],
     task="Compute the revenue of each fruit as price x quantity, then its total and mean, print a formatted line per fruit and the inner product.",
     code=r'''
import breeze.linalg._
import breeze.stats._

object Experiment {
  def main(args: Array[String]): Unit = {
    val fruits = Array("Apple", "Banana", "Orange")
    val prices = DenseVector(120.0, 45.0, 80.0)
    val qty = DenseVector(250.0, 600.0, 320.0)
    val revenue = prices *:* qty  //@@ *:* multiplies element by element (price i x quantity i). The result is again a DenseVector of length 3.
    val total = sum(revenue)  //@@ sum from breeze.linalg adds all the elements and returns a Double.
    val avg = mean(revenue)  //@@ mean comes from breeze.stats, hence the second import.
    for (i <- fruits.indices) println(f"${fruits(i)}%-7s ${revenue(i)}%,10.2f")  //@@ The f interpolator formats: %-7s left-aligns the text in 7 characters, %,10.2f adds thousands separators with 2 decimals.
    println(f"Total: $total%,.2f  Mean: $avg%.2f")
    println(prices dot qty)  //@@ dot is the inner product (sum of products), a single number, not a vector.
  }
}
''')

fill("F13", "Series and Frame (Saddle)", "scala", "Program 23",
     deps=["io.github.pityka::saddle-core:4.0.0-M14"],
     task="Build a price Series indexed by date, print the mean, filter the expensive days, then build a two-column Frame and compute revenue.",
     code=r'''
import org.saddle._
import org.saddle.ops.BinOps._

object Experiment {
  def main(args: Array[String]): Unit = {
    val prices = Vec(120.50, 125.00, 118.75, 130.25, 128.00)
    val dates = Index("2026-05-01", "2026-05-08", "2026-05-15", "2026-05-22", "2026-05-29")
    val s = Series(prices, dates)  //@@ Series(values, index): the data Vec first, the label Index second.
    println(f"Average: ${s.values.mean}%.2f")  //@@ A Series has no mean method. Take the Vec of values (.values) and call mean there.
    val high = s.filter(_ > 125.0)  //@@ filter keeps the entries whose VALUE satisfies the predicate, together with their index labels.
    println(high.index.toVec)
    val qty = Vec(45.0, 50.0, 42.0, 55.0, 48.0)
    val frame = Frame("Price" -> prices, "Qty" -> qty)  //@@ Frame(name -> Vec, ...) builds a table of named columns, all of the same length.
    println(frame.numRows + " x " + frame.numCols)
    val revenue = frame.firstCol("Price").toVec * frame.firstCol("Qty").toVec  //@@ firstCol picks a column by name, toVec exposes it as a Vec, and * multiplies element by element.
    println(revenue.sum)
  }
}
''')
