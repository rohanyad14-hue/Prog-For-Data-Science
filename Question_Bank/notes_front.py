"""Cover page, how-to-use and the tricky-topic finder for the notes document."""
from reportlab.platypus import PageBreak, Paragraph, Spacer

from dsl import *
from render import S, Heading, fmt, render_blocks
from render_notes import count_questions


def front(mods, code_dir, out_dir):
    n, t = count_questions(mods)
    subs = sum(len(m["subs"]) for m in mods)
    rows = []
    for m in mods:
        q = sum(1 for s in m["subs"] for b in s["blocks"] if b["t"] == "qa")
        tr = sum(1 for s in m["subs"] for b in s["blocks"] if b["t"] == "qa" and b.get("tag") and "tricky" in b["tag"])
        rows.append([m["num"], m["title"], len(m["subs"]), q, tr])
    fl = [
        Spacer(1, 28),
        Paragraph("MACSE502 Programming for Data Science", S["title"]),
        Paragraph("Topic notes with practice questions, Modules 1 to 6", S["subtitle"]),
        Paragraph(fmt(f"Short notes on every topic and subtopic in the syllabus, each followed by sample questions with worked answers: {n} questions in {subs} sections, "
                      f"{t} of them tagged <b>tricky</b>. The tricky topics (PCA, K-means, broadcasting, pandas traps, data leakage, Scala evaluation and linearization, Spark laziness, shuffles and closures) "
                      "get extra depth and hand-worked numbers. Every output printed here comes from a program that was run."), S["body"]),
        Spacer(1, 4),
    ]
    fl += render_blocks([
        H3("What is inside"),
        T(["Module", "Title", "Sections", "Questions", "Tricky"], rows, [0.09, 0.51, 0.12, 0.14, 0.14]),
        H3("How to use these notes"),
        N(["Read the short notes at the top of a section (they are a summary of the syllabus topic, not a textbook).",
           "Cover the answer under each question, try it on paper, then compare. Questions tagged <b>tricky</b> are the ones that usually cost marks; redo them after a day.",
           "Run or read the demo programs for the sections you find hard. Every program is in <i>Question_Bank/code</i> and its real output in <i>Question_Bank/outputs</i>.",
           "Use the finder below to jump to a tricky topic, the cheat sheet at the back for last-minute revision, and the companion <i>Question Bank</i> PDF for full exam-style questions with marks splits."]),
        P("Tags: <b>[2 marks]</b> etc. show the size of answer expected (my estimate, not an official weight); <b>[predict the output]</b> asks you to work out what a program prints; <b>[tricky]</b> marks a common trap."),
        PB(),
        H3("Tricky-topic finder"),
        T(["Topic", "Where", "The trap in one line"], [
            ["PCA by hand, scaling, choosing k, signs, limits", "2.11", "variance depends on units; centre, scale, eigen-decompose; signs are arbitrary"],
            ["K-means: one iteration, local minima, choosing k, scaling", "2.12", "result depends on start; scale features; inertia always falls with k"],
            ["Data leakage, pipelines, accuracy paradox, overfitting", "2.10", "fit on training data only; accuracy hides a missed minority class"],
            ["Gradient step by hand, zero_grad, int64 labels, early stopping", "2.13, 2.14", "PyTorch accumulates gradients; validation set is not the test set"],
            ["NumPy broadcasting, views vs copies, dtype wrap-around", "2.8", "right-align shapes; slices share memory; uint8 wraps"],
            ["pandas: loc vs iloc, chained assignment, alignment, merge explosion", "2.1, 2.2, 2.6", "end label included; write through one `.loc`; many-to-many multiplies rows"],
            ["Python aliasing, mutable defaults, `t[0] += ...`, copies", "1.2, 1.3, 1.6", "names share objects; defaults are created once"],
            ["Heap is not sorted; priority ties; `pop(0)` cost", "1.8, 1.9", "add a counter; use deque"],
            ["`finally` with return, exception order, MRO", "1.11, 1.12", "finally can override return; specific handlers first"],
            ["REST status codes, retry rules, timeouts", "1.13", "retry 429/5xx, not 404; always set a timeout"],
            ["File modes, Windows `seek`, JSON round trip", "1.14", "`w` truncates; tuples become lists"],
            ["Stemming vs lemmatization, stopwords and negation", "1.15", "lemmatizer needs the POS tag; `not` is a stopword"],
            ["`val` / `def` / `lazy val`, call-by-name", "3.1", "def runs at every use; by-name re-evaluates"],
            ["foldLeft vs foldRight, `::` associativity, Array equality, `'5'.toInt`", "3.3, 3.4, 3.5", "direction matters; arrays compare by reference; Char gives a code"],
            ["Initialisation order, case class with an Array, companion access", "3.7, 3.8, 3.9", "overridden `val` is null in the super-constructor"],
            ["Trait linearization and mixin order", "3.11", "`B with C` gives D, C, B, A; the order of `with` changes results"],
            ["Try vs NonFatal vs Either, `.get` on Failure", "4.3", "fatal errors are not caught by Try; `.get` re-throws"],
            ["Lazy evaluation, cache, shuffle, reduceByKey vs groupByKey", "4.6", "each action recomputes lineage unless cached"],
            ["Closures, accumulators, broadcast", "4.7", "driver variables are not updated from tasks"],
            ["Catalyst plans, DataFrame vs Dataset", "4.8", "filters merge, literals fold, typos fail at different times"],
            ["Decision-matrix arithmetic and weaknesses", "5.3", "show the weighted sum line by line"]], [0.43, 0.12, 0.45]),
        PB(),
        H3("If you are preparing for CAT 2 (your predicted syllabus file)"),
        T(["Predicted item", "Read"], [
            ["Module 2: data visualisation (Matplotlib, Seaborn, Bokeh, Plotly, Folium)", "2.15"],
            ["Module 3: functions, strings, collections, combinators, classes, case classes, traits, access modifiers, REPL", "3.1 to 3.13"],
            ["Module 4: Breeze, Saddle, exception handling, Spark architecture, big data, components", "4.1 to 4.9"],
            ["Module 5: selection criteria", "5.1 to 5.3"]], [0.8, 0.2]),
        P("Check this against what your faculty actually announced for CAT 2; the file only holds a prediction."),
    ], code_dir, out_dir)
    return fl
