"""Cheat sheet, revision facts, index of tricky questions, and the verification appendix."""
from reportlab.platypus import PageBreak, Paragraph

from dsl import *
from render import S, Heading, fmt, render_blocks

FACTS = [
    ("Python", [
        "`list.append` and `pop()` are O(1); `insert`, `pop(0)`, `in` are O(n). Use `deque.popleft()` for queues.",
        "Dict and set lookups are O(1) on average; keys and members must be hashable (tuples yes, lists no).",
        "A tuple is immutable, but it may hold a mutable list; `t[0] += [x]` raises `TypeError` after mutating the list.",
        "`list.sort()` returns `None`; `sorted()` returns a new list. `[[0]*2]*2` repeats one inner list.",
        "Default argument values are created once; a mutable default is shared between calls.",
        "`finally` always runs; `else` runs when no exception occurred; put specific `except` clauses first.",
        "`self.__x` is stored as `_Class__x`; MRO for `class D(B, C)` is D, B, C, A.",
        "`heapq` is a min-heap; push negated priorities for a max-heap; add a counter to break ties.",
        "GET is safe and idempotent; POST creates; retry 429 (after Retry-After) and 5xx, not 404; always set `timeout=`.",
        "`open(..., 'w')` truncates, `'a'` appends, `'x'` fails if the file exists; JSON turns tuples into lists and int keys into strings.",
        "Lemmatization needs the part of speech (`better` -> `good` only with `pos='a'`); stemming can give non-words.",
    ]),
    ("pandas, NumPy and machine learning", [
        "`loc` slices by label and includes the end; `iloc` by position and excludes the end.",
        "Combine masks with `&`, `|` and parentheses; assign through one `df.loc[mask, col] = v`.",
        "Series arithmetic aligns on index labels; missing labels give NaN.",
        "A many-to-many merge multiplies rows; `validate=` and `indicator=True` help. `agg` reduces groups, `transform` keeps the length.",
        "NumPy: basic slices are views, fancy and boolean indexing copy; `*` is element-wise, `@` is the matrix product; broadcasting right-aligns shapes (equal or 1).",
        "PCA: centre (and usually scale), covariance, eigen-decomposition, sort, project. Eigenvalue = variance on that PC; ratios sum to 1; signs are arbitrary.",
        "K-means finds a local optimum (use `n_init`); scale first; choose k with elbow or silhouette.",
        "Fit scalers, selectors and PCA on training data only (use a Pipeline); otherwise results are over-optimistic.",
        "Accuracy misleads on imbalanced data: use precision, recall, F1; recall = TP/(TP+FN).",
        "PyTorch: `zero_grad` each step, int64 class labels; gradient step is w = w - lr x gradient. Early stopping needs a validation set, not the test set.",
    ]),
    ("Scala and Spark", [
        "`val` fixed reference, `def` evaluated at every use, `lazy val` once at first use; by-name `=> T` re-evaluates at each use.",
        "`foldLeft` and `foldRight` differ for non-associative operations (subtraction): -10 versus -2 for 1 to 4.",
        "`::` is right-associative and prepends in O(1); `List(i)` is O(n); `Array(1,2) == Array(1,2)` is false (use `sameElements`); `'5'.toInt` is 53.",
        "Case class = fields + `apply` + `unapply` + `equals`/`hashCode`/`toString` + `copy` (shallow).",
        "Companion object: same name and file, reads private members, `apply` removes `new`.",
        "Trait linearization is right to left: `D extends B with C` gives D, C, B, A; the order of `with` changes behaviour.",
        "An overridden `val` is `null` (or 0) inside the superclass constructor; use a `def` or `lazy val`.",
        "`Try` captures non-fatal exceptions; `NonFatal` excludes fatal ones; `.get` on a `Failure` re-throws; `Either` carries a typed error.",
        "Spark: transformations are lazy, actions run jobs; wide transformations shuffle and start a new stage; each action recomputes the lineage unless cached.",
        "`reduceByKey` combines before the shuffle; `groupByKey` ships every value. `collect()` copies everything to the driver.",
        "Driver variables are not updated from tasks; use accumulators (counters) and broadcast variables (read-only lookups).",
        "Catalyst: analysis, logical optimisation, physical planning, code generation. DataFrame shuffles use 200 partitions by default.",
    ]),
]


def back(mods, code_dir, out_dir):
    fl = [PageBreak(), Heading("Cheat sheet and last-minute revision", S["h1"], 0)]
    blocks = [
        H3("Costs in Python"),
        T(["Structure", "Index / key", "Search / membership", "Add / remove"], [
            ["list", "O(1)", "O(n)", "end O(1), front/middle O(n)"], ["tuple", "O(1)", "O(n)", "immutable"], ["dict", "O(1) avg", "O(1) avg (by key)", "O(1) avg"],
            ["set", "-", "O(1) avg", "O(1) avg"], ["deque", "ends O(1)", "O(n)", "both ends O(1)"], ["heapq", "peek O(1)", "O(n)", "push/pop O(log n)"]], [0.18, 0.2, 0.27, 0.35]),
        H3("Python and Scala side by side"),
        T(["Idea", "Python", "Scala"], [
            ["constant / variable", "`x = 5` (no constants)", "`val x = 5` / `var x = 5`"], ["function", "`def f(a, b): return a + b`", "`def f(a: Int, b: Int) = a + b`"],
            ["lambda", "`lambda x: x * 2`", "`(x: Int) => x * 2` or `_ * 2`"], ["list index", "`a[0]`", "`a(0)`"], ["map / filter", "`[f(x) for x in xs if p(x)]`", "`xs.filter(p).map(f)`"],
            ["f-string", "`f'{x:.2f}'`", "`f\"$x%.2f\"`"], ["class", "`class A(B): def __init__(self, x): ...`", "`class A(val x: Int) extends B`"], ["no value", "`None`", "`None` (inside `Option`)"],
            ["exceptions", "`try / except / finally`", "`try / catch { case ... } / finally`, `Try`"], ["dictionary", "`{'a': 1}`", "`Map(\"a\" -> 1)`"], ["equality", "`==` value, `is` identity", "`==` value, `eq` identity"]], [0.2, 0.4, 0.4]),
        H3("Formulas"),
        T(["Topic", "Formula"], [
            ["Z-score, min-max", "z = (x - mean) / std;   x' = (x - min) / (max - min)"], ["Covariance (sample)", "C = XcT Xc / (n - 1)"],
            ["2 x 2 eigenvalues", "lambda^2 - trace lambda + det = 0"], ["PCA explained ratio, reconstruction error", "lambda_i / sum(lambda);   SSE = (n - 1) x sum of discarded lambda"],
            ["K-means inertia", "sum over clusters of sum ||x - centroid||^2"], ["Precision, recall, F1", "TP/(TP+FP);  TP/(TP+FN);  2PR/(P+R)"],
            ["Gradient descent", "w = w - lr x dL/dw;  MSE gradient dL/dw = mean(2 (pred - y) x)"], ["Dense layer parameters", "inputs x units + units"],
            ["TF-IDF", "tf x idf, idf = ln((1+N)/(1+df)) + 1 in scikit-learn"], ["Weighted score", "sum of weight x score"]], [0.3, 0.7]),
    ]
    fl += render_blocks(blocks, code_dir, out_dir)
    fl.append(Paragraph("One-line facts to revise", S["h3"]))
    for title, items in FACTS:
        fl.append(Paragraph(f"<b>{title}</b>", S["h4"]))
        fl += render_blocks([B(items)], code_dir, out_dir)

    # ---- index of tricky questions, generated from the content
    fl += [PageBreak(), Heading("Index of tricky questions", S["h1"], 0)]
    fl.append(Paragraph(fmt("Every question tagged tricky or predict-the-output, with its number. Use it as a final revision list."), S["body"]))
    for m in mods:
        rows = []
        for s in m["subs"]:
            for b in s["blocks"]:
                if b["t"] == "qa" and b.get("tag") and ("tricky" in b["tag"] or "predict" in b["tag"]):
                    q = b["q"].replace("`", "")
                    rows.append([b["label"], q if len(q) <= 150 else q[:147] + "..."])
        if rows:
            fl.append(Paragraph(f"Module {m['num']}: {m['title']}", S["h3"]))
            fl += render_blocks([T(["No.", "Question"], rows, [0.1, 0.9])], code_dir, out_dir)

    # ---- appendix
    fl += [PageBreak(), Heading("Appendix: how the demonstrations were produced", S["h1"], 0)]
    fl += render_blocks([
        T(["Programs (Question_Bank/code)", "Runtime", "Covers"], [
            ["n1_basics, n1_structures, n1_strings_exceptions, n1_oop, n1_queues", "Python 3.10", "sections 1.1 to 1.12"],
            ["n1_files_rest", "Python 3.10, requests; a local HTTP server on 127.0.0.1", "1.13, 1.14 (real HTTP status codes, no internet service)"],
            ["n1_nlp", "NLTK 3.10.4, scikit-learn", "1.15"], ["n1_chatterbot", "ChatterBot 1.2.15 with spaCy en_core_web_sm", "1.16"],
            ["n2_pandas_a, n2_pandas_b", "pandas 2.3.3", "2.1 to 2.6"], ["n2_numpy_scipy", "NumPy 1.26.4, SciPy 1.15.3", "2.8, 2.9"],
            ["n2_pca, n2_ml", "scikit-learn 1.7.2", "2.10 to 2.12"], ["n2_dl", "TensorFlow 2.21, Keras 3.12, PyTorch 2.14 (CPU), XGBoost 3.2", "2.13, 2.14"],
            ["n2_viz and the question-bank programs m2_q4, m2_q5", "Matplotlib, Seaborn, Plotly, Bokeh, Folium, Beautiful Soup, Scrapy", "2.7, 2.15"],
            ["n3_scala_traps, n3_oop_traps, m3_q1 to m3_q4", "Scala 2.13.12, Java 17, scala-cli", "3.1 to 3.13"],
            ["n4_try_breeze, m4_q1 to m4_q3", "Breeze 2.1.0, Saddle 4.0.0-M14, Spire 0.18.0", "4.1 to 4.3"], ["n4_spark_traps, m4_q4", "Spark 3.5.1, local mode", "4.4 to 4.9"],
            ["m5_decision_matrix", "Python 3.10", "5.3"]], [0.38, 0.38, 0.24]),
        H3("Not verified by running"),
        B(["Interactive charts (Plotly, Bokeh, Folium) were generated as HTML files but not opened in a browser.",
           "The Scala REPL was not recorded; the same expressions were run as compiled programs.",
           "Spark ran in local mode on one machine, not on a real cluster; cluster-manager behaviour and client/cluster deploy modes are described, not demonstrated.",
           "Section 6 is general; the syllabus gives Module 6 no topics.",
           "Timings (such as set versus list membership, deque versus list) were measured on one machine and will differ on yours."]),
        H3("Run it yourself"),
        SNIP("python run_and_capture.py n2_pca.py            # output goes to outputs/n2_pca.out.txt\n"
             "python run_and_capture.py n4_spark_traps.scala # needs scala-cli and Java 17; downloads Spark on first run\n"
             "python build_notes.py                          # rebuilds this PDF", lang="text"),
    ], code_dir, out_dir)
    return fl
