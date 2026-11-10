"""Assemble the question bank PDF.  usage: python build_pdf.py [module numbers...]"""
import importlib
import sys
from pathlib import Path

from reportlab.platypus import PageBreak, Paragraph, Spacer

import render
from render import S, Heading, Doc, fmt, render_blocks

ROOT = Path(__file__).parent
CODE_DIR, OUT_DIR = ROOT / "code", ROOT / "outputs"
PDF = ROOT / "MACSE502_Question_Bank_with_Answers.pdf"


def load_modules(only=None):
    mods = []
    for n in range(1, 7):
        if only and n not in only:
            continue
        try:
            m = importlib.import_module(f"content_m{n}")
        except ModuleNotFoundError as e:
            if e.name == f"content_m{n}":
                continue
            raise
        mods.append(getattr(m, f"MODULE_{n}"))
    return mods


def build(only=None):
    mods = load_modules(only)
    story = []
    try:
        import front
        story += front.front_matter(mods, CODE_DIR, OUT_DIR)
    except ModuleNotFoundError as e:
        if e.name != "front":
            raise
        story += [Paragraph("MACSE502 Question Bank (draft)", S["title"])]
    toc = render.make_toc()
    story += [Heading("Contents", S["h1"], 0, toc=False), toc]
    for m in mods:
        story += render.render_module(m, CODE_DIR, OUT_DIR)
    try:
        import back
        story += back.back_matter(mods, CODE_DIR, OUT_DIR)
    except ModuleNotFoundError as e:
        if e.name != "back":
            raise
    doc = Doc(str(PDF))
    doc.multiBuild(story)
    return doc.page


if __name__ == "__main__":
    only = [int(a) for a in sys.argv[1:]] or None
    pages = build(only)
    print("built", PDF, pages, "pages")
