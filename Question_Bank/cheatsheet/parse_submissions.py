"""Parse the ten lab-record PDFs (Prac/Submitions) into one JSON file of programs:
number, type, title, problem statement, code, and the observations text.
usage: python parse_submissions.py
"""
import json
import re
import sys
from pathlib import Path

import fitz

SUBS = Path(r"c:\Users\Rohan\Desktop\vit\SEM 1\Prog For Data Science\Prac\Submitions")
OUT = Path(__file__).parent / "programs.json"

HDR = re.compile(r"2026 FALL SEMESTER\s*\nProgramming for Data Science \(MACSE502\) Lab Record\s*\nPractice Program/ Exercise Program\s*\n"
                 r"Date:[^\n]*\nWeek No\.:[^\n]*\nProgram S\. No\.:\s*(\d+)\s*\nStudent Reg\. No:[^\n]*\nName:[^\n]*\nFaculty:[^\n]*\n\d+ \| P a g e\s*\n")
IDX_HDR = re.compile(r"2026 FALL SEMESTER\s*\nProgramming for Data Science Lab \(MACSE502\) Record\s*\nINDEX\s*\n.*?Pag\s*\ne\s*\nNo\.\s*\n", re.S)


def text_of(n):
    d = fitz.open(SUBS / f"Programming for Data Science Submission {n}.pdf")
    return "\n".join(p.get_text() for p in d).replace("\r", "")


def parse_one(t, sl):
    """Return dict for program number sl from a full document text, or None."""
    t = HDR.sub("", t)
    m = re.search(rf"\nProgram S\. No\.:\s*{sl}\s*\n", t)       # normally removed; fall back to title search below
    return t


def split_programs(t):
    """Split a cleaned document into chunks, one per 'Title' ... 'References' record."""
    t = HDR.sub("", t)
    parts = re.split(r"\nTitle\s*\n", t)
    return parts[1:]


def clean_code(code):
    lines = [l.rstrip() for l in code.split("\n")]
    # PDF wraps long lines; a wrapped continuation starts without indentation after a line that ends mid-expression.
    return "\n".join(lines).strip("\n")


def main():
    programs = {}
    for n in range(1, 11):
        t = text_of(n)
        for chunk in split_programs(t):
            title = chunk.split("\n", 1)[0].strip()
            m_ps = re.search(r"Problem\s*\n?\s*Statement\s*\n(.*?)\nObjectives", chunk, re.S)
            m_code = re.search(r"\nProgram\s*\n(.*?)\nOutput\s*\n?\s*Snapshots", chunk, re.S)
            m_obs = re.search(r"Explanation/\s*\nObservations\s*\n(.*?)\nConclusions", chunk, re.S)
            m_fn = re.search(r"Functions\s*\nDetails\s*\n(.*?)\nSteps/", chunk, re.S)
            m_steps = re.search(r"Algorithm/\s*\nFlowchart/\s*\nModel\s*\n(.*?)\nProgram\s*\n", chunk, re.S)
            m_no = re.search(r"//\s*Program\s*(\d+)|#\s*Program\s*(\d+)|Program\s*(\d+)\s*:", chunk)
            programs.setdefault(n, []).append({
                "submission": n, "title": title,
                "number_hint": next((g for g in (m_no.groups() if m_no else ()) if g), None),
                "problem": (m_ps.group(1).strip() if m_ps else ""),
                "functions": (m_fn.group(1).strip() if m_fn else ""),
                "steps": (m_steps.group(1).strip() if m_steps else ""),
                "code": clean_code(m_code.group(1)) if m_code else "",
                "observations": (m_obs.group(1).strip() if m_obs else ""),
            })
    OUT.write_text(json.dumps(programs, indent=1, ensure_ascii=False), encoding="utf-8")
    total = sum(len(v) for v in programs.values())
    print("records:", total)
    for n, lst in programs.items():
        print(n, [(p["number_hint"], p["title"][:42], len(p["code"])) for p in lst])


if __name__ == "__main__":
    main()
