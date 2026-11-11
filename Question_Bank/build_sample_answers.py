"""Assemble MACSE502_Sample_Questions_Answers.pdf: model answers to the 18 sample HOT questions in ../Sample Questions.
Run with the venv python:  python build_sample_answers.py      (the programs in code/sa_* must have been run first, see run_and_capture.py)
"""
from pathlib import Path

from PIL import Image as PILImage
from reportlab.platypus import PageBreak, Paragraph, Spacer

import render
from dsl import B, CODE, H3, N, NOTE, P, SNIP, T, TIP, WARN
from render import Doc, Heading, S, fmt, render_blocks

import content_sa_m1
import content_sa_m2
import content_sa_m3
import content_sa_m4

ROOT = Path(__file__).parent
CODE_DIR, OUT_DIR = ROOT / "code", ROOT / "outputs"
IMG_DIR = ROOT.parent / "Sample Questions"
PDF = ROOT / "MACSE502_Sample_Questions_Answers.pdf"
FOOTER = "MACSE502 Programming for Data Science  |  Sample questions: model answers"

MODULES = [
    (1, "Python data structures, REST APIs and NLP", content_sa_m1.QUESTIONS),
    (2, "Python libraries for data science", content_sa_m2.QUESTIONS),
    (3, "Scala data structures and object-oriented programming", content_sa_m3.QUESTIONS),
    (4, "Scala libraries and Spark basics", content_sa_m4.QUESTIONS),
]
JAVA_OPTS_LINE = ("//> using javaOpt --add-opens=java.base/java.lang=ALL-UNNAMED --add-opens=java.base/java.lang.invoke=ALL-UNNAMED "
                  "--add-opens=java.base/java.lang.reflect=ALL-UNNAMED --add-opens=java.base/java.io=ALL-UNNAMED --add-opens=java.base/java.net=ALL-UNNAMED "
                  "--add-opens=java.base/java.nio=ALL-UNNAMED --add-opens=java.base/java.util=ALL-UNNAMED --add-opens=java.base/java.util.concurrent=ALL-UNNAMED "
                  "--add-opens=java.base/java.util.concurrent.atomic=ALL-UNNAMED --add-opens=java.base/sun.nio.ch=ALL-UNNAMED --add-opens=java.base/sun.nio.cs=ALL-UNNAMED "
                  "--add-opens=java.base/sun.security.action=ALL-UNNAMED --add-opens=java.base/sun.util.calendar=ALL-UNNAMED")


def hide_java_opts(text):
    """The 13 --add-opens options of the Spark programs are listed once on the 'How to run' page, not in every listing."""
    return "\n".join("//> using javaOpt <13 --add-opens options for Java 17, see the page 'How to run the programs'>" if l.startswith("//> using javaOpt") else l
                     for l in text.split("\n"))


def prepare(blocks):
    for b in blocks:
        if b["t"] == "code" and b["file"].endswith(".scala") and not b["transform"]:
            b["transform"] = hide_java_opts
    return blocks


SUMMARY = [
    # id, topic, main tools, code
    ("M1-Q1", "Library borrowing system", "dict, list, set, deque, heapq, exceptions, text file", "sa_m1_q1.py"),
    ("M1-Q2", "Weather monitoring with REST APIs", "requests, JSON, retries, exception classes, files", "sa_m1_q2.py, sa_m1_q2_stub.py"),
    ("M1-Q3", "Student support chatbot", "NLTK, ChatterBot, classes, Counter, deque", "sa_m1_q3.py"),
    ("M2-Q1", "Student performance: missing values, statistics, risk", "pandas, scikit-learn imputer, Matplotlib", "sa_m2_q1.py"),
    ("M2-Q2", "Customer purchases: filtering, text data, insights", "pandas str methods, crosstab", "sa_m2_q2.py"),
    ("M2-Q3", "Web data mining and merging", "Beautiful Soup, Scrapy, pandas merge", "sa_m2_q3.py, sa_m2_q3_scrapy.py"),
    ("M2-Q4", "House price prediction", "NumPy, SciPy, scikit-learn", "sa_m2_q4.py"),
    ("M2-Q5", "Smart city dashboard", "Matplotlib, Seaborn, Plotly, Bokeh, Folium", "sa_m2_q5.py"),
    ("M3-Q1", "Course registration", "classes, constructors, List, overloading, inheritance", "sa_m3_q1.scala"),
    ("M3-Q2", "Library management", "abstract class, field overriding, polymorphism, final", "sa_m3_q2.scala"),
    ("M3-Q3", "Shopping cart", "Map, map / filter / reduce, imperative vs functional", "sa_m3_q3.scala"),
    ("M3-Q4", "Employee management", "case class, companion, access modifiers, singleton", "sa_m3_q4.scala"),
    ("M3-Q5", "Transport monitoring", "traits, mixins, Array, REPL", "sa_m3_q5.scala, sa_m3_q5_repl.txt"),
    ("M4-Q1", "Student analytics at scale", "Spark architecture, Breeze, MLlib", "sa_m4_q1.scala"),
    ("M4-Q2", "Healthcare data", "Saddle Series / Frame, Spark", "sa_m4_q2_saddle.scala, sa_m4_q2_spark.scala"),
    ("M4-Q3", "E-commerce recommender", "exception handling, fault tolerance, Spark", "sa_m4_q3.scala"),
    ("M4-Q4", "Social-media big data", "driver, executors, scheduling, metrics", "sa_m4_q4.scala"),
    ("M4-Q5", "Financial risk", "Breeze, Saddle, Spark", "sa_m4_q5_saddle_breeze.scala, sa_m4_q5_spark.scala"),
]


def front():
    fl = [Spacer(1, 40), Paragraph("MACSE502 Programming for Data Science", S["subtitle"]),
          Paragraph("Sample Questions: Model Answers", S["title"]),
          Paragraph("Answers to the 18 higher-order-thinking (HOT) questions of the <i>Sample Questions</i> folder: 3 on Python data structures, APIs and NLP, 5 on Python libraries, 5 on Scala, 5 on Spark, Breeze and Saddle. "
                    "Each answer replies to every bullet of its question and comes with a program that was run on the dataset printed in the question.", S["subtitle"])]
    rows = [[a, b, c, d] for a, b, c, d in SUMMARY]
    fl += render_blocks([T(["Question", "Topic", "Main tools", "Code (Question_Bank/code)"], rows, [0.1, 0.32, 0.31, 0.27])], CODE_DIR, OUT_DIR)
    fl += render_blocks([WARN("These are model answers written for revision. I do not know the marking scheme of the examiner, so no marks are given, and the points a "
                              "particular examiner expects may differ. Every program and every number in the printed outputs was produced by really running it.")], CODE_DIR, OUT_DIR)
    return fl


def how_to_read():
    blocks = [
        H3("How each answer is built"),
        N(["The question as given (the screenshot), so the dataset and the bullets are in front of you.",
           "<b>Answer, point by point</b>: one block per bullet, in the order asked, with the tool named in the first sentence and the reason (\"why this and not that\") stated, because HOT questions reward justification.",
           "<b>Code, run on the dataset of the question</b>, followed by its real output. Numbers quoted in the text come from that output.",
           "Where something had to be made up (invented posts, map coordinates, stand-in web pages) the answer says so."]),
        H3("A five-step recipe for any scenario question"),
        N(["<b>Restate the goal</b> in one line (what decision must the answer support?).",
           "<b>Answer every bullet</b> in the order asked, a short paragraph or a small table each. Use the library names from the question.",
           "<b>Show the central code</b> in a few lines: load, clean, compute, show. Do not print a whole program unless asked.",
           "<b>Justify</b>: compare at least two options for every important choice (median or mean, List or Array, Spark or pandas) and say why one wins here.",
           "<b>State the limits</b>: small sample, assumptions made, and one next step with more data."]),
        H3("How to run the programs"),
        P("Python programs: `python sa_m2_q1.py` in a Python 3.10 environment with pandas, NumPy, SciPy, scikit-learn, Matplotlib, Seaborn, Plotly, Bokeh, Folium and Beautiful Soup. "
          "Extra needs: `sa_m1_q2.py` needs `requests` and talks to the stand-in service, which it imports and starts from `sa_m1_q2_stub.py`; `sa_m1_q3.py` needs NLTK (with its `punkt` and `stopwords` data) and ChatterBot, which is best kept in its own virtual environment because it installs many dependencies (spaCy among them) that can clash with the other libraries; "
          "`sa_m2_q3_scrapy.py` needs `pip install scrapy`. "
          "Scala programs: `scala-cli run sa_m3_q1.scala` (Scala 2.13.12, Java 17). The `//> using dep` lines at the top of a file download the libraries."),
        P("The Spark programs start Spark in local mode (`master(\"local[2]\")`, one machine, no cluster). On Java 17 Spark 3.5 needs the following line in each Spark file, which the listings abbreviate:"),
        SNIP(JAVA_OPTS_LINE, "scala", "The javaOpt line of the Spark programs"),
        TIP("Three small programs are meant to fail (`sa_m3_q2_final_error.scala`, `sa_m3_q2_final_class_error.scala`, `sa_m3_q4_private_error.scala`); their compiler messages are quoted in the answers. "
            "`run_sa_extras.py` produces those messages and the REPL transcript."),
    ]
    return [PageBreak(), Heading("How to read and run this file", S["h1"], 0)] + render_blocks(blocks, CODE_DIR, OUT_DIR)


def closing():
    blocks = [
        H3("What was run, and what was not"),
        B(["18 questions, 25 runs on this computer: 21 programs (9 Python, 5 Scala, 7 on Spark, Breeze or Saddle), 3 files that are meant to fail (to capture compiler messages) and 1 REPL session. The outputs in the document are the captured outputs.",
           "Versions: Python 3.10, pandas 2.3.3, NumPy 1.26.4, SciPy 1.15.3, scikit-learn 1.7.2, Matplotlib 3.10.0, Seaborn 0.13.2, Plotly 7.1.0, Bokeh 3.9.2, Folium 0.20.0, Beautiful Soup 4.15.0, Scrapy 2.19.0, "
           "NLTK 3.10.4, ChatterBot 1.2.15 (with spaCy 3.8.18); "
           "Scala 2.13.12 on Java 17, Spark 3.5.1 (local mode), Breeze 2.1.0, Saddle 4.0.0-M14 (a maintained fork; the original Saddle does not exist for Scala 2.13).",
           "The datasets are exactly the ones printed in the screenshots. Invented material: the five posts of M4-Q4, the map coordinates of M2-Q5, the HTML pages of M2-Q3 (stand-ins for the two websites; no website was contacted), "
           "and the weather service of M1-Q2 (a small local server that fails on purpose; no weather provider was contacted).",
           "Two screenshots are cut off at the bottom (M4-Q1 and M4-Q5). Only the visible bullets are answered.",
           "M1-Q1 consists of five screenshots, and the one that would hold the opening scenario text (file number ...034) is not in the folder. That answer follows the datasets and the seven tasks.",
           "M1-Q3 answers the question with a keyword matcher built on NLTK plus a ChatterBot layer; it is a small demonstration with a handful of FAQs, not a trained support bot.",
           "Spark ran on one machine, so statements about clusters (executors on many nodes, cluster managers) come from the Spark documentation and from the structure of the program, not from a cluster run. Spark writes to disk and Structured Streaming were not used (they need extra setup on Windows).",
           "With only four or five rows per question, statistics and machine-learning results are demonstrations of method, not findings."]),
    ]
    return [PageBreak(), Heading("Notes and limits", S["h1"], 0)] + render_blocks(blocks, CODE_DIR, OUT_DIR)


def build():
    story = front()
    story += [PageBreak(), Heading("Contents", S["h1"], 0, toc=False), render.make_toc()]
    story += how_to_read()
    for num, title, questions in MODULES:
        story += [PageBreak(), Heading(f"Module {num}: {title}", S["h1"], 0),
                  Paragraph(f"{len(questions)} sample questions with model answers.", S["body"])]
        for i, q in enumerate(questions):
            if i:
                story.append(PageBreak())
            story.append(Heading(f"{q['id']}  {q['title']}", S["h2"], 1))
            images = [q["image"]] if isinstance(q["image"], str) else list(q["image"])
            width = 14.5 if len(images) == 1 else None          # several screenshots: size each by its own pixel width
            blocks = []
            for k, name in enumerate(images):
                w_cm = width or min(11.0, max(7.5, PILImage.open(IMG_DIR / name).size[0] / 84))
                cap = "The question as given" if len(images) == 1 else f"The question as given, part {k + 1} of {len(images)}"
                blocks.append({"t": "img", "path": str(IMG_DIR / name), "width_cm": w_cm, "caption": f"{cap} (Sample Questions/{name})"})
            blocks += q["blocks"]
            story += render_blocks(prepare(blocks), CODE_DIR, OUT_DIR)
    story += closing()
    doc = Doc(str(PDF), title="MACSE502 Programming for Data Science: Sample Questions, Model Answers", footer=FOOTER)
    doc.multiBuild(story)
    return doc.page


if __name__ == "__main__":
    pages = build()
    n = sum(len(q) for _, _, q in MODULES)
    print(f"built {PDF.name}: {pages} pages, {n} questions")
