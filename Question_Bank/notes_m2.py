from dsl import *
from notes_util import between, pick

# =====================================================================================================
sub_2_1 = SUB("2.1", "Pandas: Series and DataFrame", [
    B(["<b>Series</b>: 1-D labelled array (values + index, one dtype). <b>DataFrame</b>: 2-D table of aligned Series (columns may have different dtypes). `df['a']` is a Series, `df[['a']]` is a DataFrame.",
       "Attributes: `shape`, `dtypes`, `columns`, `index`, `values`/`to_numpy()`, `info()`, `head()`. Creation: from dict, list of dicts, `read_csv`, NumPy array.",
       "<b>Arithmetic aligns on index labels</b>, not positions: labels present in only one operand give NaN."]),
    OUT("n2_pandas_a.out.txt", "Verified output", transform=pick("Series", "DataFrame basics")),
    QA("What is the result of `pd.Series([10,20,30], index=list('abc')) + pd.Series([1,2,3], index=list('bcd'))`?", [
        P("`a NaN, b 21, c 32, d NaN`. Addition aligns on labels; `a` and `d` exist in only one Series so they become NaN, and the dtype becomes float. `s1.add(s2, fill_value=0)` treats a missing label as 0.")], "tricky"),
    QA("Difference between a Series and a DataFrame; how do you get each from a DataFrame column?", [
        P("A Series is one labelled column of values with one dtype; a DataFrame is a table of several. `df['age']` returns a Series; `df[['age']]` (list inside the brackets) returns a one-column DataFrame.")], "3 marks"),
    QA("Why does an integer column turn into floats when a value is missing?", [
        P("NumPy integers cannot hold NaN, so pandas upcasts to `float64`. The nullable dtype `Int64` keeps integers and shows `<NA>`.")], "2 marks"),
])

sub_2_2 = SUB("2.2", "Selecting and filtering data", [
    T(["Tool", "Selects by", "End of slice", "Example"], [
        ["`df['col']`, `df[['a','b']]`", "column name", "-", "`df[['name','age']]`"],
        ["`df.loc[rows, cols]`", "<b>labels</b> or boolean mask", "<b>included</b>", "`df.loc[1:2, 'name']`"],
        ["`df.iloc[rows, cols]`", "<b>integer positions</b>", "<b>excluded</b>", "`df.iloc[1:2, 0]`"],
        ["boolean mask", "condition on values", "-", "`df[(df.age > 25) & (df.city == 'Delhi')]`"],
        ["`isin`, `between`, `query`", "membership, range, text expression", "-", "`df.query('age > 30 and city == \"Delhi\"')`"]], [0.28, 0.27, 0.15, 0.3]),
    B(["Combine masks with `&`, `|`, `~` and <b>parentheses</b> around each comparison (`and`/`or` raise `ValueError: truth value of a Series is ambiguous`).",
       "To change values use one `df.loc[mask, 'col'] = value`. Chained indexing `df[mask]['col'] = value` may write to a temporary copy."]),
    OUT("n2_pandas_a.out.txt", "Verified output", transform=pick("selecting", "chained")),
    QA("For the default index, how many rows do `df.loc[1:3]` and `df.iloc[1:3]` return?", [P("3 and 2. `loc` includes the end label; `iloc` excludes the end position (the output shows `loc[1:2]` gives two names, `iloc[1:2]` one).")], "tricky"),
    QA("Why does `df[df.age > 25 and df.city == 'Delhi']` fail, and what is the fix?", [
        P("`and` needs a single truth value, but a Series has many (`ValueError: The truth value of a Series is ambiguous`). Use `&` with parentheses: `df[(df.age > 25) & (df.city == 'Delhi')]`.")], "tricky"),
    QA("`d2[d2.age > 30]['score'] = 0` leaves the data unchanged and warns. Why? How do you do it correctly?", [
        P("`d2[mask]` creates a new DataFrame (a copy); the second `['score'] = 0` modifies that temporary object, so the original is untouched (`SettingWithCopyWarning`). "
          "Use one call on the original: `d2.loc[d2.age > 30, 'score'] = 0` (output: changed? True).")], "tricky"),
    QA("Write the pandas code to select Name and Age, filter Age > 25, add a Country column and sort by Age descending.", [
        SNIP("df[['Name', 'Age']]\ndf[df['Age'] > 25]\ndf['Country'] = 'India'\ndf.sort_values('Age', ascending=False)", caption="Lab 1; run in the question bank, M2-C1")], "3 marks"),
])

sub_2_3 = SUB("2.3", "Handling missing values", [
    B(["Missing numbers are `NaN` (float) or `pd.NA`/`None`. `NaN == NaN` is False; test with `isna()`/`notna()`. Aggregations such as `mean`, `sum` <b>skip</b> NaN by default.",
       "Options: inspect `df.isna().sum()`; drop `dropna(subset=[...], thresh=k)`; fill `fillna(value | mean | median)`, `ffill()`, `bfill()`, `interpolate()`; flag with an indicator column when missingness is informative.",
       "Choose by column role: key fields missing -> drop the row; numeric -> mean or median (median if skewed); categorical -> mode or 'Unknown'; time series -> forward fill or interpolate.",
       "Do not fill using statistics from the test set (compute the mean on training data only)."]),
    OUT("n2_pandas_a.out.txt", "Verified output", transform=pick("missing values")),
    QA("Why does `np.nan == np.nan` return False and how do you test for missing values?", [P("By IEEE-754 rules NaN is not equal to anything, including itself. Use `pd.isna(x)`, `df.isna()`, `np.isnan(arr)`.")], "2 marks"),
    QA("Explain `dropna(subset=['score'])` and `dropna(thresh=4)`.", [
        P("`subset` drops rows that are missing a value in the listed columns only. `thresh=4` keeps rows having at least 4 non-missing values. In the sample, both keep 4 of 5 rows.")], "2 marks"),
    QA("Fill the missing Age with the mean, drop rows missing Name or City, convert Age to int, min-max scale it. In what order and why?", [
        P("Mean fill first (`df['Age'].fillna(df['Age'].mean())`), then `dropna(subset=['Name','City'])`, then `astype(int)` (impossible while NaN remains), then `(a - a.min()) / (a.max() - a.min())`. "
          "State the order: the mean is computed before rows are dropped, which changes the result if you swap the steps (question bank, M2-C1).")], "5 marks"),
    QA("Mean, median or forward fill: which for `[88.5, 72, NaN, 65.5, 91]`?", [
        P("Mean fill gives 79.25; `ffill` repeats 72.0 and suits ordered data such as a time series; `interpolate` gives 68.75, midway between the neighbours. Prefer the median when outliers skew the mean.")], "3 marks"),
])

sub_2_4 = SUB("2.4", "Built-in functions and data operations", [
    B(["Summaries: `describe()`, `value_counts()`, `nunique()`, `mean/median/std/min/max`, `corr()`. Ordering: `sort_values(by, ascending, na_position)`, `sort_index`.",
       "Changing: `assign`, `rename(columns=)`, `drop(columns=)`, `astype`, `pd.to_numeric(errors='coerce')`, `pd.to_datetime`, `pd.cut` (bins), `map` (dict/function per value), `apply` (function per row/column; `axis=1` is per row).",
       "<b>axis</b>: `axis=0` operates down the rows (one result per column); `axis=1` across the columns (one result per row).",
       "Prefer vectorised operations (`df['a'] * 2`) over `apply` or loops; they run in compiled code."]),
    OUT("n2_pandas_a.out.txt", "Verified output", transform=pick("add / drop")),
    QA("What does `df['city'].map({'Chennai': 'TN', 'Delhi': 'DL'})` give for an unmapped value?", [P("`NaN` (the output shows `nan` for Pune). Use `.fillna('Other')` or `df.replace`.")], "2 marks"),
    QA("What does `apply(..., axis=1)` mean and when should you avoid `apply`?", [P("It calls the function once per row (axis=0: once per column). It is a Python-level loop, so use vectorised column arithmetic, `np.where` or `.str` methods when possible.")], "3 marks"),
    QA("`pd.to_numeric(pd.Series(['1', 'x', '3']), errors='coerce')`?", [P("`[1.0, NaN, 3.0]`. Invalid entries become NaN instead of raising; then handle the NaN.")], "2 marks"),
    QA("What does `pd.cut(score, [0, 70, 85, 100], labels=['C','B','A'])` do with a mark of exactly 70?", [
        P("Bins are right-closed by default, `(0, 70]`, so 70 falls in `C`. Use `right=False` for left-closed bins. Missing values stay NaN (the output shows Meena with NaN).")], "tricky"),
])

sub_2_5 = SUB("2.5", "Working with text data", [
    B(["The `.str` accessor applies string methods to a whole column: `str.strip/lower/title/replace/contains/startswith/split/extract/len`. Missing values pass through as NaN/None instead of raising.",
       "`contains` treats the pattern as a regular expression unless `regex=False`; pass `na=False` when using the result as a filter mask.",
       "`str.extract(r'(\\d+)')` pulls capture groups into new columns; `str.split(expand=True)` returns a DataFrame."]),
    OUT("n2_pandas_b.out.txt", "Verified output", transform=pick("text data")),
    QA("Why does filtering with `df[df.name.str.contains('a')]` sometimes raise an error?", [
        P("If the column has missing values, `contains` returns NaN for them and a mask with NaN cannot index (`ValueError`). Use `na=False` (output: `[False, True, False, False]`).")], "tricky"),
    QA("Clean `'  asha NAIR '` to `'Asha Nair'` and validate an email ending in `.ac.in`.", [
        SNIP("s.str.strip().str.title()\ns.str.endswith('.ac.in') & s.str.contains('@')")], "2 marks"),
])

sub_2_6 = SUB("2.6", "Merging, joining, concatenating and grouping", [
    T(["how=", "Keeps", "Row counts in the sample (3 customers, 4 orders)"], [["inner", "keys in both", "3"], ["left", "all left rows", "4"], ["right", "all right rows", "4"], ["outer", "union of keys", "5"]], [0.15, 0.35, 0.5]),
    B(["`pd.merge(a, b, on='key', how=...)` is a database join; `a.join(b)` joins on the index; `pd.concat([a, b], axis=0|1)` stacks rows or columns without matching on keys.",
       "Duplicate keys on both sides multiply rows (many-to-many). Use `validate='one_to_one'`/`'one_to_many'` to catch it, `indicator=True` to see where rows came from, `suffixes=` for clashing column names, `left_on/right_on` for different key names.",
       "<b>groupby = split-apply-combine</b>: split rows by key, apply `sum/mean/count` (agg), `transform` (same length as input, e.g. share of total), or `apply` (any function), combine into a result.",
       "`reset_index()` turns group keys back into columns; `pivot_table(index, columns, values, aggfunc)` is a groupby arranged as a table."]),
    OUT("n2_pandas_b.out.txt", "Verified output", transform=pick("groupby", "merge", "concat")),
    QA("Explain split-apply-combine and show `agg` with named results.", [
        SNIP("sales.groupby(['region', 'cat']).agg(total=('amount', 'sum'), n=('amount', 'count'), avg=('amount', 'mean')).reset_index()"),
        P("Each region/category group is processed independently and the pieces are combined into one table (see the output). `groupby` is the pandas form of SQL `GROUP BY`.")], "5 marks"),
    QA("Difference between `agg` and `transform`.", [P("`agg` reduces each group to one row (3 regions give 3 rows); `transform` returns a value for every original row (6 rows), e.g. each sale's share of its region total `amount / g.transform('sum')`.")], "tricky"),
    QA("Two tables each have two rows with `k = 1`. How many rows does `merge(a, b, on='k')` return? How do you guard against this?", [
        P("4 (2 x 2 row explosion). `validate='one_to_one'` raises `MergeError: Merge keys are not unique...`. Check key uniqueness with `df['k'].is_unique` before merging.")], "tricky"),
    QA("Inner, left, right, outer: what are the row counts for customers {1,2,3} and orders for customers {1,1,2,9}?", [
        P("Inner 3 (orders for 1, 1, 2), left 4 (adds customer 3 with NaN order), right 4 (adds the order of customer 9 with NaN name), outer 5. `indicator=True` marks rows `both`, `left_only`, `right_only`.")], "3 marks"),
    QA("Why does merging on a text column '1' and a number column 1 fail?", [P("pandas raises `ValueError: You are trying to merge on object and int64 columns`. Cast one side (`astype(str)` or `astype(int)`) first.")], "2 marks"),
    QA("`merge`, `join`, `concat`: differences.", [
        T(["", "merge", "join", "concat"], [["matches on", "column values", "index (default)", "index/position; no key logic"], ["axis", "columns joined", "columns joined", "rows (0) or columns (1)"],
                                            ["duplicate index", "n/a", "n/a", "kept unless `ignore_index=True`"]], [0.2, 0.27, 0.27, 0.26])], "3 marks"),
])

sub_2_7 = SUB("2.7", "Data mining: Beautiful Soup and Scrapy", [
    B(["<b>Beautiful Soup</b> parses HTML/XML you already downloaded (`requests.get(url).text`): `soup.find_all('div', class_='book')`, `select_one('span.price')`, `.get_text(strip=True)`, `tag['href']`. Synchronous, simple, ideal for one page.",
       "<b>Scrapy</b> is a crawling framework: spiders (`parse` callbacks), Scrapy Engine, Scheduler, Downloader, Item Pipelines, Feed exports, middlewares. Built on Twisted so many requests are in flight at once; settings such as `ROBOTSTXT_OBEY`, `DOWNLOAD_DELAY`, `AUTOTHROTTLE_ENABLED`, `CONCURRENT_REQUESTS`.",
       "Selectors: CSS (`response.css('h2::text').get()`) and XPath (`response.xpath('//h2/text()')`). `.get()` returns the first match, `.getall()` all.",
       "Pages built by JavaScript are not in the downloaded HTML; use the site's API, or a browser-automation tool such as Selenium or Playwright.",
       "Responsible scraping: read `robots.txt` and the terms of service, throttle requests, identify your crawler, avoid personal data."]),
    CODE("m2_q4_scrape_bs4.py", "Beautiful Soup version (tested)"),
    OUT("m2_q4_scrape_bs4.out.txt", "Output"),
    CODE("m2_q4_scrape_scrapy.py", "Scrapy version (tested against the local file)"),
    OUT("m2_q4_scrape_scrapy.out.txt", "Output"),
    QA("Compare Beautiful Soup and Scrapy.", [
        T(["", "Beautiful Soup", "Scrapy"], [["Type", "parsing library", "full crawling framework"], ["Execution", "synchronous (with requests)", "asynchronous, event-driven (Twisted)"],
                                             ["Output/storage", "write your own CSV/JSON code", "Item Pipelines and Feed exports"], ["Politeness", "manual `time.sleep`", "`DOWNLOAD_DELAY`, AutoThrottle, robots.txt"],
                                             ["Use", "small, one-off extraction", "large repeatable crawls"]], [0.2, 0.4, 0.4])], "5 marks"),
    QA("Why is Scrapy faster than a loop of `requests.get` + Beautiful Soup?", [P("Most time is waiting on the network. Scrapy's Twisted event loop issues a new request while earlier ones wait, so total time approaches the slowest request rather than the sum; the blocking loop does one at a time.")], "3 marks"),
    QA("A page shows data in the browser but `soup.find_all` finds nothing. Why?", [P("The data is probably rendered by JavaScript after the page loads, so it is not in the HTML that `requests` downloaded. Look for a JSON API call in the browser's network tab, or use a headless browser.")], "tricky"),
    QA("What does a Scrapy item pipeline do?", [P("It receives every item the spider yields and can clean, validate, drop duplicates, and store it (database, file). Pipelines run in the order given by their numbers in `ITEM_PIPELINES`.")], "2 marks"),
])

sub_2_8 = SUB("2.8", "NumPy", [
    B(["`ndarray`: fixed dtype, contiguous memory, vectorised operations in compiled code. Attributes `shape`, `ndim`, `dtype`, `size`. Creation: `array`, `arange`, `linspace`, `zeros`, `ones`, `eye`, `random.default_rng(seed)`.",
       "<b>Broadcasting</b>: align shapes on the right (pad with 1s on the left); each pair of dimensions must be equal or 1; size-1 dimensions stretch. Otherwise `ValueError`.",
       "<b>Views and copies</b>: basic slices are <b>views</b> (share memory); fancy (integer list) and boolean indexing return <b>copies</b>; `.copy()` forces a copy.",
       "`*` is element-wise; `@` / `np.dot` is the matrix product. `sum/mean/max(axis=...)`: axis=0 collapses rows (per column), axis=1 collapses columns (per row).",
       "dtype traps: integer overflow wraps (`uint8` 250 + 10 = 4), `/` always gives float, `//` floors toward minus infinity, `np.array([1, 2.5, 'a'])` becomes strings, `mean` of an array with NaN is NaN (`nanmean`)."]),
    OUT("n2_numpy_scipy.out.txt", "Verified output", transform=pick("shape, axis", "view vs copy", "operators", "dtype", "where")),
    OUT("m2_q3_numpy.out.txt", "Broadcasting examples (question bank M2-C3)"),
    QA("State the broadcasting rules and decide whether (3,4)+(4,), (3,4)+(3,1), (3,4)+(3,) work.", [
        P("Right-align the shapes; each dimension pair must be equal or one of them 1. (3,4)+(4,): works, result (3,4). (3,4)+(3,1): works (3,4). (3,4)+(3,): aligned as (3,4) vs (1,3), 4 vs 3 differ and neither is 1, "
          "so `ValueError: operands could not be broadcast together with shapes (3,4) (3,)`.")], "tricky"),
    QA("`v = a[0, :2]; v[0] = 99`. Does `a` change? What about `c = a[[0, 1]]; c[0, 0] = -1`?", [
        P("Yes for the slice (a view: `np.shares_memory` True). No for the integer-list index (a copy). Boolean masks also return copies. Use `.copy()` when you want independence.")], "tricky"),
    QA("Difference between `x * y`, `x @ y` and `np.dot(x, y)` for 2 x 2 arrays.", [
        P("`x * y` multiplies element by element ([[10,40],[90,160]] in the output); `x @ y` and `np.dot` give the matrix product ([[70,100],[150,220]]).")], "2 marks"),
    QA("Why does `np.array([250], dtype=np.uint8) + 10` equal 4?", [P("`uint8` holds 0..255; 260 wraps around modulo 256 without an error. Choose a wider dtype when values may exceed the range.")], "tricky"),
    QA("What do `axis=0` and `axis=1` mean in `a.sum(axis=...)` for a 3 x 4 array?", [P("axis=0 collapses the rows and returns 4 column sums; axis=1 collapses the columns and returns 3 row sums (`keepdims=True` keeps a (3,1) shape for later broadcasting).")], "2 marks"),
    QA("Why is NumPy faster than a Python list for numeric work?", [P("Contiguous typed memory, no per-element object overhead, and loops run in C (vectorisation). Measured earlier: 2.5 ms against 96 ms for doubling one million integers.")], "3 marks"),
    QA("How do you make random results repeatable?", [P("Use a seeded generator: `rng = np.random.default_rng(0)`. The same seed gives the same numbers (output: `[8, 6, 5]` twice).")], "1 mark"),
])

sub_2_9 = SUB("2.9", "SciPy", [
    B(["SciPy builds on NumPy with scientific algorithms: `scipy.stats` (distributions, t-tests, correlations), `optimize` (minimise, curve fit, root finding), `integrate` (quad, ODEs), `linalg`, `sparse` (matrices that mostly hold zeros), `interpolate`, `signal`, `spatial`.",
       "Hypothesis test pattern: state H0, run the test (`ttest_ind`), compare the p-value with the significance level (0.05): p < 0.05 rejects H0."]),
    OUT("n2_numpy_scipy.out.txt", "Verified output", transform=pick("linear algebra", "SciPy")),
    QA("What does a p-value of 0.0029 mean in the t-test output?", [
        P("If the two groups had the same mean, a difference at least this large would appear in about 0.29% of samples. Since 0.0029 < 0.05 we reject the null hypothesis of equal means. It is not the probability that H0 is true.")], "3 marks"),
    QA("When do you use `scipy.sparse`?", [P("For matrices with mostly zeros (text vectors, graphs): CSR/CSC formats store only non-zero entries, saving memory and time. scikit-learn's `CountVectorizer` returns such a matrix.")], "2 marks"),
    QA("NumPy versus SciPy.", [P("NumPy supplies arrays and basic maths; SciPy adds higher-level scientific routines (optimisation, statistics, integration, sparse algebra) built on those arrays.")], "2 marks"),
])


# =====================================================================================================
sub_2_10 = SUB("2.10", "Machine-learning workflow with scikit-learn", [
    B(["Estimator API: `fit(X, y)` learns from data, `predict(X)` makes predictions, `transform(X)` converts data (scalers, PCA). `fit_transform` = fit then transform. <b>Learn parameters on the training data only</b>.",
       "Workflow: split (`train_test_split`, `stratify=y` keeps class ratios) > preprocess > fit > evaluate on unseen data > tune with cross-validation (`cross_val_score`).",
       "Types: supervised <i>classification</i> (labels), supervised <i>regression</i> (numbers), unsupervised <i>clustering</i> and <i>dimensionality reduction</i>.",
       "<b>Pipeline</b> chains steps so every fold re-fits them correctly: `Pipeline([('scale', StandardScaler()), ('clf', LogisticRegression())])`.",
       "<b>Overfitting</b>: very high training score, much lower test score (memorising noise). <b>Underfitting</b>: both scores low. Remedies: more data, simpler model, regularisation, early stopping, cross-validation."]),
    OUT("n2_ml.out.txt", "Verified output", transform=pick("CLASSIFICATION METRICS", "DATA LEAKAGE", "OVERFITTING", "PCA inside")),
    T(["Metric", "Formula", "Question it answers"], [
        ["Accuracy", "(TP + TN) / all", "how often is the model right?"], ["Precision", "TP / (TP + FP)", "of predicted positives, how many are real?"],
        ["Recall (sensitivity)", "TP / (TP + FN)", "of real positives, how many did we find?"], ["F1", "2PR / (P + R)", "balance of precision and recall"],
        ["MSE / RMSE / R-squared", "mean (y - p)^2 / its root / 1 - SSE/SST", "regression error and explained variance"]], [0.22, 0.33, 0.45]),
    QA("From TP=2, FN=2, FP=1, TN=5 compute accuracy, precision, recall and F1.", [
        P("Accuracy = (2+5)/10 = 0.70; precision = 2/(2+1) = 0.667; recall = 2/(2+2) = 0.50; F1 = 2(0.667)(0.5)/(0.667+0.5) = 0.571. scikit-learn agrees (output). The confusion matrix has true classes as rows and predicted classes as columns: [[5, 1], [2, 2]].")], "5 marks"),
    QA("A model predicts 'no fraud' for everyone on a data set with 5% fraud. What are its accuracy and recall?", [
        P("Accuracy 0.95 but recall 0.0: it finds none of the fraud. This is the accuracy paradox; use precision, recall, F1 or ROC-AUC on imbalanced data.")], "tricky"),
    QA("What is data leakage? Give an example the output demonstrates.", [
        P("Information from the test data (or the labels) influences training. With pure noise (no real signal), selecting the best 20 of 2,000 features on <i>all</i> the data and then cross-validating gives accuracy 0.78, "
          "while doing the selection inside a `Pipeline` gives the honest 0.59. Scaling or imputing before the split leaks in the same way, more mildly.")], "tricky"),
    QA("Why `scaler.fit_transform(X_train)` but `scaler.transform(X_test)`?", [
        P("The test set must be treated as unseen: the mean and standard deviation come from the training data only. Calling `fit` on the test set would use its own statistics and leak information.")], "3 marks"),
    QA("Explain overfitting using the decision-tree output.", [
        P("`max_depth=None` gives training accuracy 1.00 with 53 leaves but test accuracy 0.66, below the depth-3 tree's 0.70. The gap between train and test accuracy is the symptom. Limit depth, prune, add data or use cross-validation to choose complexity.")], "3 marks"),
    QA("What does `stratify=y` do in `train_test_split`?", [P("It keeps the class proportions equal in train and test (positives 0.628 / 0.626 against 0.627 overall in the earlier run), which matters for imbalanced classes.")], "2 marks"),
    QA("Why use a Pipeline with PCA or scaling when cross-validating?", [P("Each fold must fit the scaler or PCA on its own training part. Fitting once on all the data lets the validation folds influence the transformation (leakage).")], "3 marks"),
])

# =====================================================================================================
sub_2_11 = SUB("2.11", "PCA in depth (tricky topic)", [
    P("<b>Goal.</b> Principal Component Analysis rotates the data onto new orthogonal axes (principal components, PCs) ordered by how much variance they capture, so that a few PCs summarise most of the information. "
      "It is unsupervised (ignores the target), linear, and removes correlation between features."),
    H3("Algorithm"),
    T(["Step", "What you do", "Formula"], [
        ["1 Centre", "subtract each column's mean (standardise too if units differ)", "Xc = X - mean"],
        ["2 Covariance", "variances on the diagonal, covariances elsewhere", "C = XcT Xc / (n - 1)"],
        ["3 Eigen-decompose", "eigenvalues = variance along each PC, eigenvectors = PC directions (unit length, orthogonal)", "C v = lambda v;  det(C - lambda I) = 0"],
        ["4 Sort and choose k", "largest eigenvalues first; keep k PCs", "ratio_i = lambda_i / sum(lambda)"],
        ["5 Project", "scores = coordinates of the data on the kept PCs", "Z = Xc Wk   (Wk = first k eigenvectors)"],
        ["6 Reconstruct (optional)", "map back; the error equals the discarded variance", "Xhat = Z WkT + mean"]], [0.19, 0.5, 0.31]),
    KEY("For a 2 x 2 matrix: lambda^2 - trace(C) lambda + det(C) = 0. Then the eigenvector of lambda comes from the first row of (C - lambda I)v = 0: v is proportional to (c12, lambda - c11); divide by its length."),
    H3("Worked example: five points (2,1), (3,5), (4,3), (5,6), (6,5)"),
    OUT("n2_pca.out.txt", "Verified output (every number below is from this run)", transform=pick("STEP 1", "STEP 2", "STEP 3", "STEP 4")),
    OUT("n2_pca.out.txt", "Verified output (continued)", transform=pick("STEP 5", "STEP 6", "CHECK")),
    IMG("notes_pca.png", 17, "Left: data with the two principal axes (PC1 follows the long direction). Middle: scree plot and cumulative variance for Iris (standardised) with the 95% line. Right: the five scores on PC1 and PC2."),
    CODE("n2_pca.py", "Code (n2_pca.py): steps 1 to 6 and the checks", transform=between("STEP 1  mean and centering", "print(\"sklearn transform equals centered data")),
    H3("Scaling, variance and other traps"),
    OUT("n2_pca.out.txt", "Verified output", transform=pick("does scaling matter", "unit change", "high variance", "limits")),
    QA("What does PCA do, and what quantity does it maximise?", [
        P("It finds orthogonal directions that capture the maximum variance in turn: PC1 is the direction of greatest variance, PC2 the greatest remaining variance orthogonal to PC1, and so on. "
          "Equivalently it minimises the squared reconstruction error when data are projected on k components.")], "5 marks"),
    QA("List the steps of PCA and the role of the covariance matrix.", [
        P("Centre (and usually scale) > covariance matrix > eigenvalues and eigenvectors > sort > select k > project. The covariance matrix records how features vary and co-vary; its eigenvectors are the PC directions, its eigenvalues the variance along each.")], "5 marks"),
    QA("Compute the covariance matrix for the five points above.", [
        P("Mean (4, 4); centred points (-2,-3), (-1,1), (0,-1), (1,2), (2,1). Var x = (4+1+0+1+4)/4 = 2.5; var y = (9+1+1+4+1)/4 = 4; "
          "cov = (6 - 1 + 0 + 2 + 2)/4 = 2.25. So C = [[2.5, 2.25], [2.25, 4]]. Divide by n - 1 = 4 (sample covariance), as `np.cov` does.")], "tricky"),
    QA("Find the eigenvalues of C by hand and the percentage of variance on PC1.", [
        P("trace = 6.5, det = 2.5 x 4 - 2.25^2 = 4.9375. lambda^2 - 6.5 lambda + 4.9375 = 0 gives lambda = (6.5 +- sqrt(42.25 - 19.75))/2 = (6.5 +- 4.7434)/2 = 5.6217 and 0.8783. "
          "PC1 explains 5.6217 / 6.5 = 86.5% (the sum of eigenvalues equals the total variance, the trace).")], "tricky"),
    QA("Find the PC1 direction and the score of the first point.", [
        P("v is proportional to (c12, lambda - c11) = (2.25, 5.6217 - 2.5) = (2.25, 3.1217); its length is 3.8480, so v = (0.5847, 0.8112). First point centred is (-2, -3): "
          "score = -2(0.5847) - 3(0.8112) = -3.603, matching the output (-3.6031). PC2 is orthogonal: (-0.8112, 0.5847), eigenvalue 0.8783.")], "tricky"),
    QA("How much information is lost keeping only PC1 here?", [
        P("13.5% of the variance (0.8783 / 6.5). The squared reconstruction error summed over the points is 3.5132 = (n - 1) x discarded eigenvalue = 4 x 0.8783 (output, step 6).")], "tricky"),
    QA("Why must the data be centred? Why standardise?", [
        P("PCA describes variation <i>around the mean</i>; without centring, the first PC mostly points at the mean. Variance depends on units, so a feature in millimetres would dominate one in centimetres. "
          "In the output, changing height from cm to mm flips PC1 from (0.14, 0.99) to (1.00, 0.0085). Standardise (z-scores) when features have different units or scales; PCA then works on the correlation matrix.")], "tricky"),
    QA("Why does PCA on raw Iris give 92.5% for PC1 but 73.0% after standardising?", [
        P("Petal length has by far the largest variance (in cm), so raw PCA is dominated by it (PC1 loading 0.86). After z-scoring every feature has variance 1 and the structure shared by several features appears, "
          "giving [0.730, 0.229, 0.037, 0.005] and a different PC1 (0.52, -0.27, 0.58, 0.56). Two components then hold 95.8%.")], "tricky"),
    QA("How many components should you keep?", [
        P("Common rules: enough to reach a target of cumulative variance (e.g. 95%: `PCA(0.95)` picks 2 for standardised Iris); the elbow of the scree plot; Kaiser rule (eigenvalue > 1 on standardised data); or the number that gives the best "
          "cross-validated score of the downstream model.")], "3 marks"),
    QA("What are loadings and scores?", [
        P("Loadings (`components_`) are the weights of the original features in each PC: Iris PC1 = 0.52 sepal length - 0.27 sepal width + 0.58 petal length + 0.56 petal width, so PC1 is a 'size' axis. "
          "Scores (`transform`) are the coordinates of each observation on the PCs.")], "3 marks"),
    QA("Is a PC with high variance always useful for prediction?", [
        P("No. PCA ignores the target. In the demo a large-variance noise feature becomes PC1 and has correlation 0.004 with the label, while the low-variance PC2 (the real signal) has 0.79. Check downstream performance; supervised alternatives are LDA or feature selection.")], "tricky"),
    QA("The signs of components differ between my hand calculation and scikit-learn. Is that a bug?", [
        P("No. An eigenvector and its negative describe the same axis. Compare variances, ratios and absolute loadings, not signs (the SVD route in the output gave (0.81, -0.58) for PC2 where the hand value is (-0.81, 0.58)).")], "tricky"),
    QA("What is the maximum number of principal components?", [P("min(n_samples, n_features) (4 for a 4 x 10 matrix in the output); only n - 1 of them can have non-zero variance after centring.")], "2 marks"),
    QA("What is the relation between PCA and SVD?", [
        P("If Xc = U S VT, the rows of VT are the PCs and the eigenvalues are s^2 / (n - 1) (output: 5.6217 and 0.8783 again). scikit-learn uses SVD because it is numerically stabler than forming the covariance matrix.")], "3 marks"),
    QA("Name limitations of PCA.", [
        P("Linear only (use kernel PCA, t-SNE or UMAP for curved structure); sensitive to outliers (one point at (30, 30) rotated PC1 from (1, 0) to (0.80, 0.61) in the demo); components are hard to interpret; "
          "needs numeric features (encode categoricals first); variance is not the same as importance.")], "3 marks"),
    QA("Where must PCA be fitted when you also have a test set?", [P("On the training data only, then `transform` the test data: put the scaler and PCA inside a `Pipeline` (see 2.10).")], "2 marks"),
    QA("PCA versus feature selection versus LDA.", [
        T(["", "PCA", "Feature selection", "LDA"], [["Supervised?", "no", "usually yes", "yes"], ["Output", "new features (linear mixes)", "subset of original features", "new axes that separate classes"],
                                                    ["Goal", "maximise variance", "keep informative features", "maximise class separation"]], [0.2, 0.27, 0.27, 0.26])], "3 marks"),
])

# =====================================================================================================
sub_2_12 = SUB("2.12", "K-means clustering in depth (tricky topic)", [
    B(["Unsupervised clustering into k groups. <b>Lloyd's algorithm</b>: (1) choose k initial centroids (k-means++ spreads them out); (2) assign every point to the nearest centroid; (3) move each centroid to the mean of its points; repeat 2 to 3 until assignments stop changing.",
       "Objective: minimise <b>inertia</b> (within-cluster sum of squared distances to the centroid). It never increases, so the algorithm converges, but only to a <b>local</b> optimum: run with several starts (`n_init`) and keep the best.",
       "Choosing k: elbow plot of inertia, silhouette score (-1 to 1, higher is better), or domain knowledge. Inertia always falls as k grows, so it cannot choose k alone.",
       "Assumes round, similar-sized clusters of similar density; sensitive to feature scale and outliers; needs numeric data. Cost about O(n x k x d) per iteration."]),
    OUT("n2_ml.out.txt", "Verified output", transform=pick("K-MEANS by hand", "K-means choices")),
    QA("Run one full K-means iteration for points (1,1), (1.5,2), (3,4), (5,7), (3.5,5), (4.5,5) with starting centroids (1,1) and (5,7).", [
        P("Assignments by distance: the first three points go to centroid 1, the last three to centroid 2 (point (3,4) is exactly 3.606 from both; ties go to the first centroid). New centroids are the member means: "
          "(1.833, 2.333) and (4.333, 5.667). A second assignment pass changes nothing, so the algorithm has converged; inertia = 10.667 (scikit-learn gives the same).")], "5 marks"),
    QA("Why can two runs of K-means give different answers?", [
        P("The result depends on the starting centroids and the algorithm finds only a local minimum. With one random start per seed the inertia was either 365.6 (the good solution) or between 2278 and 2284 (a poor local minimum); `n_init=10` keeps the best run (365.6). k-means++ initialisation reduces the problem.")], "tricky"),
    QA("How do you choose k? What do the printed inertia and silhouette show?", [
        P("Inertia drops sharply until k = 4 and flattens afterwards (366, then 327, 293): the elbow. Silhouette peaks at k = 4 (0.846). Both point to 4, the number of blobs generated.")], "3 marks"),
    QA("Why must features be scaled before K-means?", [
        P("It uses Euclidean distance, so a feature with large numbers dominates. Multiplying one coordinate by 1000 changed the clusters (agreement with the unscaled solution fell to 0.774 ARI); standardising restored 1.0.")], "tricky"),
    QA("K-means versus hierarchical clustering versus DBSCAN.", [
        T(["", "K-means", "Hierarchical", "DBSCAN"], [["k needed?", "yes", "cut the dendrogram", "no (eps, min_samples)"], ["Shapes", "round", "depends on linkage", "arbitrary, finds noise"],
                                                       ["Scales to big n", "well", "poorly", "moderately"]], [0.2, 0.27, 0.27, 0.26])], "3 marks"),
    QA("Is K-means classification? How do you evaluate clusters without labels?", [
        P("No, it is unsupervised: cluster numbers are arbitrary labels. Evaluate with inertia, silhouette, or (if true labels exist) adjusted Rand index or a cross-tab. In the Iris run cluster 1 held exactly the 50 setosa flowers while versicolor and virginica overlapped.")], "3 marks"),
])

# =====================================================================================================
sub_2_13 = SUB("2.13", "Deep learning frameworks: Keras, TensorFlow, PyTorch", [
    B(["A neural network is layers of weighted sums plus activation functions. <b>Training</b>: forward pass (predictions) > loss > <b>backpropagation</b> (gradients by the chain rule) > optimiser step `w = w - lr x gradient`.",
       "Vocabulary: <b>epoch</b> = one pass over all training data; <b>batch</b> = rows per update; <b>iteration</b> = one update (150 rows / batch 16 = 10 updates per epoch); <b>learning rate</b> = step size.",
       "Activations: ReLU `max(0, z)` (hidden layers), sigmoid (binary output), softmax (class probabilities that sum to 1), tanh. Losses: MSE (regression), cross-entropy (classification).",
       "Parameters of a dense layer = inputs x units + units (bias): 4 -> 8 gives 40; 8 -> 3 gives 27; total 67.",
       "<b>TensorFlow</b> (Google): tensors, automatic differentiation (`GradientTape`), graph compilation, deployment tools. <b>Keras</b>: high-level API (`Sequential`, `compile`, `fit`, `predict`); Keras 3 runs on TensorFlow, PyTorch or JAX. "
       "<b>PyTorch</b> (Meta): define-by-run tensors and `autograd`, explicit training loop, popular in research.",
       "Overfitting remedies: more data, dropout, weight decay (L2), early stopping, smaller network."]),
    OUT("n2_dl.out.txt", "Verified output (TensorFlow 2.21, Keras 3.12, PyTorch 2.14)", transform=pick("one gradient-descent", "activations", "Keras", "PyTorch", "TensorFlow tensors")),
    CODE("n2_dl.py", "Keras and PyTorch code (n2_dl.py)", transform=between("keras.utils.set_random_seed(0)", "print(f\"loss {first:.3f}")),
    QA("Do one gradient-descent step for y = w x + b with x = [1,2,3], y = [2,4,6], w = b = 0, learning rate 0.1 (MSE loss).", [
        P("Predictions are 0, so errors are -2, -4, -6 and loss = (4 + 16 + 36)/3 = 18.667. dL/dw = mean(2 x error x x) = (2/3)(-2 - 8 - 18) = -18.667; dL/db = (2/3)(-2 - 4 - 6) = -8. "
          "Update: w = 0 - 0.1(-18.667) = 1.867; b = 0 - 0.1(-8) = 0.8. PyTorch autograd and TensorFlow's tape return the same gradients (output).")], "tricky"),
    QA("PyTorch loss stays wrong / gradients look doubled. What is the usual cause?", [
        P("Gradients accumulate in `.grad` across `backward()` calls (6.0 instead of 3.0 in the output). Call `optimizer.zero_grad()` at the start of every iteration. The loop is: zero_grad, forward, loss, backward, step.")], "tricky"),
    QA("`CrossEntropyLoss` raises `expected target dtype to be Long or Byte, but got Int`. Why?", [
        P("Class labels must be 64-bit integers. NumPy/scikit-learn labels can be int32 (on Windows); convert with `torch.tensor(y, dtype=torch.long)` (this error occurred while preparing these notes).")], "tricky"),
    QA("Keras: how many parameters does `Dense(8)` after a 4-feature input have, and what is the output shape of a 3-class softmax head for 2 samples?", [
        P("4 x 8 + 8 = 40 parameters. The output shape is (2, 3): one probability per class per sample.")], "3 marks"),
    QA("Compare Keras, TensorFlow and PyTorch.", [
        T(["", "Keras", "TensorFlow", "PyTorch"], [["Level", "high-level API", "full framework", "full framework"], ["Style", "`compile` + `fit`", "tensors, tapes, graphs", "explicit loop, autograd"],
                                                    ["Strength", "fast prototyping", "deployment ecosystem", "research flexibility"]], [0.2, 0.27, 0.27, 0.26])], "3 marks"),
    QA("Explain epoch, batch and iteration; why use mini-batches?", [
        P("Mini-batches give frequent updates at moderate cost and fit in memory, with some noise that helps escape poor minima. 150 rows with batch 16 makes ceil(150/16) = 10 iterations per epoch.")], "3 marks"),
    QA("Why use softmax with cross-entropy for multi-class output?", [P("Softmax turns scores into probabilities that sum to 1 (softmax([1,2,3]) = [0.09, 0.245, 0.665]); cross-entropy penalises low probability on the true class.")], "2 marks"),
])

sub_2_14 = SUB("2.14", "XGBoost", [
    B(["<b>Gradient-boosted decision trees</b>: trees are added one at a time, each fitted to the errors (gradients of the loss) of the ensemble so far. Contrast <b>bagging</b> (random forest: independent trees averaged).",
       "Key hyperparameters: `n_estimators`, `learning_rate` (shrinkage), `max_depth`, `subsample`, `colsample_bytree`, regularisation `reg_lambda`, `reg_alpha`. Provides `feature_importances_`, handles missing values, strong on tabular data.",
       "<b>Early stopping</b> needs a separate validation set: using the test set to decide when to stop leaks information."]),
    OUT("n2_dl.out.txt", "Verified output (XGBoost 3.2)", transform=pick("XGBoost")),
    QA("Boosting versus bagging.", [P("Boosting builds trees sequentially, each correcting the previous ones (reduces bias, can overfit with too many trees). Bagging builds independent trees on bootstrap samples and averages them (reduces variance).")], "3 marks"),
    QA("Why can adding more trees hurt, and how does early stopping help?", [
        P("Training error keeps falling but validation error eventually rises (overfitting; test accuracy went 0.959 at 10 trees to 0.953 at 100). Early stopping stops when the validation loss has not improved for N rounds (best tree 51 of 500 here).")], "3 marks"),
    QA("Why is a small learning rate usually paired with more trees?", [P("Each tree contributes a smaller correction, so the model approaches the optimum more smoothly and generalises better, at the cost of more trees and time.")], "2 marks"),
])

# =====================================================================================================
sub_2_15 = SUB("2.15", "Data visualisation: Matplotlib, Seaborn, Bokeh, Plotly, Folium", [
    T(["Library", "Style", "Key objects / calls", "Best for"], [
        ["Matplotlib", "static, low-level", "`fig, ax = plt.subplots()`, `ax.plot/scatter/bar/hist`", "full control, publication figures"],
        ["Seaborn", "static, statistical, built on Matplotlib", "`histplot, boxplot, heatmap, pairplot, relplot`", "quick exploration of DataFrames"],
        ["Bokeh", "interactive (BokehJS), servers", "`figure()`, `ColumnDataSource`, `HoverTool`, `output_file`, `save`", "linked interactive plots, dashboards"],
        ["Plotly", "interactive (Plotly.js), Dash apps", "`plotly.express`: `px.bar/scatter/line`; `graph_objects`", "fast interactive charts, 3-D, maps"],
        ["Folium", "interactive maps (Leaflet)", "`folium.Map`, `Marker`, `Choropleth`, `.save('map.html')`", "geographic data"]], [0.13, 0.25, 0.35, 0.27]),
    B(["Matplotlib has two interfaces: the pyplot state machine (`plt.plot` draws on the current axes) and the explicit object-oriented one (`fig, ax = plt.subplots(); ax.plot(...)`). Use the object-oriented form for anything with several panels.",
       "Seaborn <b>axes-level</b> functions accept `ax=`; <b>figure-level</b> ones (`pairplot`, `relplot`, `catplot`) create their own figure.",
       "Choosing a chart: comparison across categories > bar; trend over time > line; relationship of two numbers > scatter; distribution > histogram or box plot; correlations > heatmap; geography > map. Label axes and give a title."]),
    OUT("n2_viz.out.txt", "Verified output"),
    IMG("notes_viz.png", 17, "Matplotlib scatter with the object-oriented API, Seaborn box plot (axes-level) and heatmap of correlations (Iris)."),
    CODE("m2_q5_viz.py", "Tested code for the lab charts (Plotly, Bokeh, Folium)", transform=between("---- Lab 6", "m.save(\"folium_map.html\")")),
    OUT("m2_q5_viz.out.txt", "Output (HTML files written)"),
    QA("Compare Matplotlib and Seaborn.", [P("Matplotlib is the foundation with full control over figures and axes. Seaborn sits on top, understands DataFrames, and gives statistical plots and good defaults in one call; you still customise with Matplotlib.")], "3 marks"),
    QA("What is the difference between `plt.plot(...)` and `ax.plot(...)`?", [P("`plt.plot` implicitly uses the 'current' axes (global state), which becomes confusing with several subplots. `ax.plot` names the axes object explicitly (`fig, ax = plt.subplots()`).")], "2 marks"),
    QA("Create an interactive bar chart of city populations in Plotly and a line plot of daily temperatures in Bokeh (lab experiments 6 and 8).", [
        P("See the tested code above: `px.bar(cities, x='city', y='population_m')` followed by `write_html`, and a Bokeh `figure(x_range=days)` with `line`, `scatter` and a `HoverTool`. Open the HTML files to hover and zoom.")], "5 marks"),
    QA("Which library would you choose for (a) a map with markers, (b) a seaborn-style correlation heatmap, (c) an interactive web dashboard?", [P("(a) Folium (or Plotly maps), (b) Seaborn `heatmap`, (c) Plotly with Dash or Bokeh server.")], "2 marks"),
    QA("What does `ColumnDataSource` do in Bokeh?", [P("It holds the columns shared by glyphs and tools, so several plots or a hover tool refer to the same data by column name and update together when the data change.")], "2 marks"),
])

NOTES_2 = NMODULE(
    2, "Python libraries for data science", "9 hours",
    "Pandas: Series, DataFrame, missing values, built-in functions, data operations, filtering, extraction, text data, merging; data mining: Scrapy, Beautiful Soup; data processing and modelling: NumPy, SciPy, Pandas, Keras, scikit-learn, PyTorch, TensorFlow, XGBoost; data visualisation: Matplotlib, Seaborn, Bokeh, Plotly, Folium.",
    [("Pandas: Series, DataFrame", "2.1"), ("Handling missing values", "2.3"), ("Built-in functions, data operations", "2.4"), ("Filtering data in DataFrame, data extraction", "2.2"),
     ("Working with text data", "2.5"), ("Merging DataFrames", "2.6"), ("Data mining: Scrapy, Beautiful Soup", "2.7"), ("NumPy", "2.8"), ("SciPy", "2.9"),
     ("scikit-learn (workflow, metrics, leakage); PCA; K-means", "2.10, 2.11, 2.12"), ("Keras, PyTorch, TensorFlow", "2.13"), ("XGBoost", "2.14"),
     ("Matplotlib, Seaborn, Bokeh, Plotly, Folium", "2.15")],
    [sub_2_1, sub_2_2, sub_2_3, sub_2_4, sub_2_5, sub_2_6, sub_2_7, sub_2_8, sub_2_9, sub_2_10, sub_2_11, sub_2_12, sub_2_13, sub_2_14, sub_2_15],
)
