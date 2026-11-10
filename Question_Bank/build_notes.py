"""Assemble the topic-notes PDF.  usage: python build_notes.py"""
import importlib
from pathlib import Path

from reportlab.platypus import PageBreak, Paragraph

import render
from render import S, Doc, Heading
from render_notes import assign_labels, count_questions, render_notes_module

ROOT = Path(__file__).parent
CODE_DIR, OUT_DIR = ROOT / "code", ROOT / "outputs"
PDF = ROOT / "MACSE502_Topic_Notes_with_Practice_Questions.pdf"


def build():
    mods = []
    for n in range(1, 7):
        try:
            mods.append(getattr(importlib.import_module(f"notes_m{n}"), f"NOTES_{n}"))
        except ModuleNotFoundError as e:
            if e.name != f"notes_m{n}":
                raise
    assign_labels(mods)
    story = []
    import notes_front
    story += notes_front.front(mods, CODE_DIR, OUT_DIR)
    toc = render.make_toc()
    story += [Heading("Contents", S["h1"], 0, toc=False), toc]
    for m in mods:
        story += render_notes_module(m, CODE_DIR, OUT_DIR)
    try:
        import notes_back
        story += notes_back.back(mods, CODE_DIR, OUT_DIR)
    except ModuleNotFoundError as e:
        if e.name != "notes_back":
            raise
    doc = Doc(str(PDF), title="MACSE502 Programming for Data Science: Topic Notes with Practice Questions",
              footer="MACSE502 Programming for Data Science  |  Topic notes with practice questions")
    doc.multiBuild(story)
    n, t = count_questions(mods)
    return doc.page, n, t


if __name__ == "__main__":
    pages, n, t = build()
    print(f"built {PDF.name}: {pages} pages, {n} questions ({t} tagged tricky)")
