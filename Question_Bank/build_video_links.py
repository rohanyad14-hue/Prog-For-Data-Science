"""Build MACSE502_YouTube_Search_Links.pdf: one clickable YouTube search link per syllabus subtopic.
Run with the venv python:  python build_video_links.py
The links are YouTube search pages, not specific videos (individual videos could not be checked when this was written).
"""
from pathlib import Path
from urllib.parse import quote_plus

from reportlab.lib import colors
from reportlab.platypus import KeepTogether, PageBreak, Paragraph, Spacer, Table, TableStyle

from render import GREY, NAVY, RULE, S, TEXT_W, Doc, Heading

ROOT = Path(__file__).parent
PDF = ROOT / "MACSE502_YouTube_Search_Links.pdf"
FOOTER = "MACSE502 Programming for Data Science  |  YouTube search links by syllabus subtopic"
YT = "https://www.youtube.com/results?search_query="

MODULES = [
    (1, "Python Data Structures", "8 h", [
        ("Condition and Branching Statements", "python if elif else conditional statements tutorial"),
        ("List, Tuple, Dictionary, Set", "python list tuple dictionary set tutorial"),
        ("Stack, Queue, Priority Queue", "python stack queue priority queue heapq deque tutorial"),
        ("String handling methods", "python string methods tutorial"),
        ("Exception Handling", "python exception handling try except finally tutorial"),
        ("Object-Oriented Concepts", "python object oriented programming classes inheritance tutorial"),
        ("File Handling", "python file handling read write tutorial"),
        ("APIs and Data Collection; Simple API and REST APIs", "python requests REST API json tutorial"),
        ("NLTK", "nltk python tutorial tokenization stemming stop words"),
        ("ChatterBot", "python chatterbot chatbot tutorial"),
    ]),
    (2, "Python Libraries", "9 h", [
        ("Series", "pandas series tutorial"),
        ("DataFrame", "pandas dataframe tutorial"),
        ("Handling Missing Values", "pandas handling missing values fillna dropna"),
        ("Built-in functions; Data Operations", "pandas describe groupby sort_values apply tutorial"),
        ("Filtering Data in DataFrame; Data Extraction", "pandas filter rows loc iloc query tutorial"),
        ("Working with Text Data", "pandas string methods str contains extract tutorial"),
        ("Merging DataFrames", "pandas merge join concat tutorial"),
        ("Pandas (whole library)", "pandas full course python data analysis"),
        ("NumPy", "numpy tutorial arrays python"),
        ("SciPy", "scipy tutorial python"),
        ("Scikit-Learn", "scikit-learn tutorial python machine learning"),
        ("XGBoost", "xgboost python tutorial"),
        ("Keras", "keras tutorial neural network python"),
        ("TensorFlow", "tensorflow tutorial beginners"),
        ("PyTorch", "pytorch tutorial beginners"),
        ("Beautiful Soup", "beautiful soup python web scraping tutorial"),
        ("Scrapy", "scrapy python web scraping tutorial"),
        ("Matplotlib", "matplotlib tutorial python"),
        ("Seaborn", "seaborn tutorial python"),
        ("Bokeh", "bokeh python interactive visualization tutorial"),
        ("Plotly", "plotly python tutorial"),
        ("Folium", "folium python map tutorial"),
    ]),
    (3, "Scala Data Structures and OOP", "12 h", [
        ("Whole module: Scala for beginners", "scala full course for beginners"),
        ("Expanded Function Format", "scala function definition def tutorial"),
        ("Variables, Numbers, Variable types", "scala val var data types tutorial"),
        ("Strings", "scala strings string interpolation tutorial"),
        ("Getting user input", "scala readLine user input tutorial"),
        ("Operators, Booleans", "scala operators boolean tutorial"),
        ("Arrays", "scala array tutorial"),
        ("Scala Array-REPL", "scala REPL tutorial"),
        ("Lists", "scala list tutorial"),
        ("Tuple", "scala tuple tutorial"),
        ("Sets, Hash set", "scala set hashset tutorial"),
        ("Maps", "scala map tutorial"),
        ("Functional Combinators", "scala map filter reduce fold flatMap tutorial"),
        ("Scala Object and Class", "scala class object tutorial"),
        ("Anonymous object", "scala anonymous class object tutorial"),
        ("Singleton, Companion Object", "scala singleton object companion object tutorial"),
        ("Case Classes", "scala case class tutorial"),
        ("Constructors", "scala constructors primary auxiliary tutorial"),
        ("Method Overloading", "scala method overloading tutorial"),
        ("This Keyword", "scala this keyword tutorial"),
        ("Inheritance", "scala inheritance tutorial"),
        ("Field Overriding, Final", "scala override val final keyword tutorial"),
        ("Abstract Class", "scala abstract class tutorial"),
        ("Trait, Trait Mixins", "scala traits mixin tutorial"),
        ("Access Modifiers", "scala access modifiers private protected tutorial"),
    ]),
    (4, "Scala Libraries and Spark Basics", "8 h", [
        ("Breeze", "scala breeze library tutorial"),
        ("Saddle", "scala saddle library series frame"),
        ("Exception Handling (Scala)", "scala exception handling try catch finally Try Option Either"),
        ("Apache Spark Architecture", "apache spark architecture driver executor cluster manager"),
        ("Spark Big Data", "big data introduction hadoop vs spark"),
        ("Apache Spark Components", "apache spark components spark core sql streaming mllib graphx"),
    ]),
    (5, "Programming language selection criteria", "6 h", [
        ("All criteria, overview", "how to choose a programming language for a project criteria"),
        ("Performance, Efficiency", "programming language performance comparison python java scala"),
        ("Security", "choosing a programming language security considerations"),
        ("Skill Set, Programmer experience, Support and community", "choosing a programming language team skills community support"),
        ("Targeted platform, Size of the Deployment, Purpose", "choosing programming language target platform deployment requirements"),
        ("Elasticity of a language", "programming language flexibility scalability comparison"),
        ("Time to production, Ease of Development and Maintenance", "time to market programming language maintainability"),
        ("Availability of an IDE", "best IDE for python and scala comparison"),
        ("Error Checking and Diagnosis", "static vs dynamic typing compile time vs runtime errors"),
        ("Applied: Python vs Scala for data work", "python vs scala for data engineering and spark"),
    ]),
]

LINK_COLOR = "#1a56b0"


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def module_table(rows):
    data = [[Paragraph("Subtopic", S["cellh"]), Paragraph("Open on YouTube (click the search words)", S["cellh"])]]
    for sub, q in rows:
        link = f'<a href="{YT}{quote_plus(q)}" color="{LINK_COLOR}"><u>{esc(q)}</u></a>'
        data.append([Paragraph(esc(sub), S["cell"]), Paragraph(link, S["cell"])])
    t = Table(data, colWidths=[0.38 * TEXT_W, 0.62 * TEXT_W], repeatRows=1)
    st = [("BACKGROUND", (0, 0), (-1, 0), NAVY), ("GRID", (0, 0), (-1, -1), 0.4, RULE), ("VALIGN", (0, 0), (-1, -1), "TOP"),
          ("LEFTPADDING", (0, 0), (-1, -1), 5), ("RIGHTPADDING", (0, 0), (-1, -1), 5),
          ("TOPPADDING", (0, 0), (-1, -1), 3.4), ("BOTTOMPADDING", (0, 0), (-1, -1), 3.4)]
    st += [("BACKGROUND", (0, i), (-1, i), GREY) for i in range(2, len(data), 2)]
    t.setStyle(TableStyle(st))
    return t


def build():
    n = sum(len(r) for _, _, _, r in MODULES)
    story = [Spacer(1, 6), Paragraph("MACSE502 Programming for Data Science", S["subtitle"]),
             Paragraph("YouTube Search Links by Syllabus Subtopic", S["title"]),
             Paragraph(f"{n} clickable searches covering modules 1 to 5. Module 6 lists no topics in the syllabus.", S["subtitle"]),
             Paragraph("<b>What these links are.</b> Each one opens YouTube's own search results for that subtopic. They are search pages, "
                       "not specific videos: individual video links could not be checked when this file was made, so none are listed and nothing here is a "
                       "recommendation of a particular video. A printed copy keeps the search words but loses the click, so the words are enough to type into YouTube.", S["note"]),
             Paragraph("<b>Choosing a video.</b> For Python, pandas and Scala, prefer a recent and longer tutorial, because library APIs change over the years. "
                       "Check that the video uses the version you use in the lab (Scala 2.13, Spark 3.5). Module 5 is about opinion and trade-offs, so your lecture notes "
                       "are the better source there.", S["tip"]),
             Paragraph("Related subtopics that the syllabus lists separately are combined in one row, for example \"Singleton\" and \"Companion Object\". "
                       "Module 5 lists 14 criteria; they are grouped into related searches because a single criterion such as \"Purpose\" gives poor results.", S["body"])]
    for num, title, hrs, rows in MODULES:
        head = Heading(f"Module {num}: {title} ({hrs})", S["h2"], 0, toc=False)
        story += [head, module_table(rows), Spacer(1, 4)]
    story += [Heading("Module 6: Contemporary Issues (2 h)", S["h2"], 0, toc=False),
              Paragraph("The syllabus lists no topics for this module, so there is nothing to search for.", S["body"])]
    doc = Doc(str(PDF), title="MACSE502 Programming for Data Science: YouTube search links", footer=FOOTER)
    doc.multiBuild(story)
    return doc.page, n


if __name__ == "__main__":
    pages, n = build()
    print(f"built {PDF.name}: {pages} pages, {n} links")
