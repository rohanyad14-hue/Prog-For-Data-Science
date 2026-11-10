"""Cover, how-to-use, coverage map and the answer-writing guide."""
from dsl import *
from reportlab.platypus import PageBreak, Paragraph, Spacer

from render import S, Heading, fmt, render_blocks


def totals(m):
    short_marks = sum(q["marks"] for q in m["shorts"])
    long_marks = sum(q["marks"] for q in m["longs"])
    return len(m["mcqs"]), len(m["shorts"]), len(m["longs"]), len(m["mcqs"]) + short_marks + long_marks


def front_matter(mods, code_dir, out_dir):
    n_mcq = sum(len(m["mcqs"]) for m in mods)
    n_short = sum(len(m["shorts"]) for m in mods)
    n_long = sum(len(m["longs"]) for m in mods)
    cover = [
        Spacer(1, 30),
        Paragraph("MACSE502 Programming for Data Science", S["title"]),
        Paragraph("Question bank with answers, Modules 1 to 6", S["subtitle"]),
        Paragraph(fmt(f"{n_mcq} multiple-choice questions, {n_short} short-answer questions and {n_long} long questions, each with a model answer. "
                      "Questions follow your syllabus (ETH, version 1.0), the high-frequency list in your FAT notes and the 20 lab experiments. "
                      "Code answers were run, and the real output is printed beside them."), S["body"]),
        Spacer(1, 6),
    ]
    rows = []
    for m in mods:
        a, b, c, marks = totals(m)
        rows.append([f"{m['num']}", m["title"], m["hours"], a, b, c, marks])
    cover += render_blocks([
        H3("What is inside"),
        T(["Module", "Title", "Hours", "MCQ", "Short", "Long", "Marks"], rows, [0.08, 0.44, 0.12, 0.09, 0.09, 0.09, 0.09]),
        P("Marks: 1 per multiple-choice question, the stated marks for short and long questions. The marks given are for self-scoring; "
          "they are not the official weights of your paper."),
        H3("How to use it"),
        N(["Pick a module. Do <b>Part 1 (Test yourself)</b> on paper without looking at the answers. Time yourself: about 1 minute per MCQ, "
           "4 minutes per 3-mark answer, 8 minutes per 5-mark answer, 20 to 25 minutes per 10-mark answer.",
           "Open <b>Part 2 (Answers)</b>. Tick each point of the model answer that you covered and score yourself with the suggested marks split under each long answer.",
           "Write your scores in the scorecard at the back. Anything below 60 percent goes on the revision list; redo it after one day and again after one week.",
           "For code questions, type the code yourself, run it, and compare your output with the printed output.",
           "Finish with the mock paper at the back (it samples every module)."]),
        H3("What was verified"),
        P("Every program in this book was executed: Python 3.10 for modules 1, 2 and 5; Scala 2.13.12 on Java 17 (through scala-cli) for modules 3 and 4, "
          "including Breeze, Spire, Saddle and Spark 3.5.1 in local mode. The REST API examples use a mock server that returns real `requests.Response` objects, "
          "so no live service was called. ChatterBot 1.2.15 was run for the chatbot question. Details are in the appendix at the back."),
        WARN("Module 6 has no topic list in the syllabus, and I could not find a published VIT marking scheme for this course. "
             "Treat the writing advice as sound general practice and check it against two or three past papers (links at the back)."),
    ], code_dir, out_dir)

    guide = [PageBreak(), Heading("How to write answers that score", S["h1"], 0)]
    guide += render_blocks([
        P("What follows comes from three sources: the way your FAT notes phrase the likely questions (Explain, Compare, Detail, Define, Evaluate, State, Contrast, "
          "Write code), general exam-writing practice, and what a marker needs in order to give a mark quickly. It is not an official VIT rubric."),
        H3("1. Read the command word first"),
        T(["Command word", "What to produce", "Example from your FAT notes"], [
            ["Define, State, What is", "one or two precise sentences, then the key properties", "What is an RDD? Define its four properties."],
            ["Explain, Describe, Detail", "what it is, how it works, one example or diagram", "Detail four built-in capabilities of case classes."],
            ["Compare, Differentiate, Contrast", "a table with at least four rows, then one line saying when to use each", "Compare BeautifulSoup and Scrapy."],
            ["Write code, Implement, Develop", "clean code with comments, sample input, printed output, two lines of explanation", "Write code demonstrating `groupby` with multiple aggregations."],
            ["Trace, Show the output", "a step-by-step table of values", "Stack contents after each undo/redo step."],
            ["Design, Propose", "components (classes with attributes and methods), flow diagram, how parts interact", "Propose an object-oriented design for the chatbot."],
            ["Evaluate, Justify, Discuss", "criteria, evidence taken from the scenario, trade-off, conclusion", "Evaluate Python vs Scala across the selection criteria."],
            ["List", "short numbered points, no essay", "List 3 transformations and 3 actions."]], [0.22, 0.46, 0.32]),
        H3("2. Match the length to the marks"),
        T(["Marks", "Typical length", "Contents"], [
            ["1", "one line or one option", "the fact"],
            ["2 to 3", "3 to 6 lines", "definition + 2 to 3 points (or a 3-row table) + a one-line example"],
            ["5", "half a page", "definition, 4 to 5 points, small diagram or code, example"],
            ["10", "two pages", "introduction, headed sections, diagram or table, code with output, worked example, one-line conclusion"]], [0.1, 0.25, 0.65]),
        P("These are rules of thumb. If the paper has a different pattern, follow the question's marks and the space given."),
        H3("3. Structure of a 10-mark answer"),
        N(["Definition in two lines (use the textbook's term).",
           "Diagram or comparison table (label every part; examiners often award marks just for the diagram).",
           "Numbered explanation, one idea per point, each with the reason \"because ...\".",
           "Code or worked example, with output.",
           "Link to the scenario in the question (use its numbers and names).",
           "One-line conclusion that answers the question asked."]),
        H3("4. Code answers"),
        B(["Indent consistently, use meaningful names, and put a comment on each step that carries marks.",
           "Show the output (copy it from a real run). A correct output is strong evidence that the code works.",
           "Handle the error case if the question mentions failure (try/except in Python, `Try` or `Option` in Scala).",
           "State the complexity or the reason for a choice in one line, for example \"`deque.popleft()` is O(1), `list.pop(0)` is O(n)\"."]),
        H3("5. Words that tell the marker you know the topic"),
        T(["Module", "Use these terms where they apply"], [
            ["1", "hashable, O(1) average, LIFO, FIFO, min-heap, idempotent, status code, retry with back-off, fail fast, `with` closes the file, tokenization, lemmatization"],
            ["2", "vectorised, broadcasting, split-apply-combine, `loc` is label based, `iloc` is positional, inner/left/outer, non-blocking, event loop, standardise before PCA, inertia"],
            ["3", "immutable, `val` vs `var`, structural equality, companion object, `apply`, `unapply`, trait mixin, linearization, `override`, `final`, pattern matching"],
            ["4", "driver, executor, cluster manager, partition, DAG, lineage, lazy evaluation, narrow vs wide, shuffle, action, Catalyst, `Option`/`Try`/`Either`"],
            ["5", "criteria, trade-off, weighted decision matrix, time to production, elasticity, static vs dynamic typing, justify with the scenario"],
            ["6", "consent, data minimisation, pseudonymisation, bias, hallucination, drift, accountability"]], [0.1, 0.9]),
        H3("6. Common slips that cost marks"),
        B(["No output shown after the code.",
           "Mixing Python and Scala syntax: `val x = 5` vs `x = 5`; `a[0]` (Python) vs `a(0)` (Scala array); forgetting `new` in Scala when there is no companion `apply`.",
           "Python: calling a list \"faster than a tuple\" as the only difference; using `loc` when you mean `iloc`; a bare `except:`.",
           "Spark: saying a transformation \"runs\" before an action; forgetting that `collect` brings all data to the driver; saying Spark \"stores\" data.",
           "Scala: `==` vs `eq`; calling an immutable `List` mutable because the `var` changed.",
           "A comparison answer written as paragraphs instead of a table."]),
        TIP("In the lab viva you may be asked to explain your own code line by line. Be able to run each lab file and say what each combinator, constructor or DataFrame call returns."),
    ], code_dir, out_dir)
    return cover + guide
