"""Rendering of the topic-notes document (sections made of notes + sample questions)."""
from reportlab.platypus import PageBreak, Paragraph, Spacer

from render import S, Heading, fmt, render_blocks, table_flowable


def count_questions(mods):
    n = t = 0
    for m in mods:
        for s in m["subs"]:
            for b in s["blocks"]:
                if b["t"] == "qa":
                    n += 1
                    t += 1 if b.get("tag") and "tricky" in b["tag"] else 0
    return n, t


def assign_labels(mods):
    for m in mods:
        for s in m["subs"]:
            k = 0
            for b in s["blocks"]:
                if b["t"] == "qa":
                    k += 1
                    b["label"] = f"{s['id']}-Q{k}"


def render_notes_module(m, code_dir, out_dir):
    fl = [PageBreak(), Heading(f"Module {m['num']}: {m['title']}", S["h1"], 0)]
    fl.append(Paragraph(f"<b>Syllabus ({m['hours']}):</b> " + fmt(m["topics"]), S["body"]))
    fl.append(Paragraph("Where each syllabus topic is covered", S["h3"]))
    fl += table_flowable(["Syllabus topic", "Section"], [[a, b] for a, b in m["map"]], [0.75, 0.25])
    for s in m["subs"]:
        fl.append(Heading(f"{s['id']}  {s['title']}", S["h2"], 1))
        fl += render_blocks(s["blocks"], code_dir, out_dir)
    return fl
