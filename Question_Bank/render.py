"""Turns dsl blocks into reportlab flowables and builds the PDF."""
import re
import textwrap
from pathlib import Path

import matplotlib
from pygments import lex
from pygments.lexers import PythonLexer, ScalaLexer
from pygments.token import Token
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib.utils import simpleSplit
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (BaseDocTemplate, CondPageBreak, Flowable, Frame, HRFlowable, Image, KeepTogether,
                                PageBreak, PageTemplate, Paragraph, Spacer, Table, TableStyle, XPreformatted)
from reportlab.platypus.tableofcontents import TableOfContents

ROOT = Path(__file__).parent
FONT_DIR = Path(matplotlib.__file__).parent / "mpl-data" / "fonts" / "ttf"
for name, file in [("DV", "DejaVuSans.ttf"), ("DV-B", "DejaVuSans-Bold.ttf"), ("DV-I", "DejaVuSans-Oblique.ttf"),
                   ("DV-BI", "DejaVuSans-BoldOblique.ttf"), ("DVM", "DejaVuSansMono.ttf"),
                   ("DVM-B", "DejaVuSansMono-Bold.ttf"), ("DVM-I", "DejaVuSansMono-Oblique.ttf"),
                   ("DVM-BI", "DejaVuSansMono-BoldOblique.ttf")]:
    pdfmetrics.registerFont(TTFont(name, str(FONT_DIR / file)))
pdfmetrics.registerFontFamily("DV", normal="DV", bold="DV-B", italic="DV-I", boldItalic="DV-BI")
pdfmetrics.registerFontFamily("DVM", normal="DVM", bold="DVM-B", italic="DVM-I", boldItalic="DVM-BI")

W, H = A4
MARGIN = 1.7 * cm
TEXT_W = W - 2 * MARGIN

NAVY = colors.HexColor("#1f3a5f")
BLUE = colors.HexColor("#2f6db5")
LIGHT = colors.HexColor("#eaf1fa")
GREY = colors.HexColor("#f4f5f7")
RULE = colors.HexColor("#c9d3df")

S = {}
S["body"] = ParagraphStyle("body", fontName="DV", fontSize=8.7, leading=12.4, spaceAfter=3.5)
S["small"] = ParagraphStyle("small", parent=S["body"], fontSize=7.7, leading=10.4, spaceAfter=0)
S["cell"] = ParagraphStyle("cell", parent=S["body"], fontSize=7.7, leading=10.2, spaceAfter=0)
S["cellh"] = ParagraphStyle("cellh", parent=S["cell"], fontName="DV-B", textColor=colors.white)
S["bul"] = ParagraphStyle("bul", parent=S["body"], leftIndent=13, bulletIndent=3, spaceAfter=1.8)
S["title"] = ParagraphStyle("title", fontName="DV-B", fontSize=24, leading=29, textColor=NAVY, spaceAfter=6)
S["subtitle"] = ParagraphStyle("subtitle", fontName="DV", fontSize=12, leading=16, textColor=BLUE, spaceAfter=10)
S["h1"] = ParagraphStyle("h1", fontName="DV-B", fontSize=17, leading=21, textColor=NAVY, spaceBefore=4, spaceAfter=6)
S["h2"] = ParagraphStyle("h2", fontName="DV-B", fontSize=12.2, leading=15.5, textColor=BLUE, spaceBefore=9, spaceAfter=4, keepWithNext=1)
S["h3"] = ParagraphStyle("h3", fontName="DV-B", fontSize=9.8, leading=13, textColor=NAVY, spaceBefore=7, spaceAfter=2.5, keepWithNext=1)
S["h4"] = ParagraphStyle("h4", fontName="DV-B", fontSize=8.7, leading=12, textColor=colors.HexColor("#444444"),
                         spaceBefore=4, spaceAfter=1.5, keepWithNext=1)
S["q"] = ParagraphStyle("q", parent=S["body"], fontName="DV-B", spaceBefore=5, spaceAfter=2)
S["opt"] = ParagraphStyle("opt", parent=S["body"], leftIndent=20, spaceAfter=0.8)
S["cap"] = ParagraphStyle("cap", parent=S["body"], fontName="DV-I", fontSize=7.3, leading=9.5, textColor=colors.HexColor("#555555"),
                          spaceBefore=3, spaceAfter=5.5, keepWithNext=1)
S["code"] = ParagraphStyle("code", fontName="DVM", fontSize=6.7, leading=8.4, backColor=colors.HexColor("#f6f8fa"),
                           borderColor=RULE, borderWidth=0.5, borderPadding=(4, 4, 4, 4), leftIndent=4, rightIndent=4,
                           spaceAfter=7, spaceBefore=1)
S["out"] = ParagraphStyle("out", parent=S["code"], backColor=colors.HexColor("#fbf9ef"), borderColor=colors.HexColor("#e2dcb8"))
S["tip"] = ParagraphStyle("tip", parent=S["body"], backColor=colors.HexColor("#eaf6ec"), borderColor=colors.HexColor("#8fc79a"),
                          borderWidth=0.6, borderPadding=4, leftIndent=5, rightIndent=5, spaceBefore=4, spaceAfter=8)
S["note"] = ParagraphStyle("note", parent=S["tip"], backColor=LIGHT, borderColor=colors.HexColor("#8bb0d9"))
S["warn"] = ParagraphStyle("warn", parent=S["tip"], backColor=colors.HexColor("#fdf0e6"), borderColor=colors.HexColor("#e3a46c"))
S["marks"] = ParagraphStyle("marks", parent=S["tip"], backColor=colors.HexColor("#f2eefa"), borderColor=colors.HexColor("#a994d6"))
S["tricky"] = ParagraphStyle("tricky", parent=S["tip"], backColor=colors.HexColor("#fff4e0"), borderColor=colors.HexColor("#e0a030"))
S["key"] = ParagraphStyle("key", parent=S["tip"], backColor=colors.HexColor("#e8f0fb"), borderColor=colors.HexColor("#6f9bd6"))
S["qa_q"] = ParagraphStyle("qa_q", parent=S["body"], fontName="DV-B", backColor=colors.HexColor("#eef3fa"), borderPadding=(3, 3, 3, 3),
                           leftIndent=3, rightIndent=3, spaceBefore=9, spaceAfter=5)
LABELS = {"tip": "<b>Tip.</b> ", "note": "<b>Note.</b> ", "warn": "<b>Watch out.</b> ", "marks": "<b>Suggested marks split.</b> ",
          "tricky": "<b>Tricky.</b> ", "key": "<b>Remember.</b> "}

# ----------------------------------------------------------------------------- text helpers
_TAGS = r"(b|i|u|font|link|br|sub|super|strike)"


def fmt(text):
    """backticks -> monospaced; escape stray & and <."""
    parts = text.split("`")
    out = []
    for i, seg in enumerate(parts):
        if i % 2:
            esc = seg.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
            out.append(f'<font name="DVM" size="7.9" color="#8a1c5c">{esc}</font>')
        else:
            seg = re.sub(r"&(?!amp;|lt;|gt;|#)", "&amp;", seg)
            seg = re.sub(rf"<(?!/?{_TAGS}\b)", "&lt;", seg)
            out.append(seg)
    return "".join(out)


def plain(text):
    return re.sub(r"<[^>]+>", "", text.replace("`", "")).replace("&amp;", "&").replace("&lt;", "<").replace("&gt;", ">")


class Heading(Paragraph):
    def __init__(self, text, style, level, toc=True):
        super().__init__(text, style)
        self.level, self.toc, self.title = level, toc, plain(text)


TOKEN_COLORS = [
    (Token.Comment, "#6a737d", True), (Token.Keyword, "#0033b3", False), (Token.Literal.String, "#067d17", False),
    (Token.Literal.Number, "#1750eb", False), (Token.Name.Decorator, "#9e880d", False),
    (Token.Name.Function, "#00627a", False), (Token.Name.Class, "#00627a", False), (Token.Name.Builtin, "#871094", False),
]


def highlight(code, lang):
    lexer = PythonLexer() if lang == "python" else ScalaLexer() if lang == "scala" else None
    esc = lambda s: s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    if lexer is None:
        return esc(code)
    out = []
    for tt, val in lex(code, lexer):
        v = esc(val)
        for base, color, italic in TOKEN_COLORS:
            if tt in base:
                if "\n" in v:                       # colour each line separately (multi-line strings/comments)
                    v = "\n".join(f'<font color="{color}">{p}</font>' if p else p for p in v.split("\n"))
                else:
                    v = f'<font color="{color}">{v}</font>'
                if italic:
                    v = f"<i>{v}</i>"
                break
        out.append(v)
    return "".join(out)


def wrap_lines(text, width=116):
    lines = []
    for ln in text.expandtabs(4).split("\n"):
        if len(ln) <= width:
            lines.append(ln)
        else:
            indent = len(ln) - len(ln.lstrip())
            lines += textwrap.wrap(ln, width, subsequent_indent=" " * (indent + 4), break_long_words=True,
                                   replace_whitespace=False, drop_whitespace=False) or [ln]
    return "\n".join(lines)


# ----------------------------------------------------------------------------- drawings
class FlowDiagram(Flowable):
    def __init__(self, labels, width=TEXT_W, font=7.4):
        super().__init__()
        n = len(labels)
        self.gap, self.font = 15, font
        self.bw = (width - self.gap * (n - 1)) / n
        self.wrapped = [simpleSplit(l, "DV", font, self.bw - 8) for l in labels]
        lines = max(len(w) for w in self.wrapped)
        self.bh = lines * font * 1.28 + 10
        self.width, self.height = width, self.bh + 4

    def draw(self):
        c = self.canv
        x = 0
        for i, lines in enumerate(self.wrapped):
            c.setFillColor(LIGHT)
            c.setStrokeColor(BLUE)
            c.setLineWidth(0.8)
            c.roundRect(x, 2, self.bw, self.bh, 3, fill=1, stroke=1)
            c.setFillColor(colors.black)
            c.setFont("DV", self.font)
            y = 2 + self.bh / 2 + (len(lines) - 1) * self.font * 0.64 - self.font * 0.33
            for ln in lines:
                c.drawCentredString(x + self.bw / 2, y, ln)
                y -= self.font * 1.28
            if i < len(self.wrapped) - 1:
                ax = x + self.bw
                ay = 2 + self.bh / 2
                c.setStrokeColor(NAVY)
                c.setFillColor(NAVY)
                c.line(ax + 1, ay, ax + self.gap - 4, ay)
                p = c.beginPath()
                p.moveTo(ax + self.gap - 1, ay)
                p.lineTo(ax + self.gap - 6, ay + 2.6)
                p.lineTo(ax + self.gap - 6, ay - 2.6)
                p.close()
                c.drawPath(p, fill=1, stroke=0)
            x += self.bw + self.gap


class SparkArch(Flowable):
    def __init__(self, width=TEXT_W):
        super().__init__()
        self.width, self.height = width, 200

    def box(self, x, y, w, h, title, lines=(), fill=LIGHT, stroke=BLUE):
        c = self.canv
        c.setFillColor(fill)
        c.setStrokeColor(stroke)
        c.setLineWidth(0.9)
        c.roundRect(x, y, w, h, 4, fill=1, stroke=1)
        c.setFillColor(NAVY)
        c.setFont("DV-B", 7.6)
        c.drawCentredString(x + w / 2, y + h - 10, title)
        c.setFillColor(colors.black)
        c.setFont("DV", 6.8)
        yy = y + h - 20
        for ln in lines:
            c.drawCentredString(x + w / 2, yy, ln)
            yy -= 8.4

    def arrow(self, x1, y1, x2, y2, label=None, lx=0, ly=0):
        c = self.canv
        c.setStrokeColor(NAVY)
        c.setFillColor(NAVY)
        c.setLineWidth(0.9)
        c.line(x1, y1, x2, y2)
        import math
        ang = math.atan2(y2 - y1, x2 - x1)
        p = c.beginPath()
        p.moveTo(x2, y2)
        p.lineTo(x2 - 6 * math.cos(ang - 0.4), y2 - 6 * math.sin(ang - 0.4))
        p.lineTo(x2 - 6 * math.cos(ang + 0.4), y2 - 6 * math.sin(ang + 0.4))
        p.close()
        c.drawPath(p, fill=1, stroke=0)
        if label:
            c.setFont("DV-I", 6.6)
            tw = pdfmetrics.stringWidth(label, "DV-I", 6.6)
            cx, cy = (x1 + x2) / 2 + lx, (y1 + y2) / 2 + ly
            c.setFillColor(colors.white)
            c.rect(cx - tw / 2 - 2, cy - 2, tw + 4, 9, fill=1, stroke=0)      # white backing keeps the text legible
            c.setFillColor(colors.HexColor("#333333"))
            c.drawCentredString(cx, cy, label)

    def draw(self):
        W_ = self.width
        green = colors.HexColor("#eaf6ec")
        self.box(0, 112, 175, 82, "Driver program", ["SparkSession / SparkContext", "DAG scheduler: job -> stages",
                                                      "Task scheduler", "(your main() runs here)"])
        self.box(W_ - 175, 130, 175, 64, "Cluster manager", ["Standalone / YARN / Kubernetes", "allocates executors on",
                                                              "worker nodes"], fill=colors.HexColor("#fdf0e6"),
                 stroke=colors.HexColor("#e3a46c"))
        self.arrow(175, 168, W_ - 175, 168, "1. request resources", 0, 4)
        wx = [W_ * 0.02, W_ * 0.36, W_ * 0.70]
        for i, x in enumerate(wx):
            self.box(x, 0, W_ * 0.28, 82, f"Worker node {i + 1}")
            self.box(x + 8, 6, W_ * 0.28 - 16, 52, "Executor (JVM)", ["Task   Task", "cache: partitions of RDDs"],
                     fill=green, stroke=colors.HexColor("#8fc79a"))
        self.arrow(W_ - 100, 130, wx[2] + W_ * 0.14, 83, "2. launch", 22, 2)
        self.arrow(W_ - 120, 130, wx[1] + W_ * 0.14, 83)
        self.arrow(W_ - 140, 130, wx[0] + W_ * 0.14, 83)
        self.arrow(60, 112, wx[0] + W_ * 0.2, 84)
        self.arrow(90, 112, wx[1] + W_ * 0.08, 84, "3. tasks out, results back", -34, -8)
        self.arrow(120, 112, wx[2] + W_ * 0.08, 84)


# ----------------------------------------------------------------------------- doc template
class Doc(BaseDocTemplate):
    def __init__(self, path, title="MACSE502 Programming for Data Science: Question Bank with Answers",
                 footer="MACSE502 Programming for Data Science  |  Question bank with answers", **kw):
        self.footer = footer
        super().__init__(path, pagesize=A4, leftMargin=MARGIN, rightMargin=MARGIN, topMargin=1.6 * cm,
                         bottomMargin=1.7 * cm, title=title, author="Prepared with Kiro", **kw)
        frame = Frame(MARGIN, 1.7 * cm, TEXT_W, H - 3.3 * cm, id="main", leftPadding=0, rightPadding=0,
                      topPadding=0, bottomPadding=0)
        self.addPageTemplates([PageTemplate(id="p", frames=[frame], onPage=self.decorate)])
        self._n = 0

    def decorate(self, canv, doc):
        canv.saveState()
        canv.setStrokeColor(RULE)
        canv.setLineWidth(0.5)
        canv.line(MARGIN, 1.35 * cm, W - MARGIN, 1.35 * cm)
        canv.setFont("DV", 7)
        canv.setFillColor(colors.HexColor("#666666"))
        canv.drawString(MARGIN, 0.95 * cm, self.footer)
        canv.drawRightString(W - MARGIN, 0.95 * cm, f"Page {doc.page}")
        canv.restoreState()

    def afterFlowable(self, fl):
        if isinstance(fl, Heading):
            self._n += 1
            key = f"h{self._n}"
            self.canv.bookmarkPage(key)
            self.canv.addOutlineEntry(fl.title, key, fl.level, closed=fl.level >= 1)
            if fl.toc:
                self.notify("TOCEntry", (fl.level, fl.title, self.page))


# ----------------------------------------------------------------------------- block rendering
def _lang_of(file):
    return "python" if str(file).endswith(".py") else "scala" if str(file).endswith(".scala") else None


def _read(path, transform, maxlines):
    text = Path(path).read_text(encoding="utf-8").rstrip("\n")
    if transform:
        text = transform(text)
    lines = text.split("\n")
    if maxlines and len(lines) > maxlines:
        text = "\n".join(lines[:maxlines] + [f"... ({len(lines) - maxlines} more lines omitted)"])
    return text


def table_flowable(header, rows, widths):
    n = len(header)
    widths = widths or [1 / n] * n
    data = [[Paragraph(fmt(h), S["cellh"]) for h in header]]
    for r in rows:
        data.append([Paragraph(fmt(str(c)), S["cell"]) for c in r])
    t = Table(data, colWidths=[w * TEXT_W for w in widths], repeatRows=1)
    st = [("BACKGROUND", (0, 0), (-1, 0), NAVY), ("GRID", (0, 0), (-1, -1), 0.4, RULE),
          ("VALIGN", (0, 0), (-1, -1), "TOP"), ("LEFTPADDING", (0, 0), (-1, -1), 4), ("RIGHTPADDING", (0, 0), (-1, -1), 4),
          ("TOPPADDING", (0, 0), (-1, -1), 2.6), ("BOTTOMPADDING", (0, 0), (-1, -1), 2.6)]
    for i in range(1, len(data)):
        if i % 2 == 0:
            st.append(("BACKGROUND", (0, i), (-1, i), GREY))
    t.setStyle(TableStyle(st))
    return [t, Spacer(1, 6)]


def render_blocks(blocks, code_dir, out_dir):
    fl = []
    for b in blocks:
        t = b["t"]
        if t == "p":
            fl.append(Paragraph(fmt(b["text"]), S["body"]))
        elif t == "bul":
            fl += [Paragraph(fmt(x), S["bul"], bulletText="\u2022") for x in b["items"]]
            fl.append(Spacer(1, 3))
        elif t == "num":
            fl += [Paragraph(fmt(x), S["bul"], bulletText=f"{i}.") for i, x in enumerate(b["items"], 1)]
            fl.append(Spacer(1, 3))
        elif t == "table":
            fl += table_flowable(b["header"], b["rows"], b["widths"])
        elif t in ("code", "out"):
            base = code_dir if t == "code" else out_dir
            path = base / b["file"]
            text = wrap_lines(_read(path, b["transform"], b["maxlines"]))
            lang = _lang_of(b["file"]) if t == "code" else None
            cap = b["caption"] or (f"code/{b['file']}" if t == "code" else "Output")
            cap_label = f"Code: {cap}" if t == "code" and not b["caption"] else cap
            fl.append(Paragraph(fmt(cap_label), S["cap"]))
            fl.append(XPreformatted(highlight(text, lang), S["code" if t == "code" else "out"]))
        elif t == "snip":
            if b["caption"]:
                fl.append(Paragraph(fmt(b["caption"]), S["cap"]))
            fl.append(XPreformatted(highlight(wrap_lines(b["text"]), b["lang"]), S["code"]))
        elif t == "callout":
            fl.append(Paragraph(LABELS[b["kind"]] + fmt(b["text"]), S[b["kind"]]))
        elif t == "qa":
            b["_n"] = b.get("_n", 0)
            tag = f"  <font color='#b0651a' size='7.5'>[{b['tag']}]</font>" if b.get("tag") else ""
            fl.append(CondPageBreak(3.2 * cm))
            fl.append(Paragraph(f"<font color='#2f6db5'>{b['label']}</font>  " + fmt(b["q"]) + tag, S["qa_q"]))
            fl += render_blocks(b["answer"], code_dir, out_dir)
        elif t == "h3":
            fl.append(Paragraph(fmt(b["text"]), S["h3"]))
        elif t == "h4":
            fl.append(Paragraph(fmt(b["text"]), S["h4"]))
        elif t == "img":
            from PIL import Image as PILImage
            p = (out_dir / b["path"]) if not Path(b["path"]).is_absolute() else Path(b["path"])
            w, h = PILImage.open(p).size
            width = b["width_cm"] * cm
            fl.append(Image(str(p), width=width, height=width * h / w))
            if b["caption"]:
                fl.append(Paragraph(fmt(b["caption"]), S["cap"]))
            fl.append(Spacer(1, 4))
        elif t == "flow":
            fl.append(Spacer(1, 2))
            fl.append(FlowDiagram(b["labels"]))
            if b["caption"]:
                fl.append(Paragraph(fmt(b["caption"]), S["cap"]))
            fl.append(Spacer(1, 5))
        elif t == "diagram":
            fl.append(Spacer(1, 3))
            fl.append(SparkArch())
            if b["caption"]:
                fl.append(Paragraph(fmt(b["caption"]), S["cap"]))
            fl.append(Spacer(1, 5))
        elif t == "sp":
            fl.append(Spacer(1, b["h"]))
        elif t == "pb":
            fl.append(PageBreak())
        else:
            raise ValueError(f"unknown block {t}")
    return fl


def render_module(m, code_dir, out_dir):
    n = m["num"]
    fl = [PageBreak(), Heading(f"Module {n}: {m['title']}", S["h1"], 0)]
    fl.append(Paragraph(f"<b>Syllabus ({m['hours']}):</b> " + fmt(m["topics"]), S["body"]))
    fl += render_blocks(m["intro"], code_dir, out_dir)
    for en in m["exam_notes"]:
        fl += render_blocks([en], code_dir, out_dir)

    # ---- Part 1: questions only
    fl.append(Heading(f"Module {n}: Test yourself (questions only)", S["h2"], 1))
    if m["mcqs"]:
        fl.append(Paragraph(f"A. Multiple choice ({len(m['mcqs'])} questions, 1 mark each)", S["h3"]))
        for i, q in enumerate(m["mcqs"], 1):
            block = [Paragraph(f"M{n}-A{i}. " + fmt(q["q"]), S["q"])]
            for j, o in enumerate(q["opts"]):
                block.append(Paragraph(f"({'abcd'[j]}) " + fmt(o), S["opt"]))
            fl.append(KeepTogether(block))
    if m["shorts"]:
        fl.append(Paragraph("B. Short answers", S["h3"]))
        for i, q in enumerate(m["shorts"], 1):
            fl.append(Paragraph(f"M{n}-B{i}. " + fmt(q["q"]) + f"  <font color='#666666'>[{q['marks']} marks]</font>", S["bul"]))
    if m["longs"]:
        fl.append(Paragraph("C. Long questions", S["h3"]))
        for i, q in enumerate(m["longs"], 1):
            fl.append(CondPageBreak(4 * cm))
            fl.append(Paragraph(f"M{n}-C{i}. {fmt(q['title'])}  <font color='#666666'>[{q['marks']} marks]</font>", S["q"]))
            fl += render_blocks(q["prompt"], code_dir, out_dir)

    # ---- Part 2: answers
    fl.append(PageBreak())
    fl.append(Heading(f"Module {n}: Answers", S["h2"], 1))
    if m["mcqs"]:
        fl.append(Paragraph("A. Multiple-choice key", S["h3"]))
        rows = [[f"M{n}-A{i}", "abcd"[q["ans"]], q["why"]] for i, q in enumerate(m["mcqs"], 1)]
        fl += table_flowable(["No.", "Ans.", "Why"], rows, [0.1, 0.07, 0.83])
    if m["shorts"]:
        fl.append(Paragraph("B. Short answers", S["h3"]))
        for i, q in enumerate(m["shorts"], 1):
            fl.append(CondPageBreak(2.5 * cm))
            fl.append(Paragraph(f"M{n}-B{i}. " + fmt(q["q"]) + f"  <font color='#666666'>[{q['marks']} marks]</font>", S["q"]))
            fl += render_blocks(q["answer"], code_dir, out_dir)
    if m["longs"]:
        fl.append(Paragraph("C. Long answers", S["h3"]))
        for i, q in enumerate(m["longs"], 1):
            fl.append(CondPageBreak(5 * cm))
            fl.append(Heading(f"M{n}-C{i}. {q['title']}  [{q['marks']} marks]", S["h2"], 2))
            fl.append(HRFlowable(width="100%", thickness=0.6, color=RULE, spaceAfter=3))
            fl += render_blocks(q["answer"], code_dir, out_dir)
            if q.get("split"):
                fl += render_blocks([{"t": "callout", "kind": "marks", "text": q["split"]}], code_dir, out_dir)
    return fl


def make_toc():
    toc = TableOfContents()
    toc.levelStyles = [
        ParagraphStyle("t0", fontName="DV-B", fontSize=9, leading=13, leftIndent=0, spaceBefore=4),
        ParagraphStyle("t1", fontName="DV", fontSize=8, leading=11, leftIndent=12),
        ParagraphStyle("t2", fontName="DV", fontSize=7.4, leading=10, leftIndent=24, textColor=colors.HexColor("#444444")),
    ]
    return toc
