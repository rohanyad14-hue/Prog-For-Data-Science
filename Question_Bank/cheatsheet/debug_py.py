"""Format-2 (debug the program) items for the Python labs.
Each bug: setup key, buggy code, fixed code, why (the description column), kind, contains.
kind     "error"  the buggy code raises an exception whose text contains `contains`
         "warn"   no exception but a warning whose text contains `contains`
         "silent" no exception; stdout contains `contains` (a wrong answer without any error)
nofix    True when the fixed code cannot be verified here (needs network / extra install)
fixed_pre  code run before the fixed snippet (e.g. create the file that read_csv needs)
fixed_contains  text that must appear in the fixed snippet's stdout
verify_py_debug.py runs every item and stores the real messages in debug_py_results.json.
"""

SETUPS = {
    "none": "",
    "pd": r'''
import pandas as pd, numpy as np
df = pd.DataFrame({'Name': ['Asha', 'Ravi', 'Meena', 'John'], 'Age': [28, 35, 41, 30],
                   'City': ['Pune', 'Delhi', 'Pune', 'Delhi'], 'Salary': [52000, 61000, 75000, 48000]})
''',
    "np": "import numpy as np\n",
    "plt": r'''
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd, numpy as np
df = pd.DataFrame({'City': ['Pune', 'Delhi', 'Goa'], 'Age': [28, 35, 41], 'Salary': [52000, 61000, 75000]})
''',
    "bs": r'''
from bs4 import BeautifulSoup
import requests
html = """<div class="quote"><span class="text">Be yourself.</span><small class="author">Oscar Wilde</small><a>no link</a></div>
<div class="quote"><span class="text">Stay hungry.</span><small class="author">Steve Jobs</small></div>"""
soup = BeautifulSoup(html, 'html.parser')
''',
    "px": r'''
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
df = pd.DataFrame({'City': ['Pune', 'Delhi', 'Goa'], 'Sales': [120, 90, 150]})
''',
    "bk": r'''
from bokeh.plotting import figure, output_file, show
from bokeh.models import ColumnDataSource
''',
    "sk": r'''
import numpy as np, pandas as pd
from sklearn.datasets import load_iris
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
iris = load_iris(as_frame=True)
X = iris.data
df_iris = iris.data.copy()
df_iris['species'] = iris.target_names[iris.target]
''',
}

PY_BUGS = []


def bug(topic, setup, buggy, fixed, why, kind="error", contains="", nofix=False, fixed_pre="", fixed_contains=""):
    PY_BUGS.append(dict(topic=topic, setup=setup, buggy=buggy.strip("\n"), fixed=fixed.strip("\n"), why=why, kind=kind,
                        contains=contains, nofix=nofix, fixed_pre=fixed_pre, fixed_contains=fixed_contains))


# ---------------------------------------------------------------- pandas
bug("pandas", "pd", "print(df.head)", "print(df.head())",
    "A method was named but not called, so pandas prints the method object instead of the first rows. Add ( ).",
    kind="silent", contains="bound method", fixed_contains="Asha")
bug("pandas", "pd", "adults = df[df['Age'] > 30 and df['Salary'] > 50000]", "adults = df[(df['Age'] > 30) & (df['Salary'] > 50000)]\nprint(adults)",
    "Python's `and` needs a single True/False, a Series has many. Use the element-wise & and wrap each condition in ( ).",
    contains="truth value of a Series is ambiguous", fixed_contains="Ravi")
bug("pandas", "pd", "adults = df[df['Age'] > 30 & df['Salary'] > 50000]", "adults = df[(df['Age'] > 30) & (df['Salary'] > 50000)]\nprint(adults)",
    "& binds tighter than >, so Python reads df['Age'] > (30 & df['Salary']) > 50000. That is a chained comparison, which needs a single True/False, so the error is the same as with `and`. Bracket every condition.",
    contains="", fixed_contains="Ravi")
bug("pandas", "pd", "print(df.sort_values('Age', ascending='False'))", "print(df.sort_values('Age', ascending=False))",
    "ascending takes the boolean False, not the string 'False' (a non-empty string would be truthy).",
    contains="ascending", fixed_contains="Meena")
bug("pandas", "pd", "df = df.drop('Age')\nprint(df.columns)", "df = df.drop(columns='Age')\nprint(df.columns.tolist())",
    "drop looks for the label in the rows (axis=0) by default. To remove a column use columns='Age' or axis=1.",
    contains="not found in axis", fixed_contains="Salary")
bug("pandas", "pd", "d = df.copy()\nd.loc[1, 'Age'] = None\nd.dropna()\nprint(len(d))", "d = df.copy()\nd.loc[1, 'Age'] = None\nd = d.dropna()\nprint(len(d))",
    "dropna() returns a new DataFrame and leaves d untouched. Assign the result back (or use inplace=True). No error is shown.",
    kind="silent", contains="4", fixed_contains="3")
bug("pandas", "pd", "print(df['name'])", "print(df['Name'])",
    "Column labels are case sensitive: the column is 'Name', not 'name'. Check df.columns first.",
    contains="'name'", fixed_contains="Asha")
bug("pandas", "pd", "print(df.iloc[:, 'Age'])", "print(df.loc[:, 'Age'])",
    "iloc is position based and accepts integers only. Use loc (or df['Age']) for a label, or iloc[:, 1] for a position.",
    contains="Location based indexing", fixed_contains="35")
bug("pandas", "pd", "print(df.groupby('City').mean())", "print(df.groupby('City')[['Age', 'Salary']].mean())",
    "mean() cannot average the text column Name. Select the numeric columns first (or pass numeric_only=True).",
    contains="agg function failed", fixed_contains="Delhi")
bug("pandas", "pd", "a = pd.DataFrame({'id': ['1', '2', '3'], 'x': [10, 20, 30]})\nb = pd.DataFrame({'id': [1, 2, 3], 'y': [5, 6, 7]})\nprint(pd.merge(a, b, on='id'))",
    "a = pd.DataFrame({'id': ['1', '2', '3'], 'x': [10, 20, 30]})\nb = pd.DataFrame({'id': [1, 2, 3], 'y': [5, 6, 7]})\na['id'] = a['id'].astype(int)\nprint(pd.merge(a, b, on='id'))",
    "The join key is text in one frame and int in the other. Make the dtypes equal before merging.",
    contains="merge on object and int64", fixed_contains="30")
bug("pandas", "pd", "d = df.copy()\nd.loc[1, 'Age'] = None\nd['Age'] = d['Age'].fillna(d['Age'].mean)\nprint(d['Age'].dtype)", "d = df.copy()\nd.loc[1, 'Age'] = None\nd['Age'] = d['Age'].fillna(d['Age'].mean())\nprint(d['Age'].dtype, d['Age'].tolist())",
    "mean without ( ) is the method object, and fillna happily stores it in the gap, turning the column into dtype object. No error, so check dtypes after cleaning.",
    kind="silent", contains="object", fixed_contains="float64 [28.0, 33.0")
bug("pandas", "pd", "df = pd.read_csv('sales_data.csv')", "df = pd.read_csv('sales_data.csv')\nprint(df.shape)",
    "The file is not in the working directory. Put it next to the script, give the full path (raw string r'C:\\...') or check os.getcwd().",
    contains="No such file", fixed_pre="open('sales_data.csv', 'w').write('a,b\\n1,2\\n3,4\\n')", fixed_contains="(2, 2)")
bug("pandas", "pd", "df['Date'] = ['2026-01-05', '2026-02-10', '2026-03-15', '2026-04-20']\nprint(df['Date'].dt.year)",
    "df['Date'] = pd.to_datetime(['2026-01-05', '2026-02-10', '2026-03-15', '2026-04-20'])\nprint(df['Date'].dt.year.tolist())",
    "The column holds strings. The .dt accessor only works on datetime64, so convert with pd.to_datetime first.",
    contains=".dt accessor", fixed_contains="2026")
bug("pandas", "pd", "print(pd.Series(['1,200', '850']).astype(float))", "print(pd.Series(['1,200', '850']).str.replace(',', '').astype(float).tolist())",
    "float() cannot read the thousands separator. Strip it with str.replace before astype.",
    contains="could not convert string to float", fixed_contains="1200.0")
bug("pandas", "pd", "d = df.copy()\nd[d['Age'] > 30]['Salary'] = 0\nprint(d['Salary'].tolist())", "d = df.copy()\nd.loc[d['Age'] > 30, 'Salary'] = 0\nprint(d['Salary'].tolist())",
    "Chained indexing assigns into a temporary copy, so d is unchanged. Use a single .loc[row_mask, 'col'] = value.",
    kind="silent", contains="52000", fixed_contains="[52000, 0, 0, 48000]")
bug("pandas", "pd", "both = pd.concat(df, df)", "both = pd.concat([df, df], ignore_index=True)\nprint(len(both))",
    "concat takes ONE positional argument: a list of frames. ignore_index=True renumbers the rows 0..n-1.",
    contains="positional argument", fixed_contains="8")
bug("pandas", "pd", "d = df.copy()\nd.loc[1, 'Age'] = None\nprint(d['Age'].astype(int))", "d = df.copy()\nd.loc[1, 'Age'] = None\nprint(d['Age'].fillna(d['Age'].median()).astype(int).tolist())",
    "NaN is a float and has no int equivalent. Fill (or drop) the missing values before casting, or use the nullable 'Int64'.",
    contains="Cannot convert non-finite values", fixed_contains="30")
bug("pandas", "pd", "print(df.corr())", "print(df.corr(numeric_only=True))",
    "corr() tries to convert every column to float and fails on the text columns. Restrict it to numeric ones.",
    contains="could not convert string to float", fixed_contains="Salary")
bug("pandas", "pd", "df = df.sort_values('Age', inplace=True)\nprint(df.head())", "df = df.sort_values('Age')\nprint(df.head().shape)",
    "With inplace=True the method returns None, so df became None. Use either inplace=True (no assignment) or the assignment (no inplace).",
    contains="'NoneType' object has no attribute 'head'", fixed_contains="(4, 4)")
bug("pandas", "pd", "print(df[df['City'] = 'Pune'])", "print(df[df['City'] == 'Pune'])",
    "= assigns, == compares. A filter needs ==.", contains="cannot assign to subscript", fixed_contains="Meena")
bug("pandas", "pd", "print(df.isnull.sum())", "print(df.isnull().sum().sum())",
    "isnull is a method: call it with ( ) before chaining .sum().", contains="has no attribute 'sum'", fixed_contains="0")
bug("pandas", "pd", "df.columns = ['A', 'B']", "df.columns = ['A', 'B', 'C', 'D']\nprint(df.columns.tolist())",
    "The list must have one name per column (4 here). Use df.rename(columns={...}) to rename only some.",
    contains="Length mismatch", fixed_contains="['A', 'B', 'C', 'D']")
bug("pandas", "pd", "df['Dept'] = ['HR', 'IT']", "df['Dept'] = ['HR', 'IT', 'HR', 'IT']\nprint(df['Dept'].tolist())",
    "A new column needs exactly one value per row (or a single scalar that is broadcast).",
    contains="does not match length of index", fixed_contains="HR")

# ---------------------------------------------------------------- numpy
bug("numpy", "np", "print(np.array([1, 2, 3]) + np.array([1, 2]))", "print(np.array([1, 2, 3]) + np.array([1, 2, 3]))",
    "Shapes (3,) and (2,) cannot be broadcast. Broadcasting needs equal lengths or a length of 1 in a trailing dimension.",
    contains="could not be broadcast", fixed_contains="[2 4 6]")
bug("numpy", "np", "A = np.ones((2, 3))\nB = np.ones((2, 3))\nprint(np.dot(A, B))", "A = np.ones((2, 3))\nB = np.ones((2, 3))\nprint(np.dot(A, B.T))",
    "Matrix product needs A.shape[1] == B.shape[0]. Transpose B so (2,3) x (3,2) works.",
    contains="not aligned", fixed_contains="3.")
bug("numpy", "np", "a = np.arange(8)\nprint(a.reshape(3, 3))", "a = np.arange(8)\nprint(a.reshape(2, 4))",
    "The new shape must hold exactly as many elements (8) as the array. -1 lets numpy work out one dimension: reshape(2, -1).",
    contains="cannot reshape array of size 8", fixed_contains="[0 1 2 3]")
bug("numpy", "np", "A = np.array([[1, 2], [3, 4]])\nB = np.array([[5, 6], [7, 8]])\nprint(A * B)", "A = np.array([[1, 2], [3, 4]])\nB = np.array([[5, 6], [7, 8]])\nprint(A @ B)",
    "* multiplies element by element. The matrix product is @ (or np.dot / np.matmul). No error is raised.",
    kind="silent", contains="[[ 5 12]", fixed_contains="[19 22]")
bug("numpy", "np", "A = np.arange(6).reshape(2, 3)\nprint(A.mean(axis=2))", "A = np.arange(6).reshape(2, 3)\nprint(A.mean(axis=1))",
    "A 2-D array has axes 0 (rows) and 1 (columns) only. axis=0 gives column means, axis=1 gives row means.",
    contains="out of bounds", fixed_contains="[1. 4.]")
bug("numpy", "np", "a = np.array([1, 2, 3])\nb = a\nb[0] = 99\nprint(a)", "a = np.array([1, 2, 3])\nb = a.copy()\nb[0] = 99\nprint(a)",
    "b = a only creates a second name for the same array, so editing b edits a. Slices are views too. Use .copy() for independent data.",
    kind="silent", contains="[99", fixed_contains="[1 2 3]")
bug("numpy", "np", "print(np.zeros(3, 3))", "print(np.zeros((3, 3)).shape)",
    "The shape is ONE argument: a tuple. The second positional argument of np.zeros is dtype.",
    contains="Cannot interpret", fixed_contains="(3, 3)")
bug("numpy", "np", "M = np.array([[1, 2], [2, 4]])\nprint(np.linalg.inv(M))", "M = np.array([[1, 2], [2, 4]])\nprint(np.linalg.det(M))\nprint(np.linalg.pinv(M).round(2))",
    "The second row is twice the first, so det = 0 and the matrix has no inverse. Check np.linalg.det first or use the pseudo-inverse pinv.",
    contains="Singular matrix", fixed_contains="0.")
bug("numpy", "np", "a = np.array([1, 2, 'x'])\nprint(a.mean())", "a = np.array([1, 2, 3])\nprint(a.mean())",
    "One string turns the whole array into dtype '<U21' (text), so arithmetic fails. Clean the data so that the dtype is numeric (check a.dtype).",
    contains="", fixed_contains="2.0")
bug("numpy", "np", "a = np.array([1, 2, 3, 4, 5])\nprint(a[(a > 1) and (a < 5)])", "a = np.array([1, 2, 3, 4, 5])\nprint(a[(a > 1) & (a < 5)])",
    "and / or / not work on single truth values. For arrays use & | ~ with brackets around each condition.",
    contains="truth value of an array", fixed_contains="[2 3 4]")

# ---------------------------------------------------------------- matplotlib / seaborn
bug("matplotlib", "plt", "plt.plot([1, 2, 3], [4, 5, 6, 7])", "plt.plot([1, 2, 3], [4, 5, 6])",
    "x and y must have the same length (3 vs 4).", contains="same first dimension")
bug("seaborn", "plt", "sns.barplot(x='City', y='Salary')", "sns.barplot(data=df, x='City', y='Salary')",
    "Column names are strings, so seaborn needs data=df to look them up. Without it it cannot interpret 'City'.",
    contains="Could not interpret")
bug("matplotlib", "plt", "plt.title = 'Salary by city'\nplt.plot([1, 2], [3, 4])\nplt.title('Salary by city')", "plt.plot([1, 2], [3, 4])\nplt.title('Salary by city')",
    "Using = replaced the function plt.title with a string, so calling it later fails. Call the function, do not assign to it.",
    contains="'str' object is not callable")
bug("matplotlib", "plt", "plt.scatter(df.Age, df.Salry)", "plt.scatter(df.Age, df.Salary)",
    "Misspelled column name (Salry). Attribute access df.Salary only works for exact names without spaces.",
    contains="no attribute 'Salry'")
bug("matplotlib", "plt", "plt.plot([1, 2, 3], [4, 5, 6])\nplt.legend()", "plt.plot([1, 2, 3], [4, 5, 6], label='trend')\nplt.legend()",
    "legend() only lists artists that have a label=. Without one the legend is empty and matplotlib just warns.",
    kind="warn", contains="No artists with labels")
bug("matplotlib", "plt", "plt.subplot(2, 2, 5)", "plt.subplot(2, 2, 4)",
    "A 2 x 2 grid has panels 1 to 4 only (numbered row by row from 1).", contains="num must be an integer")

# ---------------------------------------------------------------- BeautifulSoup / requests
bug("bs4", "bs", "quotes = soup.find_all('div', class='quote')", "quotes = soup.find_all('div', class_='quote')\nprint(len(quotes))",
    "class is a reserved word in Python. BeautifulSoup uses class_ (with the underscore), or attrs={'class': 'quote'}.",
    contains="invalid syntax", fixed_contains="2")
bug("bs4", "bs", "print(soup.find('span', class_='txt').text)", "tag = soup.find('span', class_='text')\nprint(tag.text if tag else 'not found')",
    "find returns None when nothing matches (wrong class name or JavaScript-rendered page). Test the result before using .text.",
    contains="'NoneType' object has no attribute 'text'", fixed_contains="Be yourself.")
bug("bs4", "bs", "print(soup.find_all('span', class_='text').text)", "print([s.text for s in soup.find_all('span', class_='text')])",
    "find_all returns a list-like ResultSet. Loop over it (or index it) and take .text of each tag.",
    contains="ResultSet", fixed_contains="Stay hungry.")
bug("bs4", "bs", "for div in soup.find_all('div', class_='quote'):\n    print(div.find('a')['href'])", "for div in soup.find_all('div', class_='quote'):\n    a = div.find('a')\n    print(a.get('href') if a else None)",
    "Indexing a tag with ['href'] raises KeyError if the attribute is missing; .get('href') returns None instead. The second quote even has no <a>.",
    contains="href", fixed_contains="None")
bug("bs4", "bs", "print(soup.find_all('span', class_='text')[5].text)", "spans = soup.find_all('span', class_='text')\nprint(spans[0].text if spans else 'none')",
    "Only two matches exist, so index 5 is out of range. Check len() before indexing.",
    contains="index out of range", fixed_contains="Be yourself.")
bug("requests", "bs", "r = requests.get('quotes.toscrape.com')", "r = requests.get('https://quotes.toscrape.com')  # needs internet",
    "The URL must start with http:// or https://. (Fix not run here: it needs a live network.)",
    contains="No scheme supplied", nofix=True)

# ---------------------------------------------------------------- Plotly
bug("plotly", "px", "fig = px.bar(df, x='City', y='Sale')", "fig = px.bar(df, x='City', y='Sales')\nprint(len(fig.data))",
    "The y column name does not exist in the DataFrame. The message lists the valid names.",
    contains="not the name of a column", fixed_contains="1")
bug("plotly", "px", "fig = go.Figure(go.Bar(x=df['City'], y=df['Sales']))\nfig.update_layout(titel='Sales')", "fig = go.Figure(go.Bar(x=df['City'], y=df['Sales']))\nfig.update_layout(title='Sales')\nprint(fig.layout.title.text)",
    "Misspelled layout property. Plotly validates property names and lists the valid ones.",
    contains="Invalid property specified", fixed_contains="Sales")
bug("plotly", "px", "go.Bar(x=df['City'], y=df['Sales'], color='red')", "bar = go.Bar(x=df['City'], y=df['Sales'], marker_color='red')\nprint(bar.marker.color)",
    "graph_objects have no color= shortcut (that is plotly.express). Use marker_color or marker=dict(color=...).",
    contains="Invalid property specified", fixed_contains="red")
bug("plotly", "px", "fig = px.bar(df, x='City', y='Sales')\nfig.write_image('sales.png')", "# pip install -U kaleido  (then the same call works)\nfig.write_image('sales.png')",
    "Static export needs the kaleido package. Install it with pip, or use fig.write_html('sales.html') which needs nothing extra.",
    contains="Kaleido", nofix=True)

# ---------------------------------------------------------------- Bokeh
bug("bokeh", "bk", "p = figure(plot_width=400, plot_height=300)", "p = figure(width=400, height=300)\nprint(p.width)",
    "plot_width / plot_height were removed in Bokeh 3. Use width and height.",
    contains="plot_width", fixed_contains="400")
bug("bokeh", "bk", "p = figure(width=300, height=300)\np.circle([1, 2, 3], [4, 5, 6], size=10)", "p = figure(width=300, height=300)\np.scatter([1, 2, 3], [4, 5, 6], size=10)\nprint(len(p.renderers))",
    "In Bokeh 3.4+ circle(size=...) is deprecated. Use scatter(), which also accepts a marker= argument.",
    kind="warn", contains="deprecated", fixed_contains="1")
bug("bokeh", "bk", "src = ColumnDataSource(dict(x=[1, 2, 3], y=[4, 5]))", "src = ColumnDataSource(dict(x=[1, 2, 3], y=[4, 5, 6]))\nprint(len(src.data['x']))",
    "All columns of a ColumnDataSource must have the same length; Bokeh only warns, then the plot misbehaves.",
    kind="warn", contains="same length", fixed_contains="3")

# ---------------------------------------------------------------- scikit-learn: PCA and KMeans
bug("PCA", "sk", "pca = PCA(n_components=5).fit(X)", "pca = PCA(n_components=2).fit(X)\nprint(pca.n_components_)",
    "Components cannot exceed min(n_samples, n_features); iris has 4 features.",
    contains="n_components=5 must be between", fixed_contains="2")
bug("PCA", "sk", "pca = PCA(n_components=2).fit(X)\nprint(pca.explained_variance_ratio_.round(4))", "Xs = StandardScaler().fit_transform(X)\npca = PCA(n_components=2).fit(Xs)\nprint(pca.explained_variance_ratio_.round(4))",
    "Not an error but a wrong analysis: PCA follows variance, so a large-scale feature dominates. Standardise first (PC1 falls from 92.46% to 72.96%).",
    kind="silent", contains="0.9246", fixed_contains="0.7296")
bug("PCA", "sk", "pca = PCA(n_components=2)\nprint(pca.explained_variance_ratio_)", "pca = PCA(n_components=2).fit(X)\nprint(pca.explained_variance_ratio_.round(2))",
    "Attributes ending in _ exist only after fit(). Call fit or fit_transform first.",
    contains="no attribute 'explained_variance_ratio_'", fixed_contains="[0.92 0.05]")
bug("PCA", "sk", "scaled = StandardScaler().fit_transform(X)\nprint(scaled.head())", "scaled = pd.DataFrame(StandardScaler().fit_transform(X), columns=X.columns)\nprint(scaled.head(2).shape)",
    "sklearn transformers return a NumPy array, which has no .head(). Wrap it in pd.DataFrame(..., columns=...).",
    contains="'numpy.ndarray' object has no attribute 'head'", fixed_contains="(2, 4)")
bug("PCA", "sk", "pcs = PCA(n_components=2).fit_transform(X)\nprint(pcs['PC1'])", "pcs = pd.DataFrame(PCA(n_components=2).fit_transform(X), columns=['PC1', 'PC2'])\nprint(pcs['PC1'].shape)",
    "fit_transform returns an ndarray, so a column name cannot index it. Create a DataFrame with named columns first.",
    contains="only integers, slices", fixed_contains="(150,)")
bug("KMeans", "sk", "km = KMeans(n_clusters=3, n_init=10, random_state=0).fit(df_iris)", "km = KMeans(n_clusters=3, n_init=10, random_state=0).fit(df_iris.drop(columns='species'))\nprint(sorted(np.bincount(km.labels_)))",
    "The species column is text. Clustering uses numeric features only, so drop the label column first.",
    contains="could not convert string to float", fixed_contains="[38, 50, 62]")

# ---------------------------------------------------------------- core python seen in the labs
bug("python", "none", "total = 5\nprint('Total: ' + total)", "total = 5\nprint('Total: ' + str(total))",
    "+ cannot join a str and an int. Convert with str() or use an f-string: f'Total: {total}'.",
    contains="can only concatenate str", fixed_contains="Total: 5")
bug("python", "none", "for i in range(3):\nprint(i)", "for i in range(3):\n    print(i)",
    "The loop body must be indented (4 spaces).", contains="expected an indented block", fixed_contains="2")
bug("python", "none", "nums = [4, 8, 6]\nprint(mean(nums))", "nums = [4, 8, 6]\nprint(sum(nums) / len(nums))",
    "mean is not a built-in. Import statistics.mean, or compute sum / len. The error NameError means a name was never defined or imported.",
    contains="'mean' is not defined", fixed_contains="6.0")
bug("python", "none", "lst = [1, 2]\nlst.append(3, 4)", "lst = [1, 2]\nlst.extend([3, 4])\nprint(lst)",
    "append adds one element. extend (or +) adds several.", contains="append() takes exactly one argument", fixed_contains="[1, 2, 3, 4]")
