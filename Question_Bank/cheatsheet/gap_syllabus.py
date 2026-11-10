"""The syllabus (MACSE502 ETH / ELA PDF) broken into topics, each mapped to where code for it can be found.
Status:  "cheat"  covered by the lab-based cheat sheet (MACSE502_Coding_Cheat_Sheet.pdf, group letter)
         "new"    code added in MACSE502_Syllabus_Gap_Code.pdf (group number)
         "both"   basics in the cheat sheet, more in the gap file
         "theory" no programming content
check_against_pdf() proves that every topic phrase really occurs in the syllabus PDF text.
"""
import glob
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
SYLLABUS_DIR = HERE.parent.parent / "MACSE502_2026-07-06_19-06-12"

CHEAT = {"A": "pandas basics", "B": "cleaning and missing values", "C": "NumPy", "D": "Matplotlib / seaborn EDA", "E": "Beautiful Soup", "F": "Plotly",
         "G": "Bokeh", "H": "PCA / K-means", "S1": "Scala collections", "S2": "combinators and case class", "S3": "Saddle", "S4": "Breeze and Plotly.Scala", "S5": "Spire"}

# (module number, title, hours, [(phrase as it appears in the syllabus, status, where)])
MODULES = [
    (1, "Python Data Structures", 8, [
        ("Condition and Branching Statements", "new", "1.1"),
        ("List, Tuple, Dictionary, Set", "new", "1.2"),
        ("Stack, Queue, Priority Queue", "new", "1.3"),
        ("String handling methods", "new", "1.4"),
        ("Exception Handling", "new", "1.5"),
        ("Object-Oriented Concepts", "new", "1.6"),
        ("APIs and Data Collection", "new", "1.8"),
        ("Simple API and REST APIs", "new", "1.8"),
        ("File Handling", "new", "1.7"),
        ("NLTK", "new", "1.9"),
        ("ChatterBot", "new", "1.10"),
    ]),
    (2, "Python Libraries", 9, [
        ("Series", "new", "2.1"),
        ("DataFrame", "both", "cheat A; gap 2.2"),
        ("Handling Missing Values", "both", "cheat B; gap 2.1"),
        ("Built-in functions", "new", "2.2"),
        ("Data Operations", "new", "2.2"),
        ("Filtering Data in DataFrame", "both", "cheat A; gap 2.2"),
        ("Data Extraction", "new", "2.2"),
        ("Working with Text Data", "new", "2.3"),
        ("Merging DataFrames", "new", "2.4"),
        ("Scrapy", "new", "2.6"),
        ("Beautiful Soup", "cheat", "cheat E"),
        ("NumPy", "cheat", "cheat C"),
        ("SciPy", "new", "2.5"),
        ("Pandas", "cheat", "cheat A, B"),
        ("Keras", "new", "2.9"),
        ("Scikit - Learn", "both", "cheat H (PCA, K-means); gap 2.7"),
        ("PyTorch", "new", "2.11"),
        ("TensorFlow", "new", "2.10"),
        ("XGBoost", "new", "2.8"),
        ("Matplotlib", "both", "cheat D; gap 2.13"),
        ("Seaborn", "both", "cheat D; gap 2.13"),
        ("Bokeh", "cheat", "cheat G"),
        ("Plotly", "cheat", "cheat F"),
        ("Folium", "new", "2.12"),
    ]),
    (3, "Scala Data Structures and Object-Oriented Programming", 12, [
        ("Expanded Function Format", "new", "3.1"),
        ("Variables and Strings", "new", "3.2"),
        ("Getting user input", "new", "3.3"),
        ("Numbers", "new", "3.2"),
        ("Variable types", "new", "3.2"),
        ("Operators", "new", "3.3"),
        ("Booleans", "new", "3.3"),
        ("Arrays", "both", "cheat S1; gap 3.4"),
        ("Lists", "cheat", "cheat S1"),
        ("Tuple", "cheat", "cheat S1"),
        ("Sets", "cheat", "cheat S1"),
        ("Hash set", "new", "3.4"),
        ("Maps", "cheat", "cheat S1"),
        ("Functional Combinators", "cheat", "cheat S2"),
        ("Scala Object and Class", "new", "3.5"),
        ("Anonymous object", "new", "3.5"),
        ("Singleton", "new", "3.5"),
        ("Companion Object", "new", "3.5"),
        ("Case Classes", "both", "cheat S2; gap 3.5"),
        ("Constructors", "new", "3.5"),
        ("Method Overloading", "new", "3.5"),
        ("This Keyword", "new", "3.5"),
        ("Inheritance", "new", "3.6"),
        ("Field Overriding", "new", "3.6"),
        ("Final", "new", "3.6"),
        ("Abstract Class", "new", "3.6"),
        ("Trait", "new", "3.6"),
        ("Trait Mixins", "new", "3.6"),
        ("Access Modifiers", "new", "3.5"),
        ("Scala Array-REPL", "new", "3.4"),
    ]),
    (4, "Scala Libraries and Spark Basics", 8, [
        ("Breeze", "cheat", "cheat S4"),
        ("saddle", "cheat", "cheat S3"),
        ("Exception Handling", "new", "4.1"),
        ("Apache Spark Architecture", "new", "4.2"),
        ("Spark Big Data", "new", "4.2"),
        ("Apache Spark Components", "new", "4.2"),
    ]),
    (5, "Programming language selection criteria", 6, [
        ("Size of the Deployment", "new", "5.1 (as a scoring matrix)"),
        ("Security", "new", "5.1 (as a scoring matrix)"),
        ("Skill Set", "new", "5.1 (as a scoring matrix)"),
        ("targeted platform", "new", "5.1 (as a scoring matrix)"),
        ("elasticity of a language", "new", "5.1 (as a scoring matrix)"),
        ("time to production", "new", "5.1 (as a scoring matrix)"),
        ("performance", "new", "5.1 (as a scoring matrix)"),
        ("support and community", "new", "5.1 (as a scoring matrix)"),
        ("Purpose", "new", "5.1 (as a scoring matrix)"),
        ("Programmer experience", "new", "5.1 (as a scoring matrix)"),
        ("Ease of Development and Maintenance", "new", "5.1 (as a scoring matrix)"),
        ("Efficiency", "new", "5.1 (as a scoring matrix)"),
        ("Availability of an IDE", "new", "5.1 (as a scoring matrix)"),
        ("Error Checking and Diagnosis", "new", "5.1 (as a scoring matrix)"),
    ]),
    (6, "Contemporary Issues", 2, [
        ("Contemporary Issues", "theory", "the syllabus lists no topics"),
    ]),
]

# The indicative list of experiments in the syllabus and the cheat-sheet table that solves each
EXPERIMENTS = [
    ("Basic Data Manipulation with Pandas", "1", "A"),
    ("Data Cleaning and Preprocessing with Pandas", "2", "B"),
    ("Creating and Manipulating Arrays", "3", "C"),
    ("Feature Engineering, Exploratory Data Analysis", "4", "D"),
    ("Scrape data from a webpage", "5", "E"),
    ("Interactive Bar Chart with Plotly", "6", "F"),
    ("Interactive Scatter Plot with Plotly", "7", "F"),
    ("Interactive Line Plot with Bokeh", "8", "G"),
    ("Interactive Bar Chart with Bokeh", "9", "G"),
    ("Interactive Scatter Plot with Bokeh", "10", "G"),
    ("Visualizing Clusters with scikit-learn and Plotly", "11", "H"),
    ("Visualizing PCA with scikit-learn and Plotly", "12", "H"),
    ("Introduction to arrays in Scala", "13", "S1"),
    ("Understanding lists, sets, and tuples in Scala", "14", "S1"),
    ("Handling collisions and resolving conflicts in HashMap", "15", "S1"),
    ("Exploring advanced functional combinators", "16", "S2"),
    ("Case Classes", "17", "S2"),
    ("Use Saddle to load and manipulate a dataset", "18", "S3"),
    ("Use Breeze library to calculate total revenue", "19", "S4"),
    ("Analyse fruit prices using Spire", "20", "S5"),
]


def _norm(s):
    s = s.lower().replace("\u2013", "-").replace("\u2014", "-").replace("\u2019", "'")
    s = re.sub(r"\s+", " ", s)
    s = re.sub(r"\s*-\s*", "-", s)
    return s.strip()


def syllabus_text():
    import fitz
    path = sorted(glob.glob(str(SYLLABUS_DIR / "*_ETH_*.pdf")))[0]
    doc = fitz.open(path)
    return Path(path).name, _norm("\n".join(p.get_text() for p in doc))


def check_against_pdf():
    """-> (pdf name, [phrases that were NOT found])"""
    name, text = syllabus_text()
    missing = []
    for _, _, _, topics in MODULES:
        for phrase, _, _ in topics:
            if _norm(phrase) not in text:
                missing.append(phrase)
    for phrase, _, _ in EXPERIMENTS:
        if _norm(phrase) not in text:
            missing.append(phrase)
    return name, missing


if __name__ == "__main__":
    n, miss = check_against_pdf()
    print("syllabus file:", n)
    print("topics:", sum(len(t) for *_, t in MODULES), "experiments:", len(EXPERIMENTS), "not found in the PDF text:", miss)
