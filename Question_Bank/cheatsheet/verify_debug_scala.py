"""Compile and run every buggy and fixed snippet of debug_scala.py with scala-cli; store real messages in debug_scala_results.json.
usage: python verify_debug_scala.py [item numbers...]     (env DBG_TIMEOUT = seconds per run, default 300)
"""
import json
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from debug_scala import SCALA_BUGS  # noqa: E402

CLI = str(Path(os.environ["TEMP"]) / "pds" / "scala" / "scala-cli.exe")
TIMEOUT = int(os.environ.get("DBG_TIMEOUT", "300"))
work = Path(tempfile.mkdtemp(prefix="dbg_scala_"))
only = {int(a) for a in sys.argv[1:]}

LOC = re.compile(r"\.scala:\d+:\d+\s*$")
CARET = re.compile(r"^\s*\^+\s*$")


def source(b, code, top):
    head = ["//> using scala 2.13.12"] + [f"//> using dep {d}" for d in b["deps"]]
    body = "\n".join(("    " + l) if l.strip() else l for l in code.split("\n"))
    parts = head + ([b["imports"]] if b["imports"] else []) + ([top] if top else [])
    return "\n".join(parts) + "\nobject Experiment {\n  def main(args: Array[String]): Unit = {\n" + body + "\n  }\n}\n"


def run(name, src):
    f = work / f"{name}.scala"
    f.write_bytes(src.encode("utf-8"))  # no BOM
    try:
        r = subprocess.run([CLI, "run", str(f), "--scala", "2.13.12"], cwd=work, capture_output=True, text=True,
                           encoding="utf-8", errors="replace", timeout=TIMEOUT, stdin=subprocess.DEVNULL)
    except subprocess.TimeoutExpired:
        return dict(rc=-1, out="", err="TIMEOUT")
    def strip(s):
        return re.sub(r"\x1b\[[0-9;]*m", "", s)  # scala-cli colours its output
    return dict(rc=r.returncode, out=strip(r.stdout), err=strip(r.stderr))


def compiler_message(text):
    """First compiler error: lines after the location line, up to (not including) the echoed source line."""
    lines = [re.sub(r"^\[error\]\s?", "", l.rstrip()) for l in text.splitlines() if l.startswith("[error]")]
    for i, l in enumerate(lines):
        if LOC.search(l.strip()):
            block = []
            for nxt in lines[i + 1:]:
                if LOC.search(nxt.strip()):
                    break
                block.append(nxt)
            for j, nxt in enumerate(block):
                if CARET.match(nxt):
                    block = block[:max(j - 1, 1)]
                    break
            return "\n".join(x.strip() for x in block if x.strip())
    return "\n".join(lines[:3])


def runtime_message(text):
    for l in text.splitlines():
        if l.startswith("Exception in thread"):
            return l
    return ""


results, problems = [], []
for i, b in enumerate(SCALA_BUGS, 1):
    if only and i not in only:
        continue
    rb = run(f"b{i}", source(b, b["buggy"], b["top"]))
    allout = rb["out"] + "\n" + rb["err"]
    r = dict(n=i, topic=b["topic"], kind=b["kind"])
    if b["kind"] == "compile":
        msg = compiler_message(allout)
        ok = rb["rc"] != 0 and "[error]" in allout and b["contains"] in msg
    elif b["kind"] == "runtime":
        msg = runtime_message(allout)
        ok = rb["rc"] != 0 and b["contains"] in msg
    else:
        msg = rb["out"].strip()
        ok = rb["rc"] == 0 and b["contains"] in rb["out"]
    r["buggy_msg"], r["buggy_out"], r["buggy_ok"] = msg, rb["out"].strip(), ok
    if not ok:
        problems.append((i, "buggy", b["buggy"].splitlines()[0], msg, allout[-600:]))
    rf = run(f"f{i}", source(b, b["fixed"], b["top_fixed"]))
    fok = rf["rc"] == 0 and b["fixed_contains"] in rf["out"]
    r["fixed_out"], r["fixed_ok"] = rf["out"].strip(), fok
    if not fok:
        problems.append((i, "fixed", b["fixed"].splitlines()[0], "", (rf["out"] + rf["err"])[-600:]))
    results.append(r)
    print(f"{i:2d} {b['kind']:8s} buggy {'ok' if ok else 'BAD'}  fixed {'ok' if fok else 'BAD'}  | {msg.splitlines()[0][:90] if msg else ''}", flush=True)

out_name = "debug_scala_results.json" if not only else "debug_scala_results_partial.json"
with open(HERE / out_name, "w", encoding="utf-8") as fh:
    json.dump(results, fh, indent=1, ensure_ascii=False)
print(f"\nitems: {len(results)}, problems: {len(problems)}")
for p in problems:
    print("----", p[:4])
    print(p[4])
print("work dir:", work)
