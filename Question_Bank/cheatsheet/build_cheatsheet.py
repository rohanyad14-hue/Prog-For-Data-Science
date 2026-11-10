"""Build MACSE502_Coding_Cheat_Sheet.pdf from the verified data files.
Run with the venv python:  python build_cheatsheet.py
"""
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parent))

from reportlab.lib import colors  # noqa: E402
from reportlab.lib.styles import ParagraphStyle  # noqa: E402
from reportlab.platypus import CondPageBreak, PageBreak, Paragraph, Spacer, Table, TableStyle, XPreformatted  # noqa: E402

from render import (GREY, LABELS, LIGHT, NAVY, RULE, TEXT_W, S, Doc, Heading, fmt, highlight, make_toc,  # noqa: E402
                    wrap_lines)

from cheat_fill import FILLS, parse  # noqa: E402
from cheat_index import IMPORTS, INDEX, SCALA_IMPORTS  # noqa: E402
from cheat_py import GROUPS  # noqa: E402
from cheat_scala import SGROUPS  # noqa: E402
from debug_py import PY_BUGS, SETUPS  # noqa: E402
from debug_scala import SCALA_BUGS  # noqa: E402

PDF = HERE / "MACSE502_Coding_Cheat_Sheet.pdf"
FOOTER = "MACSE502 Programming for Data Science  |  CAT-2 coding cheat sheet (parsed from the lab submissions)"

PY_RES = {r["n"]: r for r in json.loads((HERE / "debug_py_results.json").read_text(encoding="utf-8"))}
SC_RES = {r["n"]: r for r in json.loads((HERE / "debug_scala_results.json").read_text(encoding="utf-8"))}
FILL_RES = {r["id"]: r for r in json.loads((HERE / "fill_results.json").read_text(encoding="utf-8"))}

SKIP_REASON = {
    "Fetch a live page (guarded)": "not run: needs internet",
    "Save as PNG (needs kaleido)": "not run: kaleido is not installed here",
    "Vegas line chart (needs the Vegas library)": "not run: no Vegas build for Scala 2.13",
}

# ------------------------------------------------------------------------------------------- styles
CC = ParagraphStyle("cc", fontName="DVM", fontSize=6.5, leading=8.1)
CMSG = ParagraphStyle("cmsg", parent=CC, fontSize=6.4, leading=8, textColor=colors.HexColor("#8b1a1a"))
COUT = ParagraphStyle("cout", parent=CC, fontSize=6.4, leading=8, textColor=colors.HexColor("#5b4a00"))
LBL = ParagraphStyle("lbl", parent=S["cell"], fontName="DV-B", fontSize=6.8, leading=8.4, spaceBefore=2.5, spaceAfter=0.6)
WHY = ParagraphStyle("why", parent=S["cell"], spaceAfter=1.2)
CAPS = ParagraphStyle("caps", parent=S["cap"], keepWithNext=0, spaceBefore=0, spaceAfter=3)
LIST = ParagraphStyle("list", parent=S["code"], fontSize=6.7, leading=8.5)
IDX = ParagraphStyle("idx", parent=S["h4"], keepWithNext=0, spaceBefore=6, spaceAfter=3)


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def chars(frac, size=6.5):
    """how many monospaced characters fit into a table column of the given width fraction"""
    return int((frac * TEXT_W - 9) / (0.602 * size))


def _breakable(line):
    """positions i (cut before line[i]) that are outside quotes and follow ', ' or a space"""
    ok, quote = [], None
    for i, ch in enumerate(line):
        if quote:
            if ch == quote:
                quote = None
        elif ch in "'\"":
            quote = ch
        elif ch in ", " and i + 1 < len(line):
            ok.append(i + 1)
    return ok


def smart_wrap(text, width):
    """Wrap long code lines after a comma or space that is outside a string; continuation lines are indented by 4."""
    out = []
    for ln in text.expandtabs(4).split("\n"):
        indent = len(ln) - len(ln.lstrip())
        first = True
        while len(ln) > width:
            cuts = [c for c in _breakable(ln) if c <= width and len(ln[:c].strip()) > 6]
            cut = max(cuts) if cuts else width
            out.append(ln[:cut].rstrip())
            ln = " " * (indent + 4) + ln[cut:].lstrip()
            first = False
        out.append(ln)
    return "\n".join(out)


def code_cell(code, lang, width):
    return XPreformatted(highlight(smart_wrap(code, width), lang), CC)


def mono(text, style, width, maxlines=None):
    lines = wrap_lines(text, width).split("\n")
    if maxlines and len(lines) > maxlines:
        lines = lines[:maxlines] + ["..."]
    return XPreformatted(esc("\n".join(lines)), style)


def table(header, rows, fracs, zebra=True):
    data = [[Paragraph(h, S["cellh"]) for h in header]] + rows
    t = Table(data, colWidths=[f * TEXT_W for f in fracs], repeatRows=1)
    st = [("BACKGROUND", (0, 0), (-1, 0), NAVY), ("GRID", (0, 0), (-1, -1), 0.4, RULE), ("VALIGN", (0, 0), (-1, -1), "TOP"),
          ("LEFTPADDING", (0, 0), (-1, -1), 4), ("RIGHTPADDING", (0, 0), (-1, -1), 4),
          ("TOPPADDING", (0, 0), (-1, -1), 2.6), ("BOTTOMPADDING", (0, 0), (-1, -1), 2.6)]
    if zebra:
        st += [("BACKGROUND", (0, i), (-1, i), GREY) for i in range(2, len(data), 2)]
    t.setStyle(TableStyle(st))
    return t


def callout(kind, text):
    return Paragraph(LABELS[kind] + fmt(text), S[kind])


def bullets(items):
    return [Paragraph(fmt(x), S["bul"], bulletText="\u2022") for x in items] + [Spacer(1, 3)]


# ------------------------------------------------------------------------------------------- Format 1
def f1_group(g, lang):
    fl = [CondPageBreak(5 * 28), Heading(f"{g['id']}. {g['title']}", S["h2"], 1)]
    n_run = sum(1 for r in g["rows"] if not (len(r) > 2 and r[2] in ("skip", "wrapper")))
    fl.append(Paragraph(f"Lab records: {g['labs']}.  {len(g['rows'])} rows; the rows form one program, executed top to bottom.", CAPS))
    cw = chars(0.64)
    rows = []
    for i, r in enumerate(g["rows"], 1):
        task, code = r[0], r[1]
        flag = r[2] if len(r) > 2 else ""
        t = fmt(task)
        if flag == "skip":
            t += f"<br/><font size='6.6' color='#9a5b00'><i>({SKIP_REASON.get(task, 'not run')})</i></font>"
        rows.append([Paragraph(str(i), S["cell"]), Paragraph(t, S["cell"]), code_cell(code, lang, cw)])
    fl.append(table(["T.No", "Task Desc", "Program code"], rows, [0.07, 0.29, 0.64]))
    fl.append(Spacer(1, 4))
    if g.get("note"):
        fl.append(callout("note", g["note"]))
    return fl, n_run


# ------------------------------------------------------------------------------------------- Format 2
def short_lines(text, n=3, width=70):
    out = []
    for l in text.splitlines():
        if l.strip():
            l = l.rstrip()
            out.append(l if len(l) <= width else l[: width - 1] + "\u2026")
        if len(out) == n:
            break
    return "\n".join(out)


def py_message(err):
    err = re.sub(r"\s*\(<cell>, line \d+\)", "", err)
    lines = [l.rstrip() for l in err.splitlines() if l.strip()]
    keep = []
    for l in lines:
        if "Valid properties" in l:
            break
        keep.append(l)
    if len(keep) > 1 and keep[0].endswith(":"):
        keep = [keep[0] + " " + keep[1].strip()] + keep[2:]
    return "\n".join(keep)


def desc_cell(label, color, msg_flow, topic, why, fixed_code, lang, width, fix_note=""):
    cell = [Paragraph(f"<font color='{color}'>{label}</font>", LBL), msg_flow]
    cell.append(Paragraph((f"<b>{esc(topic)}.</b> " if topic else "") + fmt(why), WHY))
    cell.append(Paragraph("Fix" + (f" <font size='6.4' color='#9a5b00'>{fix_note}</font>" if fix_note else "") + ":", LBL))
    cell.append(code_cell(fixed_code, lang, width))
    return cell


def py_rows(bugs_with_n):
    cw_code, cw_desc = chars(0.325), chars(0.61, 6.4)
    rows = []
    for k, (n, b) in enumerate(bugs_with_n, 1):
        r = PY_RES[n]
        if b["kind"] == "error":
            label, color = "Error raised", "#8b1a1a"
            msg = mono(py_message(r["buggy_error"]), CMSG, cw_desc, maxlines=4)
        elif b["kind"] == "warn":
            label, color = "Runs, but warns", "#9a5b00"
            msg = mono(py_message(r["buggy_warnings"][0]), COUT, cw_desc, maxlines=3)
        else:
            label, color = "No error, wrong result", "#9a5b00"
            text = short_lines(r["buggy_out"], 3, cw_desc)
            if r["buggy_warnings"]:
                text += "\n+ " + r["buggy_warnings"][0].split(":")[0] + " (printed to the console)"
            msg = mono(text, COUT, cw_desc)
        fix_note = "(not run here)" if b["nofix"] else ""
        rows.append([Paragraph(str(k), S["cell"]), code_cell(b["buggy"], "python", cw_code),
                     desc_cell(label, color, msg, "", b["why"], b["fixed"], "python", cw_desc, fix_note)])
    return rows


def scala_rows():
    cw_code, cw_desc = chars(0.325), chars(0.61, 6.4)
    rows = []
    for k, b in enumerate(SCALA_BUGS, 1):
        r = SC_RES[k]
        shown = "\n".join(x for x in [b["imports"], b["top"], b["buggy"]] if x)
        fixed = "\n".join(x for x in [b["imports"], b["top_fixed"] if b["top_fixed"] != b["top"] else "", b["fixed"]] if x)
        if b["kind"] == "compile":
            label, color = "Compile error", "#8b1a1a"
            msg = mono(r["buggy_msg"], CMSG, cw_desc, maxlines=4)
        elif b["kind"] == "runtime":
            label, color = "Compiles, then throws", "#8b1a1a"
            msg = mono(r["buggy_msg"].replace('Exception in thread "main" ', ""), CMSG, cw_desc, maxlines=3)
        else:
            label, color = "No error, wrong result", "#9a5b00"
            msg = mono(short_lines(r["buggy_out"], 3, cw_desc), COUT, cw_desc)
        rows.append([Paragraph(str(k), S["cell"]), code_cell(shown, "scala", cw_code),
                     desc_cell(label, color, msg, b["topic"], b["why"], fixed, "scala", cw_desc)])
    return rows


PY_GROUP_TITLES = {"pd": "pandas", "np": "NumPy", "plt": "Matplotlib and seaborn", "bs": "Beautiful Soup and requests",
                   "px": "Plotly", "bk": "Bokeh", "sk": "scikit-learn: PCA and K-means", "none": "Plain Python"}


def setup_for_display(key):
    keep = [l for l in SETUPS[key].strip().split("\n") if l.strip() and "matplotlib.use" not in l and l.strip() != "import matplotlib"]
    return "\n".join(keep)


def format2():
    fl = [PageBreak(), Heading("Part 2. Debug the program  (S.No | code | description)", S["h1"], 0)]
    fl.append(Paragraph(
        "Each row is a small program with one bug. The description column shows what Python or the Scala compiler really printed, "
        "why it happens and the corrected code. Items marked <b>No error, wrong result</b> are the dangerous ones: nothing crashes, "
        "so you have to spot the mistake by reading the code. Every buggy snippet and every fix was run; the messages are copied from those runs.", S["body"]))
    order = []
    for b in PY_BUGS:
        if b["setup"] not in order:
            order.append(b["setup"])
    letter = 0
    for key in order:
        items = [(n, b) for n, b in enumerate(PY_BUGS, 1) if b["setup"] == key]
        letter += 1
        fl.append(CondPageBreak(7 * 28))
        fl.append(Heading(f"2.{letter}  Python: {PY_GROUP_TITLES[key]}  ({len(items)} items)", S["h2"], 1))
        setup = setup_for_display(key)
        if setup:
            fl.append(Paragraph("Assumed before every item below:", CAPS))
            fl.append(XPreformatted(highlight(wrap_lines(setup, 118), "python"), S["code"]))
        fl.append(table(["S.No", "Code (buggy)", "Description"], py_rows(items), [0.065, 0.325, 0.61], zebra=False))
        fl.append(Spacer(1, 6))
    letter += 1
    fl.append(CondPageBreak(7 * 28))
    fl.append(Heading(f"2.{letter}  Scala  ({len(SCALA_BUGS)} items)", S["h2"], 1))
    fl.append(Paragraph("Each snippet is the body of main() (classes are shown above the statements). Compiled and run with Scala 2.13.12.", CAPS))
    fl.append(table(["S.No", "Code (buggy)", "Description"], scala_rows(), [0.065, 0.325, 0.61], zebra=False))
    return fl


# ------------------------------------------------------------------------------------------- Format 3
def numbered_listing(lines, blank_nos, lang):
    shown = []
    for i, l in enumerate(lines, 1):
        if i in blank_nos:
            indent = len(l) - len(l.lstrip())
            shown.append(" " * indent + "__MISSING__")
        else:
            if len(l) > 112:
                raise ValueError(f"line {i} too long for the listing: {len(l)}")
            shown.append(l)
    hl = highlight("\n".join(shown), lang).split("\n")
    while len(hl) > len(lines) and not re.sub(r"<[^>]+>", "", hl[-1]).strip():  # pygments appends a final newline
        hl.pop()
    assert len(hl) == len(lines), (len(hl), len(lines))
    out = []
    for i, l in enumerate(hl, 1):
        l = re.sub(r'(?:<font color="[^"]+">)?__MISSING__(?:</font>)?',
                   '<font color="#c0392b"><b>________ line %d: missing ________</b></font>' % i, l)
        out.append(f'<font color="#8a8a8a">{i:>2}</font>  {l}')
    return XPreformatted("\n".join(out), LIST)


def format3():
    fl = [PageBreak(), Heading("Part 3. Fill in the missing lines  (Line No | Missing code | Justification)", S["h1"], 0)]
    fl.append(Paragraph(
        "Each program below is complete in the answer table and was run end to end. Cover the answer table, fill the red lines yourself, then check. "
        "A good justification names what the line does <b>and</b> what would go wrong without it (wrong type, wrong axis, no output file).", S["body"]))
    cw = chars(0.45)
    for it in FILLS:
        lines, blanks = parse(it["code"])
        res = FILL_RES[it["id"]]
        assert res["ok"] and res["blank_lines"] == [b[0] for b in blanks]
        fl.append(CondPageBreak(10.5 * 28))
        fl.append(Heading(f"{it['id']}. {it['title']}", S["h2"], 1))
        nos = ", ".join(str(b[0]) for b in blanks)
        fl.append(Paragraph(f"Lab records: {it['labs']}.  <b>Task:</b> {fmt(it['task'])}  <b>Fill lines {nos}.</b>", CAPS))
        fl.append(numbered_listing(lines, {b[0] for b in blanks}, it["lang"]))
        rows = [[Paragraph(str(no), S["cell"]), code_cell(code, it["lang"], cw), Paragraph(fmt(why), S["cell"])] for no, code, why in blanks]
        fl.append(table(["Line No", "Missing code", "Justification"], rows, [0.09, 0.45, 0.46]))
        out = res["output"].strip()
        if out:
            fl.append(Paragraph("Output of the complete program:", CAPS))
            olines = [l for l in out.splitlines() if l.strip()]
            shown = olines[:9] + (["... (output continues)"] if len(olines) > 9 else [])
            fl.append(XPreformatted(esc(wrap_lines("\n".join(shown), 112)), S["out"]))
        fl.append(Spacer(1, 4))
    return fl


# ------------------------------------------------------------------------------------------- reference and front/back matter
def reference():
    fl = [PageBreak(), Heading("Part 4. Reference: Load-package rows and function index", S["h1"], 0)]
    fl.append(Heading("4.1  Load package (the first row of almost every Q1 table)", S["h2"], 1))
    rows = [[Paragraph(fmt(a), S["cell"]), code_cell(b, "python", chars(0.5)), Paragraph(fmt(c), S["cell"])] for a, b, c in IMPORTS]
    fl.append(table(["Library", "Import line", "Install"], rows, [0.24, 0.5, 0.26]))
    fl.append(Spacer(1, 6))
    rows = [[Paragraph(fmt(a), S["cell"]), code_cell(b, "scala", chars(0.36)), code_cell(c, "scala", chars(0.4))] for a, b, c in SCALA_IMPORTS]
    fl.append(table(["Scala library", "Import line", "scala-cli directive"], rows, [0.24, 0.36, 0.4]))
    fl.append(Heading("4.2  Function to package index", S["h2"], 1))
    fl.append(Paragraph("Written by hand from the rows that were executed (the lab PDFs' own function tables could not be extracted cleanly).", CAPS))
    for section, entries in INDEX:
        fl.append(CondPageBreak(4 * 28))
        fl.append(Paragraph(f"<b>{esc(section)}</b>", IDX))
        rows = [[Paragraph(f"<font name='DVM' size='6.8'>{esc(f)}</font>", S["cell"]), Paragraph(fmt(p), S["cell"]), Paragraph(fmt(d), S["cell"])]
                for f, p, d in entries]
        fl.append(table(["Function", "Package", "What it does"], rows, [0.41, 0.17, 0.42]))
        fl.append(Spacer(1, 4))
    return fl


def decoder(counts):
    fl = [PageBreak(), Heading("How the CAT-2 coding questions look", S["h1"], 0)]
    fl.append(Paragraph(
        "This page is my reading of the whiteboard photo in <i>Prac/Submitions</i>. The column names and row numbers are what the photo shows. "
        "The marks are <b>my guess</b>, check them against your own notes.", S["body"]))
    hdr = ["Format", "What the photo shows", "What to write", "Marks (guess)"]
    rows = [
        [Paragraph("<b>1. Task table</b> (Q1)", S["cell"]),
         Paragraph("Columns T.No | Task Desc | Program code. Row 1 is \"Load package\", row 3 is \"Data frame\". Each row has a tick, a running count (1, 2, 3) and \"+1\". "
                   "\"10%\" is circled above Task Desc and \"90%\" above Program code. An \"8\" is written below the table.", S["cell"]),
         Paragraph("One task per row, in workflow order (load, create, inspect, clean, analyse, plot, save). Code is the exact statements for that task.", S["cell"]),
         Paragraph("+1 per row. The 8 may be the total. 10% / 90% may be column widths or the split of each row's marks (describe the task / write the code), I cannot tell.", S["cell"])],
        [Paragraph("<b>2. Debug program</b>", S["cell"]),
         Paragraph("Columns S.No | code | description (the word \"code\" is written under the last heading, so it may mean \"description of the code\"). "
                   "Rows are numbered 1, 2, 4, 5. Row 4 holds a <i>print( )</i> line, row 5 is an empty box, dashes fill the description column. A \"6\" is written below.", S["cell"]),
         Paragraph("Copy the faulty line, then in the description say what is wrong (error message or wrong result) and give the corrected line.", S["cell"]),
         Paragraph("Possibly 6 rows or 6 marks.", S["cell"])],
        [Paragraph("<b>3. Missing code</b> (10 Mks)", S["cell"]),
         Paragraph("Columns Line No | Missing code | Justification (underlined). The listed lines are 5, 6, 17, 25 and 27 (boxes are drawn next to the first four), so the program has at least 27 lines.", S["cell"]),
         Paragraph("The exact missing line for each listed number, plus one sentence on why that line is needed.", S["cell"]),
         Paragraph("5 blanks for 10 marks: perhaps 2 each (code and justification).", S["cell"])],
    ]
    fl.append(table(hdr, rows, [0.14, 0.34, 0.31, 0.21]))
    fl.append(Spacer(1, 8))
    fl.append(Heading("What an answer looks like", S["h2"], 1))
    ex1 = table(["T.No", "Task Desc", "Program code"], [
        [Paragraph("1", S["cell"]), Paragraph("Load package", S["cell"]), code_cell("import pandas as pd", "python", 60)],
        [Paragraph("2", S["cell"]), Paragraph("Data frame", S["cell"]), code_cell("df = pd.DataFrame(data)", "python", 60)]], [0.1, 0.3, 0.6])
    ex2 = table(["S.No", "Code", "Description"], [
        [Paragraph("1", S["cell"]), code_cell("print(df.head)", "python", 30),
         Paragraph("Method not called: prints <font name='DVM'>&lt;bound method ...&gt;</font>. Use <font name='DVM'>df.head()</font>.", S["cell"])]], [0.1, 0.35, 0.55])
    ex3 = table(["Line No", "Missing code", "Justification"], [
        [Paragraph("7", S["cell"]), code_cell("df = pd.DataFrame(data)", "python", 30),
         Paragraph("Turns the dict into a table; later lines use df.", S["cell"])]], [0.12, 0.4, 0.48])
    for e in (ex1, ex2, ex3):
        fl += [e, Spacer(1, 5)]
    fl.append(Heading("How this sheet is organised", S["h2"], 1))
    fl += bullets([
        f"<b>Part 1</b> ({counts['f1_rows']} Python and Scala rows in {len(GROUPS) + len(SGROUPS)} tables): Format 1. A table is one program; the rows are in running order, so you can type them top to bottom.",
        f"<b>Part 2</b> ({counts['bugs']} bugs): Format 2. {counts['bug_err']} stop with an error message, {counts['bug_silent']} run and print a wrong result, {counts['bug_warn']} only warn.",
        f"<b>Part 3</b> ({len(FILLS)} programs, {counts['blanks']} blanked lines): Format 3, with the full program, the justification and the real output.",
        "<b>Part 4</b>: the import line for each library and a function to package index (the 'Function Details' table of every lab record).",
        "<b>Part 5</b>: what was and was not verified. Read it before trusting a number.",
    ])
    return fl


def part1(counts):
    fl = [PageBreak(), Heading("Part 1. Task tables  (T.No | Task Desc | Program code)", S["h1"], 0)]
    fl.append(Paragraph(
        "Python programs 1 to 17 (Parts A to H) and Scala programs 18 to 25 (S1 to S5). Rows are written the way the labs solve the tasks, "
        "but with small inline data so that every table runs without your CSV files. If the exam gives a file, replace the data-creation row with "
        "<font name='DVM'>pd.read_csv('file.csv')</font>.", S["body"]))
    n = 0
    for g in GROUPS:
        f, k = f1_group(g, "python")
        fl += f
        n += len(g["rows"])
    fl.append(PageBreak())
    fl.append(Heading("Scala tables (programs 18 to 25)", S["h2"], 1))
    fl.append(Paragraph("Statements marked as the entry point go inside <font name='DVM'>object Experiment { def main(args: Array[String]): Unit = { ... } }</font>. "
                        "Each table was assembled into one program, compiled with Scala 2.13.12 and run.", CAPS))
    for g in SGROUPS:
        f, k = f1_group(g, "scala")
        fl += f
        n += len(g["rows"])
    counts["f1_rows"] = n
    return fl


def caveats(counts):
    fl = [PageBreak(), Heading("Part 5. What was verified and what was not", S["h1"], 0)]
    fl.append(Heading("Verified by running", S["h2"], 1))
    fl += bullets([
        f"Part 1: {counts['py_rows'] - 2} of the {counts['py_rows']} Python rows were executed group by group in order (the other 2 are marked 'not run'); the 5 Scala tables were compiled and run with scala-cli. Failures: 0.",
        f"Part 2: {len(PY_BUGS)} Python and {len(SCALA_BUGS)} Scala bugs. Each buggy snippet was run to capture the real message, each fix was run too (2 fixes need internet or kaleido, so they are marked 'not run here').",
        f"Part 3: the {len(FILLS)} complete programs ran without error and their output is shown.",
        "Versions used: pandas 2.3.3, NumPy 1.26.4, scikit-learn 1.7.2, Plotly 7.1.0, Bokeh 3.9.2, seaborn 0.13.2, Python 3.10; Scala 2.13.12 on Java 17 with Breeze 2.1.0, Spire 0.18.0, Plotly.Scala 0.8.5. "
        "Error texts change between versions, so yours may be worded a little differently.",
    ])
    fl.append(Heading("Not verified, or only partly", S["h2"], 1))
    fl += bullets([
        "<b>Marks and layout of the three formats</b> come from reading one photo. I do not know your rubric.",
        "<b>The code is rewritten, not copied.</b> The text extracted from the lab PDFs wraps long strings and puts the closing braces of Scala <i>main</i> on the wrong page, so I wrote clean versions of the same tasks and ran them. "
        "I did not diff them against your records line by line.",
        "<b>Datasets:</b> small inline data replaces whatever files or web pages the labs loaded. Outputs of random data depend on the seed and the library version.",
        "<b>Not executed:</b> a live <font name='DVM'>requests.get</font> of a real website, <font name='DVM'>fig.write_image</font> (kaleido is not installed here, I captured the error text only), "
        "Bokeh <font name='DVM'>export_png</font> (needs a browser driver), and <font name='DVM'>show()</font> calls, which I patched so that no browser opened (the figures were built but I did not look at them).",
        "<b>Vegas:</b> programs 23 and 25 of the labs use Vegas, which has no Scala 2.13 build. The Saddle rows were verified with the maintained fork <font name='DVM'>io.github.pityka::saddle-core:4.0.0-M14</font>, "
        "so the API may differ slightly from the original <font name='DVM'>org.scala-saddle</font> your lab used.",
        "<b>Plotly.Scala:</b> <font name='DVM'>Plotly.plot</font> opens a browser by default. It was verified with <font name='DVM'>openInBrowser = false</font>.",
        "<b>Coverage:</b> only lab programs 1 to 25. Spark, regular expressions and the other lecture topics are not in this sheet; see the earlier question bank and topic notes for those.",
        "<b>Function index:</b> hand-written because the function tables in the lab PDFs do not extract cleanly.",
    ])
    return fl


def cover(counts):
    fl = [Spacer(1, 40), Paragraph("MACSE502 Programming for Data Science", S["subtitle"]),
          Paragraph("CAT-2 Coding Cheat Sheet", S["title"]),
          Paragraph("Parsed from your 10 lab submissions (25 programs) and laid out in the three question formats from the whiteboard photo.", S["subtitle"])]
    facts = [
        ["Part 1", f"{counts['f1_rows']} task rows: Python programs 1 to 17, Scala programs 18 to 25"],
        ["Part 2", f"{counts['bugs']} debug items with the real error messages ({len(PY_BUGS)} Python, {len(SCALA_BUGS)} Scala)"],
        ["Part 3", f"{len(FILLS)} fill-in-the-missing-lines programs, {counts['blanks']} blanks with justifications"],
        ["Part 4", "Load-package lines and a function to package index"],
        ["Part 5", "What was verified and what was not"],
    ]
    t = Table([[Paragraph(f"<b>{a}</b>", S["body"]), Paragraph(b, S["body"])] for a, b in facts], colWidths=[0.14 * TEXT_W, 0.86 * TEXT_W])
    t.setStyle(TableStyle([("LINEBELOW", (0, 0), (-1, -1), 0.4, RULE), ("VALIGN", (0, 0), (-1, -1), "TOP"),
                           ("BACKGROUND", (0, 0), (0, -1), LIGHT)]))
    fl += [t, Spacer(1, 10),
           callout("warn", "The marks and the 10% / 90% split in the photo are my interpretation. Every code row, bug and program in this sheet was run; "
                           "the exceptions are listed in Part 5.")]
    return fl


def main():
    counts = {}
    counts["py_rows"] = sum(len(g["rows"]) for g in GROUPS)
    counts["bug_err"] = sum(1 for b in PY_BUGS + SCALA_BUGS if b["kind"] in ("error", "compile", "runtime"))
    counts["bug_silent"] = sum(1 for b in PY_BUGS + SCALA_BUGS if b["kind"] == "silent")
    counts["bug_warn"] = sum(1 for b in PY_BUGS + SCALA_BUGS if b["kind"] == "warn")
    counts["bugs"] = len(PY_BUGS) + len(SCALA_BUGS)
    counts["blanks"] = sum(len(parse(f["code"])[1]) for f in FILLS)
    body1 = part1(counts)  # fills counts['f1_rows']
    story = cover(counts)
    story += [PageBreak(), Heading("Contents", S["h1"], 0, toc=False), make_toc()]
    story += decoder(counts)
    story += body1
    story += format2()
    story += format3()
    story += reference()
    story += caveats(counts)
    doc = Doc(str(PDF), title="MACSE502 Programming for Data Science: CAT-2 Coding Cheat Sheet", footer=FOOTER)
    doc.multiBuild(story)
    print("pages:", doc.page, "->", PDF)
    print(counts)


if __name__ == "__main__":
    main()
