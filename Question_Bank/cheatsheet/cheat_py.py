"""Format-1 rows (Task | Code) for the Python lab areas.
Every row is executed in order by verify_py.py, so the rows of a group form one runnable program.
A row is (task, code) or (task, code, "skip") when it must not be executed (opens a browser, needs the internet, ...).
"""

GROUPS = []


def group(gid, title, labs, rows, note=""):
    GROUPS.append({"id": gid, "title": title, "labs": labs, "rows": rows, "note": note})


# ----------------------------------------------------------------------------------------------- A
group("A", "Pandas basics: create, select, filter, add, sort, average", "Programs 1, 2", [
    ("Load package", "import pandas as pd"),
    ("Create the dataset (dictionary)", "data = {'Name': ['Alice', 'Bob', 'Charlie', 'David', 'Emma'],\n        'Age': [23, 30, 28, 35, 22],\n        'City': ['New York', 'London', 'Paris', 'Tokyo', 'Sydney']}"),
    ("Create the DataFrame and display it", "df = pd.DataFrame(data)\nprint(df)"),
    ("First rows, size and column names", "print(df.head(3))\nprint(df.shape, df.columns.tolist())"),
    ("Select only Name and Age columns", "name_age = df[['Name', 'Age']]\nprint(name_age)"),
    ("Filter rows where Age > 25", "filtered_df = df[df['Age'] > 25]\nprint(filtered_df)"),
    ("Filter with two conditions (and / or)", "both = df[(df['Age'] > 25) & (df['City'] != 'Paris')]\neither = df[(df['Age'] > 30) | (df['City'] == 'Sydney')]"),
    ("Filter with query()", "q = df.query('Age > 25')"),
    ("Add a column with a default value", "df['Country'] = 'India'\nprint(df)"),
    ("Add a derived column", "df['Age_Next_Year'] = df['Age'] + 1"),
    ("Sort by Age in descending order", "sorted_df = df.sort_values(by='Age', ascending=False)\nprint(sorted_df)"),
    ("Calculate the average Age", "average_age = df['Age'].mean()\nprint('Average Age =', average_age)"),
    ("Other statistics of a column", "print(df['Age'].max(), df['Age'].min(), df['Age'].median(), df['Age'].sum())"),
    ("Top 3 rows by Age", "top3 = df.sort_values('Age', ascending=False).head(3)"),
    ("Drop a column", "slim = df.drop(columns=['Age_Next_Year'])"),
    ("Product table: 20 ids with a list comprehension", "amounts = [45000, 62000, 78000, 35000, 91000, 54000, 28000,\n           67000, 83000, 41000, 56000, 72000, 39000, 88000,\n           47000, 61000, 95000, 33000, 70000, 58000]\nsales = pd.DataFrame({'ProductID': [f'PRD{i}' for i in range(1, 21)],\n                      'SalesAmount': amounts,\n                      'Category': ['Electronics', 'Clothing', 'Electronics',\n                                   'Grocery', 'Home'] * 4})"),
    ("Filter SalesAmount > 50000 and add Region", "big = sales[sales['SalesAmount'] > 50000].copy()\nbig['Region'] = 'South India'"),
    ("Group by category: total, sorted", "cat_sales = sales.groupby('Category')['SalesAmount'].sum().sort_values(ascending=False)\nprint(cat_sales)"),
    ("Best and weakest category", "print(cat_sales.idxmax(), cat_sales.max(), cat_sales.idxmin(), cat_sales.min())"),
    ("Count rows per category", "print(sales['Category'].value_counts())"),
    ("Export to CSV and JSON", "sales.to_csv('sales.csv', index=False)\nsales.to_json('sales.json', orient='records', indent=2)"),
])

# ----------------------------------------------------------------------------------------------- B
group("B", "Pandas inspection, missing values, cleaning, scaling", "Programs 3, 4", [
    ("Load packages", "import pandas as pd\nimport numpy as np"),
    ("DataFrame from nested lists", "stud = [['Jhon', 20, 85], ['Mary', 21, 90], ['David', 19, 78]]\ndf0 = pd.DataFrame(stud, columns=['Name', 'Age', 'Marks'])"),
    ("Core attributes", "print(df0.size, df0.shape, df0.ndim)\nprint(df0.columns, df0.index)\nprint(df0.dtypes)"),
    ("Select one column / several columns", "print(df0['Name'])\nprint(df0[['Name', 'Age']])"),
    ("loc (labels) and iloc (positions)", "print(df0.loc[0, 'Name'], df0.iloc[0:2, 0:2])"),
    ("Dataset with missing values", "data = {'Name': ['Alice', 'Bob', np.nan, 'David', 'Emma'],\n        'Age': [23.0, np.nan, 28.0, 35.0, np.nan],\n        'City': ['New York', 'London', 'Paris', np.nan, 'Sydney']}\ndf = pd.DataFrame(data)"),
    ("Detect missing values", "print(df.isnull())\nprint(df.isnull().sum())\nprint(df.notnull())"),
    ("Preview: fill every NaN with 0", "fill_0 = df.fillna(0)"),
    ("Fill Age with the mean age", "mean_age = df['Age'].mean()\ndf['Age'] = df['Age'].fillna(mean_age)\nprint(df)"),
    ("Drop rows where Name or City is missing", "df = df.dropna(subset=['Name', 'City'])\nprint(df)"),
    ("Convert Age to integer", "df['Age'] = df['Age'].astype(int)\nprint(df.dtypes)"),
    ("Min-max scaling of Age", "df['Norm_Age'] = (df['Age'] - df['Age'].min()) / (df['Age'].max() - df['Age'].min())\nprint(df)"),
    ("Remove duplicates, reset the index", "df = df.drop_duplicates().reset_index(drop=True)"),
    ("Rename a column, clean text", "df = df.rename(columns={'Norm_Age': 'Age_Scaled'})\ndf['Name'] = df['Name'].str.strip().str.title()"),
    ("Fleet example: fill with mean then drop", "fleet = pd.DataFrame({'VehicleID': ['V101', 'V102', 'V103'], 'FuelConsumption': [15.0, np.nan, 22.0], 'Route': ['R1', 'R2', np.nan]})\nfleet['FuelConsumption'] = fleet['FuelConsumption'].fillna(fleet['FuelConsumption'].mean())\nfleet = fleet.dropna(subset=['VehicleID', 'Route'])"),
    ("Flag with np.where / group report", "fleet['Level'] = np.where(fleet['FuelConsumption'] >= 18, 'High', 'Low')\nreport = fleet.groupby('Route')['FuelConsumption'].agg(['sum', 'mean']).reset_index()"),
], note="Order matters: fillna first, then dropna, then astype(int) (an int column cannot hold NaN), then scaling.")

# ----------------------------------------------------------------------------------------------- C
group("C", "NumPy arrays: create, statistics, slice, reshape, multiply", "Programs 5, 6", [
    ("Load package", "import numpy as np"),
    ("Random integers 0..10 in a (3, 4) array", "np.random.seed(0)\narr = np.random.randint(0, 11, size=(3, 4))\nprint(arr)"),
    ("Shape, size, dtype", "print(arr.shape, arr.size, arr.dtype)"),
    ("Mean and standard deviation of the whole array", "print(np.mean(arr))\nprint(np.std(arr))"),
    ("First two rows and last two columns", "sub = arr[:2, -2:]\nprint(sub)"),
    ("Reshape to (4, 3)", "reshaped = arr.reshape(4, 3)\nprint(reshaped)"),
    ("Element-wise multiplication with another (4, 3) array", "other = np.random.randint(1, 5, size=(4, 3))\nproduct = reshaped * other\nprint(product)"),
    ("Explicit 4 x 5 array", "production = np.array([[120, 135, 128, 110, 140],\n                       [95, 105, 100, 90, 98],\n                       [150, 145, 160, 155, 148],\n                       [80, 85, 78, 82, 75]])"),
    ("Slice first 3 rows and last 2 columns", "print(production[:3, -2:])"),
    ("Reshape (4, 5) to (5, 4) and multiply by a weight matrix", "w = np.full((5, 4), 0.9)\neffective = production.reshape(5, 4) * w"),
    ("Row-wise and column-wise statistics", "print(np.mean(production, axis=1))\nprint(np.sum(production, axis=0))"),
    ("Rank rows by total (highest first)", "totals = np.sum(production, axis=1)\nranking = np.argsort(totals)[::-1]\nprint(ranking)"),
    ("Shifts below the overall average", "shift_avg = np.mean(production, axis=0)\nlow = np.where(shift_avg < shift_avg.mean())[0]"),
    ("Label values with np.where", "labels = np.where(totals >= totals.mean(), 'High', 'Low')"),
    ("Matrix product and transpose", "m = production @ production.T\nprint(m.shape, production.T.shape)"),
    ("Useful creators", "print(np.arange(0, 10, 2), np.linspace(0, 1, 5), np.zeros((2, 2)), np.ones(3))"),
], note="np.std divides by n (population). For the sample standard deviation use np.std(a, ddof=1). randint(0, 11) gives 0..10 because the upper bound is excluded.")

# ----------------------------------------------------------------------------------------------- D
group("D", "Feature engineering and EDA with Matplotlib / Seaborn", "Programs 7, 8", [
    ("Load packages", "import numpy as np\nimport pandas as pd\nimport matplotlib\nmatplotlib.use('Agg')\nimport matplotlib.pyplot as plt\nimport seaborn as sns"),
    ("Create random data", "np.random.seed(42)\ndf = pd.DataFrame({'Feature1': np.random.rand(50) * 100 + 1,\n                   'Feature2': np.random.randn(50) * 15 + 50,\n                   'Target': np.random.randint(0, 2, 50)})"),
    ("Logarithm of Feature1", "df['Log_Feature1'] = np.log(df['Feature1'])"),
    ("Bin Feature2 into low / medium / high", "df['Feature2_Bin'] = pd.cut(df['Feature2'], bins=3, labels=['low', 'medium', 'high'])\nprint(df['Feature2_Bin'].value_counts())"),
    ("Bin with your own limits", "df['Band'] = pd.cut(df['Feature2'], bins=[0, 45, 55, np.inf], labels=['Optimal', 'Moderate', 'Degraded'], right=False)"),
    ("Bin with an if / elif function", "def categorize(v):\n    if v < 45:\n        return 'Normal'\n    elif v < 55:\n        return 'Elevated'\n    else:\n        return 'Hypertensive'\ndf['Level'] = df['Feature2'].apply(categorize)"),
    ("Correlation matrix", "corr = df[['Feature1', 'Feature2', 'Target', 'Log_Feature1']].corr()\nprint(corr)"),
    ("Scatter plot coloured by Target", "plt.figure(figsize=(6, 4))\nplt.scatter(df['Feature1'], df['Feature2'], c=df['Target'], cmap='viridis')\nplt.colorbar(label='Target')\nplt.xlabel('Feature1')\nplt.ylabel('Feature2')\nplt.title('Feature1 vs Feature2 by Target')"),
    ("Save the figure, then show it", "plt.savefig('scatter.png', dpi=120)\nplt.show()"),
    ("Seaborn scatter with hue", "plt.figure()\nsns.scatterplot(x='Feature1', y='Feature2', hue='Target', data=df)"),
    ("Box plot of a value grouped by category", "plt.figure()\nsns.boxplot(x='Target', y='Feature2', data=df)"),
    ("Heatmap of the correlation matrix", "plt.figure()\nsns.heatmap(corr, annot=True, cmap='coolwarm')"),
    ("Two plots side by side", "fig, axes = plt.subplots(1, 2, figsize=(10, 4))\naxes[0].hist(df['Feature2'], bins=8)\naxes[0].set_title('Feature2')\naxes[1].bar(['low', 'medium', 'high'], df['Feature2_Bin'].value_counts().reindex(['low', 'medium', 'high']))\naxes[1].set_title('Bins')\nplt.tight_layout()"),
    ("Interpretation sentence", "# Feature1 and Log_Feature1 correlate strongly (the log is a monotone transform);\n# correlation of Feature2 with Target is near 0, so the groups overlap in the scatter plot."),
], note="Call plt.savefig() BEFORE plt.show(): after show() the figure is closed and the saved file is blank.")

# ----------------------------------------------------------------------------------------------- E
group("E", "Web scraping with Beautiful Soup, then CSV / JSON / statistics", "Programs 9, 10", [
    ("Load packages", "import requests\nfrom bs4 import BeautifulSoup\nimport pandas as pd\nimport json"),
    ("Fetch a live page (guarded)", "resp = requests.get('https://quotes.toscrape.com', timeout=3)\nhtml = resp.text if resp.status_code == 200 else ''", "skip"),
    ("Offline HTML fallback used in the lab", "html_doc = \"\"\"\n<div class='quote'>\n  <span class='text'>\"Stay hungry, stay foolish.\"</span>\n  <small class='author'>Steve Jobs</small>\n  <div class='tags'><a class='tag'>inspirational</a><a class='tag'>wisdom</a></div>\n</div>\n<div class='quote'>\n  <span class='text'>\"Knowledge is power.\"</span>\n  <small class='author'>Francis Bacon</small>\n  <div class='tags'><a class='tag'>knowledge</a><a class='tag'>wisdom</a></div>\n</div>\n<div class='quote'>\n  <span class='text'>\"Imagination is more important than knowledge.\"</span>\n  <small class='author'>Steve Jobs</small>\n  <div class='tags'><a class='tag'>imagination</a></div>\n</div>\n\"\"\""),
    ("Parse the HTML", "soup = BeautifulSoup(html_doc, 'html.parser')"),
    ("Find all repeated blocks", "cards = soup.find_all('div', class_='quote')\nprint(len(cards))"),
    ("Extract text, author and tags of each block", "records = []\nfor card in cards:\n    text_elem = card.find('span', class_='text')\n    author_elem = card.find('small', class_='author')\n    tags = [t.get_text().strip() for t in card.find_all('a', class_='tag')]\n    quote = text_elem.get_text().strip('\"') if text_elem else 'N/A'\n    author = author_elem.get_text().strip() if author_elem else 'Unknown'\n    records.append({'Quote': quote, 'Author': author, 'Tags': ', '.join(tags), 'Tag_Count': len(tags), 'Quote_Length': len(quote)})"),
    ("Build the DataFrame", "scraped_df = pd.DataFrame(records)\nprint(scraped_df.head())"),
    ("Export to CSV and JSON", "scraped_df.to_csv('quotes.csv', index=False)\nscraped_df.to_json('quotes.json', orient='records', indent=2)"),
    ("Author frequency", "author_counts = scraped_df['Author'].value_counts()\nprint(author_counts)"),
    ("Descriptive statistics", "print(scraped_df[['Quote_Length', 'Tag_Count']].describe().round(2))"),
    ("Most frequent tags", "all_tags = [t.strip() for s in scraped_df['Tags'] for t in s.split(',') if t.strip()]\nprint(pd.Series(all_tags).value_counts().head(5))"),
    ("CSS-selector alternative", "texts = [e.get_text() for e in soup.select('div.quote span.text')]"),
    ("Job cards: number parsed from text", "job_html = \"\"\"\n<div class='job-card'><h2 class='title'>Data Engineer</h2>\n  <span class='loc'>Pune</span><span class='sal'>26 LPA</span></div>\n<div class='job-card'><h2 class='title'>ML Engineer</h2>\n  <span class='loc'>Pune</span><span class='sal'>22 LPA</span></div>\n<div class='job-card'><h2 class='title'>DevOps</h2>\n  <span class='loc'>Chennai</span><span class='sal'>18 LPA</span></div>\n\"\"\"\njobs = []\nfor c in BeautifulSoup(job_html, 'html.parser').find_all('div', class_='job-card'):\n    salary = float(c.find('span', class_='sal').text.replace(' LPA', '').strip())\n    jobs.append({'Job_Title': c.find('h2', class_='title').text,\n                 'Location': c.find('span', class_='loc').text,\n                 'Salary_LPA': salary})\njob_df = pd.DataFrame(jobs)"),
    ("Group and aggregate (named aggregation)", "loc_stats = job_df.groupby('Location').agg(Job_Count=('Job_Title', 'count'), Average_Salary_LPA=('Salary_LPA', 'mean')).sort_values(by='Job_Count', ascending=False)\nprint(loc_stats)"),
    ("Bar chart of the counts", "import matplotlib\nmatplotlib.use('Agg')\nimport matplotlib.pyplot as plt\nplt.figure()\nplt.bar(loc_stats.index, loc_stats['Job_Count'], color='steelblue', edgecolor='black')\nplt.title('Openings by city')\nplt.xlabel('City')\nplt.ylabel('Count')\nplt.savefig('jobs.png', dpi=120)"),
], note="find() returns the first match (or None); find_all() returns a list. class is a Python keyword, so the argument is class_.")

# ----------------------------------------------------------------------------------------------- F
group("F", "Plotly Express: interactive bar and scatter with trendline", "Programs 11, 12", [
    ("Load packages", "import numpy as np\nimport pandas as pd\nimport plotly.express as px"),
    ("Dataset and derived indicators", "df = pd.DataFrame({'IT_Hub': ['Bengaluru', 'Hyderabad', 'Pune', 'Chennai'],\n                   'Workforce_K': [1650.0, 1150.0, 820.0, 780.0],\n                   'Export_Billion_USD': [78.5, 52.0, 36.2, 34.0]})\ndf['National_Share_Pct'] = (df['Workforce_K'] / df['Workforce_K'].sum() * 100).round(2)\ndf['Export_Per_Worker_USD'] = (df['Export_Billion_USD'] * 1e9 / (df['Workforce_K'] * 1000)).round(2)\ndf = df.sort_values(by='Workforce_K', ascending=False).reset_index(drop=True)"),
    ("Interactive bar chart", "fig = px.bar(df, x='IT_Hub', y='Workforce_K', color='Workforce_K', color_continuous_scale='Tealgrn',\n             text='Workforce_K', title='Tech workforce by hub',\n             labels={'Workforce_K': 'Workforce (thousands)', 'IT_Hub': 'Hub'})"),
    ("Value labels and hover template", "fig.update_traces(texttemplate='%{text:.0f}k', textposition='outside',\n                  hovertemplate='<b>%{x}</b><br>Workforce: %{y:,.1f}k<extra></extra>')"),
    ("Layout: titles, axis range, background", "fig.update_layout(title_font=dict(size=18), xaxis=dict(tickangle=-25), yaxis=dict(range=[0, 1900]),\n                  plot_bgcolor='rgba(245,248,250,1)', margin=dict(l=60, r=40, t=70, b=80))"),
    ("Show on screen / save as HTML", "fig.show()\nfig.write_html('hubs.html')"),
    ("Save as PNG (needs kaleido)", "fig.write_image('hubs.png', width=750, height=450, scale=2)", "skip"),
    ("Scatter data and correlation", "np.random.seed(42)\narea = np.sort(np.random.uniform(15000, 120000, 30))\nlease = area * np.random.uniform(1100, 1550, 30) / 100000.0 + np.random.normal(0, 15, 30)\nprop = pd.DataFrame({'Floor_Area_SqFt': area.round(0), 'Annual_Lease_Lakhs': lease.round(2),\n                     'Occupancy_Pct': np.clip(np.random.normal(88, 7, 30), 65, 99).round(1)})\nprint(prop['Floor_Area_SqFt'].corr(prop['Annual_Lease_Lakhs']))"),
    ("Least-squares line (slope, intercept)", "slope, intercept = np.polyfit(prop['Floor_Area_SqFt'], prop['Annual_Lease_Lakhs'], 1)\nprint(slope, intercept)"),
    ("Scatter with size, colour scale and OLS trendline", "fig2 = px.scatter(prop, x='Floor_Area_SqFt', y='Annual_Lease_Lakhs', size='Occupancy_Pct',\n                  color='Annual_Lease_Lakhs', color_continuous_scale='Plasma',\n                  trendline='ols', trendline_color_override='#222222', title='Area vs lease')"),
    ("Hover text from other columns", "fig2.update_traces(marker=dict(opacity=0.88, line=dict(width=1.5, color='black')), selector=dict(mode='markers'))\nfig2.update_layout(coloraxis_colorbar=dict(title='Lease', thickness=15, len=0.75))"),
    ("Annotation text on the chart", "fig2.add_annotation(x=70000, y=350, text='Linear fit', showarrow=False)\nfig2.write_html('lease.html')"),
], note="trendline='ols' needs statsmodels; write_image needs kaleido (>=1) installed.")

# ----------------------------------------------------------------------------------------------- G
group("G", "Bokeh: scatter, multi-line and bar charts", "Programs 13, 14, 15", [
    ("Load packages", "import pandas as pd\nfrom sklearn.datasets import load_iris\nfrom bokeh.plotting import figure, show, output_file, save\nfrom bokeh.models import ColumnDataSource, HoverTool, LabelSet\nfrom bokeh.transform import factor_cmap"),
    ("Iris data frame with species names", "raw = load_iris()\ndf = pd.DataFrame(raw.data, columns=['sepal_length', 'sepal_width', 'petal_length', 'petal_width'])\nnames = ['Setosa', 'Versicolor', 'Virginica']\ndf['species'] = [names[i] for i in raw.target]"),
    ("Wrap the data in a ColumnDataSource", "source = ColumnDataSource(df)"),
    ("Colour map by category", "color_map = factor_cmap('species', palette=['#D95F02', '#7570B3', '#1B9E77'], factors=names)"),
    ("Hover tool (fields start with @)", "hover = HoverTool(tooltips=[('Species', '@species'), ('Petal Length', '@petal_length{0.1f} cm'), ('Sepal Length', '@sepal_length{0.1f} cm')])"),
    ("Create the figure", "p = figure(title='Petal vs sepal length', x_axis_label='Petal Length (cm)', y_axis_label='Sepal Length (cm)',\n           width=720, height=440, tools=[hover, 'pan', 'wheel_zoom', 'box_zoom', 'reset', 'save'])"),
    ("Scatter glyph with legend", "p.scatter('petal_length', 'sepal_length', source=source, color=color_map, size=11, alpha=0.82, legend_field='species')\np.legend.location = 'top_left'"),
    ("Output file and show", "output_file('iris_bokeh.html')\nshow(p)"),
    ("Multi-line data", "days = [f'Day {i}' for i in range(1, 8)]\nnet = pd.DataFrame({'Day': days, 'US_East_ms': [45.2, 48.1, 42.6, 51.3, 47.0, 44.5, 49.2],\n                    'AP_South_ms': [28.5, 31.2, 29.8, 36.4, 33.1, 30.2, 34.7], 'SLA_Limit_ms': [100.0] * 7})\nsrc2 = ColumnDataSource(net)"),
    ("Line figure with a categorical x axis", "p2 = figure(title='Latency', x_range=days, width=720, height=440, tools=['pan', 'wheel_zoom', 'reset', 'save'])"),
    ("One line per series, with markers", "p2.line('Day', 'US_East_ms', source=src2, legend_label='US-East', line_width=3, color='#386CB0')\np2.scatter('Day', 'US_East_ms', source=src2, size=8, color='#386CB0', fill_color='white')\np2.line('Day', 'AP_South_ms', source=src2, legend_label='AP-South', line_width=3, color='#33A02C')"),
    ("Dashed threshold line", "p2.line('Day', 'SLA_Limit_ms', source=src2, legend_label='SLA 100 ms', line_width=2, color='#E41A1C', line_dash='dashed')"),
    ("Clickable legend", "p2.legend.location = 'top_left'\np2.legend.click_policy = 'hide'"),
    ("Bar chart data", "cost = pd.DataFrame({'Department': ['AI Research', 'Engineering', 'Data Platform'], 'Actual_Spend_USD_K': [485.0, 365.0, 280.0]})\ncost['Spend_Label'] = [f'${int(a)}k' for a in cost['Actual_Spend_USD_K']]\nsrc3 = ColumnDataSource(cost)\ndept = cost['Department'].tolist()"),
    ("Bar chart (vbar) with a categorical axis", "p3 = figure(x_range=dept, title='Spend by department', width=720, height=440)\np3.vbar(x='Department', top='Actual_Spend_USD_K', width=0.62, source=src3,\n        color=factor_cmap('Department', palette=['#e41a1c', '#377eb8', '#4daf4a'], factors=dept), legend_field='Department')"),
    ("Numbers on top of the bars (LabelSet)", "labels = LabelSet(x='Department', y='Actual_Spend_USD_K', text='Spend_Label', level='glyph', x_offset=-16, y_offset=4, source=src3)\np3.add_layout(labels)\np3.xaxis.major_label_orientation = 0.35"),
    ("Save to HTML / export image", "save(p3, filename='bar_bokeh.html')\n# export_png(p3, filename='bar.png')   needs selenium + a browser driver", ),
], note="Bokeh 3 uses p.scatter(...) for markers and legend_field= / legend_label=; the old legend= argument was removed.")

# ----------------------------------------------------------------------------------------------- H
group("H", "scikit-learn: StandardScaler, PCA, K-means, silhouette, crosstab", "Programs 16, 17", [
    ("Load packages", "import pandas as pd\nfrom sklearn.datasets import load_iris\nfrom sklearn.preprocessing import StandardScaler\nfrom sklearn.decomposition import PCA\nfrom sklearn.cluster import KMeans\nfrom sklearn.metrics import silhouette_score\nimport plotly.express as px"),
    ("Load Iris, features and labels", "iris = load_iris()\nX = iris.data\ny = iris.target\nfeature_names = ['Sepal_Length', 'Sepal_Width', 'Petal_Length', 'Petal_Width']\nspecies_names = ['Setosa', 'Versicolor', 'Virginica']"),
    ("Standardise the features", "scaler = StandardScaler()\nX_scaled = scaler.fit_transform(X)"),
    ("Fit PCA on all components: variance ratios", "pca_full = PCA(n_components=4)\npca_full.fit(X_scaled)\nvar_ratios = pca_full.explained_variance_ratio_\ncum_var = var_ratios.cumsum()\nprint(var_ratios.round(4), cum_var.round(4))"),
    ("Scree table", "scree_df = pd.DataFrame({'Principal_Component': ['PC1', 'PC2', 'PC3', 'PC4'],\n                         'Explained_Variance_Pct': (var_ratios * 100).round(2),\n                         'Cumulative_Variance_Pct': (cum_var * 100).round(2)})\nprint(scree_df.to_string(index=False))"),
    ("Reduce to 2 components", "pca_2d = PCA(n_components=2)\nX_pca = pca_2d.fit_transform(X_scaled)\npca_df = pd.DataFrame(X_pca, columns=['PC1', 'PC2'])\npca_df['Species'] = [species_names[i] for i in y]"),
    ("Component loadings (eigenvectors)", "loadings = pd.DataFrame(pca_2d.components_.T, columns=['PC1_Loading', 'PC2_Loading'], index=feature_names).round(4)\nprint(loadings)"),
    ("Interactive 2-D scatter of the components", "fig = px.scatter(pca_df, x='PC1', y='PC2', color='Species', symbol='Species',\n                 labels={'PC1': f'PC1 ({var_ratios[0] * 100:.2f}%)', 'PC2': f'PC2 ({var_ratios[1] * 100:.2f}%)'})\nfig.show()"),
    ("Inertia and silhouette for k = 2..6", "k_vals = list(range(2, 7))\ninertias, sils = [], []\nfor k in k_vals:\n    km = KMeans(n_clusters=k, random_state=42, n_init=10)\n    labels = km.fit_predict(X_scaled)\n    inertias.append(round(km.inertia_, 2))\n    sils.append(round(silhouette_score(X_scaled, labels), 4))\nprint(pd.DataFrame({'k': k_vals, 'Inertia': inertias, 'Silhouette': sils}))"),
    ("Final model with k = 3", "kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)\ncluster_labels = kmeans.fit_predict(X_scaled)\nprint(kmeans.inertia_, silhouette_score(X_scaled, cluster_labels))"),
    ("Cluster table with true species", "k3_df = pd.DataFrame(X, columns=feature_names)\nk3_df['Cluster'] = [f'Cluster {c}' for c in cluster_labels]\nk3_df['True_Species'] = [species_names[i] for i in y]"),
    ("Contingency matrix: clusters vs real species", "ct = pd.crosstab(k3_df['True_Species'], k3_df['Cluster'], margins=True)\nprint(ct)"),
    ("Centroids back in original units", "centroids = pd.DataFrame(scaler.inverse_transform(kmeans.cluster_centers_), columns=feature_names)\nprint(centroids.round(2))"),
    ("Interactive 3-D scatter", "fig3 = px.scatter_3d(k3_df, x='Sepal_Length', y='Petal_Length', z='Petal_Width', color='Cluster')\nfig3.show()"),
    ("Save the plot", "fig3.write_html('kmeans3d.html')"),
], note="fit_transform on training data only; kmeans.labels_ and pca.explained_variance_ratio_ end with an underscore (learned attributes).")
