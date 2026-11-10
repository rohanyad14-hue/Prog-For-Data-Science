from dsl import *

mcqs = [
    MCQ("For a DataFrame with the default integer index, `df.loc[1:3]` and `df.iloc[1:3]` return respectively:",
        ["3 rows and 3 rows", "3 rows and 2 rows", "2 rows and 3 rows", "2 rows and 2 rows"], 1,
        "`loc` slices by label and includes the end label (rows 1, 2, 3). `iloc` slices by position and excludes the end (rows 1, 2)."),
    MCQ("Which array can be broadcast against an array of shape (3, 4) in an addition?",
        ["shape (3,)", "shape (4,)", "shape (2, 4)", "shape (3, 2)"], 1,
        "Compare trailing dimensions: (4,) matches 4. (3,) would be compared with 4 and fails; (2,4) fails on 2 vs 3; (3,2) fails on 2 vs 4."),
    MCQ("`pd.merge(a, b, on='k', how='left')` returns:",
        ["only keys present in both", "all rows of `a`, with NaN where `b` has no match",
         "all rows of `b`, with NaN where `a` has no match", "the Cartesian product"], 1,
        "A left join keeps every left row. Use `inner` for matches only and `outer` for the union of keys."),
    MCQ("`df.groupby('city')['sales'].sum()` is an example of:",
        ["map-reduce on disk", "split-apply-combine", "broadcasting", "one-hot encoding"], 1,
        "Split the rows by city, apply `sum` to each group, combine the results into one Series."),
    MCQ("Which call removes every row that has at least one missing value?",
        ["`df.fillna(0)`", "`df.dropna()`", "`df.isna()`", "`df.drop_duplicates()`"], 1,
        "`dropna()` drops rows (axis=0) containing NaN; `subset=[...]` restricts the check to some columns."),
    MCQ("Scrapy achieves high crawl throughput mainly because it is built on:",
        ["multiprocessing only", "the Twisted asynchronous, event-driven engine", "Selenium", "a single blocking loop"], 1,
        "Non-blocking I/O lets one process keep many requests in flight while others wait for the network."),
    MCQ("Which library is used to draw interactive maps with markers (Leaflet-based)?",
        ["Seaborn", "Bokeh", "Folium", "SciPy"], 2, "Folium wraps Leaflet.js: `folium.Map(...)`, `folium.Marker(...)`, saved as HTML."),
    MCQ("Before running K-means or PCA on features measured in very different units you should:",
        ["drop the target", "standardise the features", "convert them to strings", "sort the rows"], 1,
        "Both methods use distances or variance, so large-scale features dominate unless scaled (`StandardScaler`)."),
    MCQ("XGBoost is best described as:",
        ["a deep learning framework", "an optimised gradient-boosted decision tree library", "a plotting library", "a web scraper"], 1,
        "It builds trees sequentially, each correcting the previous errors; very strong on tabular data."),
    MCQ("`pd.concat([a, b], axis=1)` does what?",
        ["stacks `b` below `a`", "places `b` beside `a`, aligning on the index", "merges on a key column", "removes duplicates"], 1,
        "axis=0 stacks rows (union of rows), axis=1 joins columns side by side."),
]

shorts = [
    SHORT("Differentiate a pandas Series from a DataFrame, and show how to create each.", 3, [
        P("A <b>Series</b> is a one-dimensional labelled array (values + index) with a single dtype. A <b>DataFrame</b> is a two-dimensional "
          "table of aligned Series sharing one index; each column can have its own dtype."),
        SNIP("import pandas as pd\ns = pd.Series([22, 31, 27], index=['a', 'b', 'c'], name='Age')\n"
             "df = pd.DataFrame({'Name': ['Asha', 'Ravi', 'Meena'], 'Age': [22, 31, 27]})\n"
             "type(df['Age'])    # Series: one column of a DataFrame")]),
    SHORT("Describe four ways of handling missing values in pandas and when each is suitable.", 5, [
        T(["Method", "Code", "Use when"], [
            ["Detect", "`df.isna().sum()`", "always first: count NaN per column"],
            ["Drop rows", "`df.dropna(subset=['Name','City'])`", "key columns are missing and cannot be guessed; few rows lost"],
            ["Fill with a statistic", "`df['Age'].fillna(df['Age'].mean())`", "numeric column, roughly symmetric (use median if skewed)"],
            ["Forward / back fill, interpolate", "`ffill()`, `bfill()`, `interpolate()`", "ordered data such as time series"],
            ["Fill with a constant or category", "`fillna('Unknown')`", "categorical column where \"missing\" is informative"]], [0.22, 0.42, 0.36])]),
    SHORT("Distinguish `.loc`, `.iloc` and boolean filtering with examples.", 3, [
        B(["`df.loc[1:2, 'Name']`: label based, end label included.",
           "`df.iloc[1:2, 0]`: position based, end excluded.",
           "`df[df['Age'] > 25]`: boolean mask selects rows that satisfy a condition; combine with `&`, `|` and parentheses: "
           "`df[(df.Age > 25) & (df.City == 'Pune')]`."])]),
    SHORT("Compare `merge`, `join` and `concat` in pandas.", 5, [
        T(["", "merge", "join", "concat"], [
            ["Matches on", "column values (`on=`, `left_on=`, `right_on=`)", "the index of the right frame (by default)", "the index / position, no key logic"],
            ["Types", "`inner`, `left`, `right`, `outer`", "same `how` options", "stacks rows (axis=0) or columns (axis=1)"],
            ["Typical use", "SQL-style join of two tables on a key", "shortcut for index-based joins", "append monthly files, glue columns"],
            ["Example", "`pd.merge(c, o, on='cust_id', how='left')`", "`c.join(o.set_index('cust_id'), on='cust_id')`", "`pd.concat([a, b], axis=0)`"]],
          [0.14, 0.32, 0.27, 0.27])]),
    SHORT("Why is NumPy faster than Python lists for numerical work?", 3, [
        B(["An `ndarray` stores one fixed dtype in a contiguous block of memory; a list stores pointers to separate Python objects.",
           "Operations are <b>vectorised</b>: the loop runs in compiled C instead of the Python interpreter, with no per-element type check.",
           "Broadcasting and slicing create views without copying, saving time and memory.",
           "Measured here (Python 3.10, one million integers): `a * 2` took 2.5 ms, the list comprehension `[x * 2 for x in l]` took 96 ms, about 38 times slower. "
           "Your ratio will differ by machine."])]),
    SHORT("How do you work with text data in a DataFrame? Give four `.str` operations.", 3, [
        SNIP("df['name'] = df['name'].str.strip().str.title()\ndf[df['name'].str.contains('sh', case=False)]\n"
             "df['first'] = df['name'].str.split().str[0]\ndf['email'].str.endswith('.ac.in')\n"
             "df['name'].str.replace(r'\\s+', ' ', regex=True)"),
        P("The `.str` accessor applies string methods to a whole column and propagates NaN instead of raising.")]),
    SHORT("Compare Matplotlib and Seaborn.", 3, [
        P("Matplotlib is the low-level base library: full control of figures, axes and styles, static output. Seaborn is built on "
          "Matplotlib and works directly with DataFrames; it offers statistical plots (`histplot`, `boxplot`, `heatmap`, `pairplot`) "
          "and attractive defaults with one line of code. Use Seaborn for quick exploration, Matplotlib to customise details.")]),
    SHORT("State the role of SciPy, scikit-learn, Keras, TensorFlow, PyTorch and XGBoost in one line each.", 5, [
        T(["Library", "Role"], [
            ["SciPy", "scientific algorithms on arrays: optimisation, statistics, linear algebra, signal processing, sparse matrices"],
            ["scikit-learn", "classical machine learning with a uniform `fit / predict / transform` API: regression, classification, clustering, PCA, pipelines"],
            ["TensorFlow", "Google's deep learning framework with tools for deployment (serving, mobile, browser)"],
            ["Keras", "high-level neural-network API (`Sequential`, `Model`) that runs on TensorFlow and other backends"],
            ["PyTorch", "deep learning with dynamic (define-by-run) graphs; popular for research and prototyping"],
            ["XGBoost", "gradient-boosted decision trees, often the strongest model for tabular data"]], [0.2, 0.8])]),
    SHORT("What is `robots.txt` and what are the rules of responsible scraping?", 3, [
        B(["`robots.txt` at the site root tells crawlers which paths they may fetch. Scrapy obeys it with `ROBOTSTXT_OBEY = True`.",
           "Throttle requests (`DOWNLOAD_DELAY`, `AUTOTHROTTLE_ENABLED`), identify your crawler with a User-Agent, "
           "respect the site's terms of service and do not collect personal data without a lawful basis.",
           "Prefer an official API when one exists."])]),
]

# ------------------------------------------------------------------------------------------------ longs
c1_prompt = [
    P("(Lab experiments 1 and 2) <b>Part A.</b> Create a DataFrame with columns Name, Age and City for five individuals. "
      "Select only Name and Age; filter rows where Age is greater than 25; add a column Country with a default value; "
      "sort by Age in descending order; calculate the average age."),
    P("<b>Part B.</b> Create a DataFrame with missing values in Name, Age and City. Fill missing Age values with the mean age, "
      "drop rows where Name or City is missing, convert Age to integer, and normalise Age with min-max scaling. Explain each step."),
]
c1_answer = [
    H3("Concepts"),
    B(["A DataFrame is a labelled 2-D table. `df[['Name','Age']]` (double brackets) returns a DataFrame with those columns; "
       "a boolean mask `df[df.Age > 25]` filters rows; assigning a scalar to a new column broadcasts it to every row.",
       "`sort_values('Age', ascending=False)` returns a new sorted frame (original unchanged unless `inplace=True`).",
       "Missing-value pipeline: `isna().sum()` to inspect, `fillna(mean)` for numeric gaps, `dropna(subset=[...])` for rows missing key fields, "
       "`astype(int)` after the NaNs are gone (an int column cannot hold NaN).",
       "Min-max scaling maps values to [0, 1]: <b>x' = (x - min) / (max - min)</b>."]),
    WARN("The mean in the output below (32.0) is computed <i>before</i> the incomplete rows are dropped, as the question's order requires. "
         "If you drop first, the mean changes. State the order you used."),
    CODE("m2_q1_pandas_basic.py"),
    OUT("m2_q1_pandas_basic.out.txt"),
]

c2_prompt = [
    P("(FAT high-frequency question 1) Explain the split-apply-combine strategy in pandas. Write code that uses `groupby` with "
      "multiple aggregation functions. Also explain the different kinds of merge on two related tables (customers and orders)."),
]
c2_answer = [
    FLOW(["Split: group rows by key(s)", "Apply: run sum / mean / count on each group", "Combine: results form one table"],
         "Split-apply-combine."),
    H3("Concept"),
    P("`groupby` <b>splits</b> a DataFrame into groups that share the same key, <b>applies</b> a function to every group independently, "
      "and <b>combines</b> the per-group results into a new Series or DataFrame. It replaces explicit loops and is the pandas equivalent of SQL `GROUP BY`."),
    B(["`agg` reduces each group to one row per aggregation (named aggregation `total=('sales','sum')` gives readable column names).",
       "`transform` returns a result the same length as the input (e.g. each row's share of its group total).",
       "`apply` runs any function on each group and is the most flexible but slowest.",
       "`reset_index()` turns the group keys back into ordinary columns."]),
    H3("Merge types"),
    T(["how=", "Rows kept", "Rows in the example output"], [
        ["`inner`", "keys present in both tables", "4 (customer 4 has no orders; order 105's customer 9 does not exist)"],
        ["`left`", "all customers, NaN where no order", "5 (customer 4 appears with NaN)"],
        ["`right`", "all orders, NaN where no customer", "5"],
        ["`outer`", "union of keys", "6"]], [0.14, 0.4, 0.46]),
    P("`concat` does not match on keys: `axis=0` stacks rows, `axis=1` places frames side by side by index alignment."),
    CODE("m2_q2_pandas_merge.py"),
    OUT("m2_q2_pandas_merge.out.txt"),
]

c3_prompt = [
    P("(Lab experiment 3, FAT high-frequency question 8) Using NumPy create a 2-D array of shape (3, 4) with random integers between 0 and 10. "
      "Calculate the mean and standard deviation, slice the first two rows and last two columns, reshape to (4, 3) and multiply "
      "element-wise with another array of the same shape. State the broadcasting rules and show one example that fails."),
]
c3_answer = [
    H3("Broadcasting rules"),
    N(["Write the two shapes aligned on the <b>right</b>; a shorter shape is padded with 1s on the left.",
       "For each aligned pair of dimensions the sizes must be <b>equal, or one of them must be 1</b>.",
       "A dimension of size 1 is virtually stretched to match the other (no data is copied).",
       "If any pair fails, NumPy raises `ValueError: operands could not be broadcast together`."]),
    T(["Shapes", "Aligned", "Result"], [
        ["(3,4) + (4,)", "(3,4) vs (1,4)", "(3,4) valid: the row is added to every row"],
        ["(3,4) + (3,1)", "(3,4) vs (3,1)", "(3,4) valid: the column is added to every column"],
        ["(3,1) + (1,4)", "(3,1) vs (1,4)", "(3,4) valid: outer-sum pattern"],
        ["(3,4) + (3,)", "(3,4) vs (1,3)", "error: 4 vs 3 differ and neither is 1"]], [0.25, 0.3, 0.45]),
    P("Why it matters: broadcasting removes Python loops and extra copies; e.g. column standardisation is `(x - x.mean(axis=0)) / x.std(axis=0)`. "
      "`axis=0` runs down the rows (one result per column), `axis=1` runs across the columns (one result per row)."),
    CODE("m2_q3_numpy.py"),
    OUT("m2_q3_numpy.out.txt"),
    NOTE("The random numbers depend on the seed and NumPy version, so yours may differ. The shapes and the error message are what to remember."),
]

c4_prompt = [
    P("(FAT high-frequency question 2, Lab experiment 5) Compare Beautiful Soup and Scrapy. Explain why Scrapy's Twisted event loop "
      "gives higher throughput. Scrape a page and store the result as CSV or JSON."),
]
c4_answer = [
    T(["Feature", "Beautiful Soup (with requests)", "Scrapy"], [
        ["What it is", "HTML/XML parsing library; you fetch pages yourself", "complete crawling framework"],
        ["Execution model", "synchronous: one request at a time unless you add threads", "asynchronous, event-driven (Twisted)"],
        ["Concurrency", "single-threaded by default", "many concurrent non-blocking requests (`CONCURRENT_REQUESTS`)"],
        ["Pipelines / export", "write your own code", "Item Pipelines, Feed Exporters (JSON, CSV, XML)"],
        ["Politeness", "manual `time.sleep()`", "`DOWNLOAD_DELAY`, AutoThrottle, `ROBOTSTXT_OBEY`"],
        ["Best for", "small, one-off pages and quick scripts", "large, repeatable, multi-page crawls"]], [0.18, 0.41, 0.41]),
    H3("Why the Twisted event loop is faster"),
    P("A blocking scraper spends most of its time waiting for the network, with the CPU idle. Twisted runs an event loop: when a request "
      "is sent, control returns immediately and the loop services other requests; a callback fires when the response arrives. "
      "One thread therefore keeps dozens of downloads in flight, so total time is close to the slowest request rather than the sum of all of them."),
    H3("Scrapy components"),
    P("Spider (parsing rules) -> Engine -> Scheduler (queue of requests) -> Downloader (fetch, via middlewares) -> Spider callback "
      "yields items -> Item Pipeline (clean, validate, store)."),
    CODE("m2_q4_scrape_bs4.py"),
    OUT("m2_q4_scrape_bs4.out.txt"),
    CODE("m2_q4_scrape_scrapy.py"),
    OUT("m2_q4_scrape_scrapy.out.txt"),
    NOTE("Both scripts read a local HTML page (the Scrapy one through a `file://` URL), so no website is contacted. For a real site, use its URL and respect `robots.txt`."),
]

c5_prompt = [
    P("(Lab experiments 6 to 10) Compare Matplotlib, Seaborn, Bokeh, Plotly and Folium and say when you would use each. Write code for: "
      "an interactive Plotly bar chart of city populations; a Plotly scatter plot of house size against price; a Bokeh line plot of "
      "a week's temperatures; a Bokeh bar chart of product sales; a Bokeh scatter plot of Iris petal length against petal width."),
]
c5_answer = [
    T(["Library", "Output", "Strength", "Typical call"], [
        ["Matplotlib", "static (PNG, PDF, SVG)", "full control; base for others", "`plt.plot(x, y)`"],
        ["Seaborn", "static", "statistical plots on DataFrames, good defaults", "`sns.histplot(df, x='age')`"],
        ["Bokeh", "interactive HTML (BokehJS), servers", "linked brushing, widgets, streaming", "`figure(); p.line(...)`; `HoverTool`"],
        ["Plotly", "interactive HTML (Plotly.js), Dash apps", "quickest interactive charts with `plotly.express`", "`px.bar(df, x=..., y=...)`"],
        ["Folium", "interactive Leaflet map in HTML", "markers, popups, choropleths on real maps", "`folium.Map(location=[lat, lon])`"]],
      [0.14, 0.24, 0.34, 0.28]),
    P("Choice guide: exploring a DataFrame -> Seaborn; report figure -> Matplotlib; interactive dashboard -> Plotly (Dash) or Bokeh server; geographic data -> Folium."),
    CODE("m2_q5_viz.py"),
    OUT("m2_q5_viz.out.txt"),
    NOTE("The script writes six HTML files; open them in a browser to hover, zoom and pan. City populations are illustrative numbers. "
         "`trendline='ols'` in Plotly needs the `statsmodels` package."),
]

c6_prompt = [
    P("(Lab experiments 4, 11 and 12) For a table with Feature1, Feature2 and Target: create the log of Feature1, bin Feature2 into low, "
      "medium and high, and compute the correlation matrix. Then perform K-means (k = 3) on the Iris data and visualise the clusters, "
      "and perform PCA to two components. Explain the steps and interpret the results. State the role of the main modelling libraries."),
]
c6_answer = [
    H3("K-means and PCA in brief"),
    N(["<b>K-means</b>: choose k, place k centroids, assign every point to its nearest centroid, move each centroid to the mean of its points, "
       "repeat until assignments stop changing. Choose k with the elbow plot of inertia (within-cluster sum of squares).",
       "<b>PCA</b>: standardise features, find orthogonal directions of maximum variance (eigenvectors of the covariance matrix, computed by SVD), "
       "project the data on the first components. `explained_variance_ratio_` says how much information each component keeps."]),
    H3("Reading the results below"),
    B(["Cluster sizes 62 / 50 / 38. Cluster 1 holds exactly the 50 setosa flowers. Versicolor and virginica overlap: cluster 0 has 48 versicolor + 14 virginica, "
       "cluster 2 has 2 versicolor + 36 virginica. K-means finds structure without labels, but it cannot separate overlapping species perfectly.",
       "PCA: PC1 explains 73.0% and PC2 22.9% of the variance, together 95.8%, so two components preserve almost all the information. "
       "PC1 is a \"size\" axis: petal length, petal width and sepal length load positively.",
       "The correlation matrix of random data is near zero everywhere, except `log_F1` with `Feature1` (0.90), because one is a transform of the other."]),
    CODE("m2_q6_ml.py"),
    OUT("m2_q6_ml.out.txt"),
    IMG("kmeans_pca.png", 15.5, "Left: Iris projected on the first two principal components, coloured by K-means cluster. Right: elbow plot."),
    NOTE("PCA used standardised features, K-means used the raw measurements (all in cm), so the two views are not identical. "
         "Always scale before PCA when the units differ."),
]

longs = [
    LONG("Data manipulation and cleaning with pandas", 10, c1_prompt, c1_answer,
         "concepts 3, correct operations 4, missing-value handling and scaling 2, output 1."),
    LONG("Split-apply-combine and merging DataFrames", 10, c2_prompt, c2_answer,
         "definition and diagram 2, groupby/agg code 3, merge types 3, concat vs merge 2."),
    LONG("NumPy arrays and broadcasting", 10, c3_prompt, c3_answer,
         "array operations 4, broadcasting rules 3, failing example 2, vectorisation benefit 1."),
    LONG("Beautiful Soup versus Scrapy", 10, c4_prompt, c4_answer,
         "comparison table 4, event-loop explanation 3, working code 2, ethics 1."),
    LONG("Python visualisation libraries", 10, c5_prompt, c5_answer,
         "comparison 3, five working charts 5, choice guide 2."),
    LONG("EDA, K-means, PCA and the modelling libraries", 10, c6_prompt, c6_answer,
         "EDA steps 2, K-means 3, PCA 3, interpretation 2."),
]

MODULE_2 = MODULE(
    2, "Python libraries for data science", "9 hours",
    "Pandas: Series, DataFrame, missing values, built-in functions, data operations, filtering, extraction, text data, merging; data mining with "
    "Scrapy and Beautiful Soup; processing and modelling with NumPy, SciPy, Pandas, Keras, scikit-learn, PyTorch, TensorFlow, XGBoost; "
    "visualisation with Matplotlib, Seaborn, Bokeh, Plotly, Folium.",
    [P("Labs 1 to 12 in your list of experiments belong to this module; the long questions below follow them. Questions marked FAT in the "
       "text come from the high-frequency list in your FAT notes.")],
    mcqs, shorts, longs,
    exam_notes=[TIP("Always end a pandas answer with a small output table. Examiners compare it with what the code should produce, "
                    "and it also proves you know the shape of the result.")],
)
