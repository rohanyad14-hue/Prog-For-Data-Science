"""Build MACSE502_Syllabus_Gap_Code.pdf: code for the syllabus topics that the lab-based cheat sheet does not cover.
Run with the venv python:  python build_gap.py      (needs gap_py_results.json and gap_scala_results.json from the verifiers)
"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parent))

from reportlab.lib import colors  # noqa: E402, F401
from reportlab.lib.styles import ParagraphStyle  # noqa: E402
from reportlab.platypus import CondPageBreak, PageBreak, Paragraph, Spacer, Table, TableStyle  # noqa: E402

import build_cheatsheet as bc  # noqa: E402  (table, code_cell, chars, callout, bullets helpers)
import gap_py  # noqa: E402
import gap_scala  # noqa: E402
import gap_syllabus as syl  # noqa: E402
from render import LIGHT, RULE, TEXT_W, S, Doc, Heading, fmt, make_toc  # noqa: E402

PDF = HERE / "MACSE502_Syllabus_Gap_Code.pdf"
FOOTER = "MACSE502 Programming for Data Science  |  Syllabus topics not covered by the lab cheat sheet"
PY_RES = json.loads((HERE / "gap_py_results.json").read_text(encoding="utf-8"))
SC_RES = json.loads((HERE / "gap_scala_results.json").read_text(encoding="utf-8"))

SKIP_REASON = {**gap_py.SKIP_REASON, **gap_scala.SKIP_REASON}
INSTALL = {
    "1.8": "pip install requests pandas", "1.9": "pip install nltk scikit-learn", "1.10": "pip install chatterbot spacy, then python -m spacy download en_core_web_sm",
    "2.1": "pip install pandas numpy", "2.2": "pip install pandas numpy", "2.3": "pip install pandas", "2.4": "pip install pandas",
    "2.5": "pip install scipy numpy", "2.6": "pip install scrapy", "2.7": "pip install scikit-learn joblib",
    "2.8": "pip install xgboost scikit-learn", "2.9": "pip install keras tensorflow scikit-learn", "2.10": "pip install tensorflow",
    "2.11": "pip install torch scikit-learn", "2.12": "pip install folium", "2.13": "pip install matplotlib seaborn pandas", "5.1": "pip install pandas matplotlib",
}
H2_FREE = ParagraphStyle("h2free", parent=S["h2"], keepWithNext=0)   # heading that may be followed by a table longer than the rest of the page
STATUS_STYLE = {"new": ("#1e7a3a", "new here"), "both": ("#2f6db5", "basics in the cheat sheet, more here"), "cheat": ("#555555", "already in the cheat sheet"),
                "theory": ("#a85a00", "no code")}


def where_text(status, where):
    if status == "cheat":
        return where.replace("cheat ", "Cheat sheet table ")
    if status == "both":
        return where.replace("cheat ", "Cheat sheet table ").replace("gap ", "this file, ")
    if where.startswith("the syllabus"):
        return where
    return "This file, " + where


def group_flow(g, lang):
    fl = [CondPageBreak(5 * 28), Heading(f"{g['id']}  {g['title']}", S["h2"], 1)]
    cap = f"Syllabus: {g['topics']}.  {len(g['rows'])} rows, in running order."
    if lang == "python":
        env = {"main": "", "cb": " Needs ChatterBot (its own environment).", "sc": " Needs Scrapy.", "dl": " Needs TensorFlow / Keras / PyTorch / XGBoost."}[g["env"]]
        cap += f"{env}  Install: {INSTALL.get(g['id'], 'standard libraries only')}."
    else:
        cap += "  " + ("Libraries: " + ", ".join(g["deps"]) + "." if g["deps"] else "No extra libraries.")
    fl.append(Paragraph(bc.esc(cap), bc.CAPS))
    cw = bc.chars(0.64)
    rows = []
    for i, r in enumerate(g["rows"], 1):
        task, code = r[0], r[1]
        flag = r[2] if len(r) > 2 else ""
        t = fmt(task)
        if flag == "skip":
            t += f"<br/><font size='6.6' color='#9a5b00'><i>({SKIP_REASON.get(task, 'not run')})</i></font>"
        cell_lang = None if flag == "repl" else lang
        rows.append([Paragraph(str(i), S["cell"]), Paragraph(t, S["cell"]), bc.code_cell(code, cell_lang, cw)])
    fl.append(bc.table(["T.No", "Task Desc", "Program code"], rows, [0.07, 0.29, 0.64]))
    fl.append(Spacer(1, 4))
    if g.get("note"):
        fl.append(bc.callout("note", g["note"]))
    return fl


def coverage_page():
    fl = [PageBreak(), Heading("How the syllabus was read", S["h1"], 0)]
    name, missing = syl.check_against_pdf()
    n_topics = sum(len(t) for *_, t in syl.MODULES)
    fl.append(Paragraph(
        f"The topics below are the phrases of the syllabus PDF (<i>{bc.esc(name)}</i>), module by module. A script checked that all {n_topics} topic phrases and all "
        f"{len(syl.EXPERIMENTS)} experiment titles occur in the text of that PDF ({'none missing' if not missing else 'MISSING: ' + ', '.join(missing)}). "
        "The lab-based cheat sheet covers what the 20 indicative experiments ask for. Everything else that the syllabus names has code in this file.", S["body"]))
    for num, title, hours, topics in syl.MODULES:
        fl.append(CondPageBreak(6 * 28))
        fl.append(Heading(f"Module {num}: {title} ({hours} hours)", H2_FREE, 1))
        rows = []
        for phrase, status, where in topics:
            color, label = STATUS_STYLE[status]
            rows.append([Paragraph(bc.esc(phrase), S["cell"]), Paragraph(f"<font color='{color}'><b>{label}</b></font>", S["cell"]),
                         Paragraph(bc.esc(where_text(status, where)), S["cell"])])
        fl.append(bc.table(["Syllabus topic", "Status", "Where the code is"], rows, [0.34, 0.31, 0.35]))
    fl.append(CondPageBreak(8 * 28))
    fl.append(Heading("The 20 indicative experiments and the cheat-sheet table that solves each", H2_FREE, 1))
    rows = [[Paragraph(n, S["cell"]), Paragraph(bc.esc(title), S["cell"]), Paragraph(f"{g} ({syl.CHEAT[g]})", S["cell"])] for title, n, g in syl.EXPERIMENTS]
    fl.append(bc.table(["No", "Experiment", "Cheat sheet table"], rows, [0.07, 0.55, 0.38]))
    return fl


def caveats(counts):
    fl = [PageBreak(), Heading("What was verified and what was not", S["h1"], 0)]
    fl.append(Heading("Verified by running", S["h2"], 1))
    fl += bc.bullets([
        f"Python: {counts['py_ok']} of {counts['py_rows']} rows were executed in order, group by group, each group in an empty folder ({counts['py_skip']} rows are marked 'not run'). Failures: {counts['py_fail']}.",
        f"Scala: {counts['sc_groups']} programs (one per table) were compiled with Scala 2.13.12 and run (one Spark row is marked 'not run'). Failures: {counts['sc_fail']}. The REPL transcript in 3.4 was fed to the real Scala 2.13 REPL engine and every reply matched.",
        "Rows were checked for running without an error. Printed values were read for the Scala programs and spot-checked for the Python ones, not compared one by one with an expected answer.",
        "Versions: Python 3.10; scipy 1.15.3, nltk 3.10.4, folium 0.20.0, requests 2.34.2, scikit-learn 1.7.2, pandas 2.3.3 (main environment); ChatterBot 1.2.15 with spaCy 3.8.18; Scrapy 2.19.0; "
        "xgboost 3.2.0, torch 2.14.1 (CPU), tensorflow 2.21.0, keras 3.12.4; Spark 3.5.1 on Java 17 with Scala 2.13.12.",
    ])
    fl.append(Heading("Not verified, or only partly", S["h2"], 1))
    fl += bc.bullets([
        "<b>The REST rows</b> ran against a small local server that copies the routes of jsonplaceholder.typicode.com, not against the live site. The displayed code uses the real URL; only the base URL differed during the check.",
        "<b>The Scrapy spider</b> ran on two local HTML files with the same structure as quotes.toscrape.com, so pagination and the pipeline were exercised, but the live site was not contacted.",
        "<b>The NLTK download row</b> was not run (it needs internet); the data was already installed. The terminal commands for a Scrapy project are shown but not run.",
        "<b>Spark</b> ran in local mode on one machine, not on a cluster. The Structured Streaming row is shown but was not run: Spark writes a checkpoint, which needs winutils.exe on Windows. No row makes Spark write files (DataFrame.write was left out because it was not tested). The Java 17 --add-opens options are needed for Spark 3.5 on Java 17.",
        "<b>Group 5.1</b> (language selection) turns the syllabus criteria into a calculation. The 1 to 5 scores are example opinions, not facts. Module 5 and Module 6 are theory in the syllabus.",
        "<b>Lab experiments 1 to 20</b> are not repeated here; they are in the cheat sheet. Debug and fill-in-the-blank questions were not written for these extra topics.",
        "Error texts and printed numbers can differ a little on other library versions.",
    ])
    return fl


def cover(counts):
    fl = [Spacer(1, 40), Paragraph("MACSE502 Programming for Data Science", S["subtitle"]),
          Paragraph("Syllabus Gap Code", S["title"]),
          Paragraph("Code for the syllabus topics that the lab-based cheat sheet does not cover, in the same task-table format (T.No | Task Desc | Program code).", S["subtitle"])]
    facts = [
        ["Module 1", f"Python: conditions, data structures, stack / queue / priority queue, strings, exceptions, OOP, files, REST APIs, NLTK, ChatterBot"],
        ["Module 2", "pandas Series and data operations, text data, merging, SciPy, Scrapy, scikit-learn, XGBoost, Keras, TensorFlow, PyTorch, Folium, more plots"],
        ["Module 3", "Scala: functions, variables, strings, numbers, operators, input, HashSet, REPL, classes, objects, traits, inheritance"],
        ["Module 4", "Scala exceptions; Apache Spark (RDD, DataFrame, SQL, MLlib, streaming, GraphX)"],
        ["Module 5", "Language selection criteria as a weighted scoring matrix"],
        ["Size", f"{counts['groups']} tables, {counts['rows']} rows ({counts['py_groups']} Python tables, {counts['sc_groups']} Scala tables)"],
    ]
    t = Table([[Paragraph(f"<b>{a}</b>", S["body"]), Paragraph(bc.esc(b), S["body"])] for a, b in facts], colWidths=[0.14 * TEXT_W, 0.86 * TEXT_W])
    t.setStyle(TableStyle([("LINEBELOW", (0, 0), (-1, -1), 0.4, RULE), ("VALIGN", (0, 0), (-1, -1), "TOP"), ("BACKGROUND", (0, 0), (0, -1), LIGHT)]))
    fl += [t, Spacer(1, 10),
           bc.callout("warn", "Every row was run, except the few marked 'not run' in the tables and listed on the last page. "
                              "The network examples were checked against local stand-ins, not the live sites.")]
    return fl


def main():
    py = {g["id"]: g for g in gap_py.GROUPS}
    sc = {g["id"]: g for g in gap_scala.SGROUPS}
    counts = dict(
        py_rows=len(PY_RES), py_ok=sum(r["status"] == "ok" for r in PY_RES), py_skip=sum(r["status"] == "skip" for r in PY_RES),
        py_fail=sum(r["status"] == "FAIL" for r in PY_RES), sc_groups=len(SC_RES), sc_fail=sum(not r["ok"] for r in SC_RES),
        py_groups=len(py), groups=len(py) + len(sc), rows=sum(len(g["rows"]) for g in py.values()) + sum(len(g["rows"]) for g in sc.values()))
    assert counts["py_fail"] == 0 and counts["sc_fail"] == 0, "run the verifiers first: failures present"
    assert counts["py_rows"] == sum(len(g["rows"]) for g in py.values()), "gap_py_results.json is out of date"
    assert counts["sc_groups"] == len(sc), "gap_scala_results.json is out of date"
    story = cover(counts) + [PageBreak(), Heading("Contents", S["h1"], 0, toc=False), make_toc()] + coverage_page()
    modules = {1: ("Module 1: Python Data Structures (8 hours)", "python"), 2: ("Module 2: Python Libraries (9 hours)", "python"),
               3: ("Module 3: Scala Data Structures and Object-Oriented Programming (12 hours)", "scala"),
               4: ("Module 4: Scala Libraries and Spark Basics (8 hours)", "scala"), 5: ("Module 5: Programming language selection criteria (6 hours)", "python")}
    for num, (title, lang) in modules.items():
        story += [PageBreak(), Heading(title, S["h1"], 0)]
        groups = py if lang == "python" else sc
        for gid, g in groups.items():
            if gid.startswith(f"{num}."):
                story += group_flow(g, lang)
    story += caveats(counts)
    doc = Doc(str(PDF), title="MACSE502 Programming for Data Science: Syllabus Gap Code", footer=FOOTER)
    doc.multiBuild(story)
    print("pages:", doc.page, "->", PDF)
    print(counts)


if __name__ == "__main__":
    main()
