"""Tiny content DSL: every helper returns a plain dict ("block") that render.py turns into flowables."""


def P(text):                     # paragraph (reportlab inline markup allowed: <b>, <i>, <font>, <link>)
    return {"t": "p", "text": text}


def B(items):                    # bullet list
    return {"t": "bul", "items": items}


def N(items):                    # numbered list
    return {"t": "num", "items": items}


def T(header, rows, widths=None):   # table; widths are fractions of the text width
    return {"t": "table", "header": header, "rows": rows, "widths": widths}


def CODE(file, caption=None, transform=None, maxlines=None):
    return {"t": "code", "file": file, "caption": caption, "transform": transform, "maxlines": maxlines}


def OUT(file, caption="Output", transform=None, maxlines=None):
    return {"t": "out", "file": file, "caption": caption, "transform": transform, "maxlines": maxlines}


def SNIP(text, lang="python", caption=None):     # inline snippet (not from a file)
    return {"t": "snip", "text": text, "lang": lang, "caption": caption}


def TIP(text):
    return {"t": "callout", "kind": "tip", "text": text}


def NOTE(text):
    return {"t": "callout", "kind": "note", "text": text}


def WARN(text):
    return {"t": "callout", "kind": "warn", "text": text}


def MARKS(text):
    return {"t": "callout", "kind": "marks", "text": text}


def H3(text):
    return {"t": "h3", "text": text}


def H4(text):
    return {"t": "h4", "text": text}


def IMG(path, width_cm=15, caption=None):
    return {"t": "img", "path": path, "width_cm": width_cm, "caption": caption}


def FLOW(labels, caption=None):          # horizontal flow diagram of boxes
    return {"t": "flow", "labels": labels, "caption": caption}


def DIAGRAM(name, caption=None):         # named custom drawing
    return {"t": "diagram", "name": name, "caption": caption}


def SP(h=6):
    return {"t": "sp", "h": h}


def PB():
    return {"t": "pb"}


# ---- question types -------------------------------------------------------
def MCQ(q, opts, ans, why):
    """ans is the index (0-3) of the correct option."""
    return {"q": q, "opts": opts, "ans": ans, "why": why}


def SHORT(q, marks, answer):
    """answer is a list of blocks (or a string)."""
    if isinstance(answer, str):
        answer = [P(answer)]
    return {"q": q, "marks": marks, "answer": answer}


def LONG(title, marks, prompt, answer, split=None):
    return {"title": title, "marks": marks, "prompt": prompt, "answer": answer, "split": split}


def MODULE(num, title, hours, topics, intro, mcqs, shorts, longs, exam_notes=None):
    return {"num": num, "title": title, "hours": hours, "topics": topics, "intro": intro,
            "mcqs": mcqs, "shorts": shorts, "longs": longs, "exam_notes": exam_notes or []}


# ---- notes-specific blocks ------------------------------------------------
def QA(q, answer, tag=None):
    """Sample question with its answer. `tag` is a short label such as '2 marks' or 'tricky'."""
    if isinstance(answer, str):
        answer = [P(answer)]
    return {"t": "qa", "q": q, "answer": answer, "tag": tag, "label": ""}


def TRICKY(text):
    return {"t": "callout", "kind": "tricky", "text": text}


def KEY(text):
    return {"t": "callout", "kind": "key", "text": text}


def SUB(sid, title, blocks):
    return {"id": sid, "title": title, "blocks": blocks}


def NMODULE(num, title, hours, topics, topic_map, subs):
    """topic_map: list of (syllabus phrase, section ids)."""
    return {"num": num, "title": title, "hours": hours, "topics": topics, "map": topic_map, "subs": subs}
