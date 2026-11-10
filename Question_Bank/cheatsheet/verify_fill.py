"""Run every COMPLETE Format-3 program of cheat_fill.py (Python with the venv interpreter, Scala with scala-cli)
and store the real output in fill_results.json.   usage: python verify_fill.py [F1 F2 ...]
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
from cheat_fill import FILLS, parse  # noqa: E402

CLI = str(Path(os.environ["TEMP"]) / "pds" / "scala" / "scala-cli.exe")
TIMEOUT = int(os.environ.get("FILL_TIMEOUT", "400"))
work = Path(tempfile.mkdtemp(prefix="fill_"))
only = set(sys.argv[1:])
env = dict(os.environ, MPLBACKEND="Agg", PYTHONIOENCODING="utf-8")
ansi = lambda s: re.sub(r"\x1b\[[0-9;]*m", "", s)  # noqa: E731

results, bad = [], 0
for it in FILLS:
    if only and it["id"] not in only:
        continue
    lines, blanks = parse(it["code"])
    program = "\n".join(lines) + "\n"
    if it["lang"] == "python":
        f = work / f"{it['id']}.py"
        f.write_bytes(program.encode("utf-8"))
        cmd = [sys.executable, str(f)]
    else:
        head = ["//> using scala 2.13.12"] + [f"//> using dep {d}" for d in it["deps"]]
        f = work / f"{it['id']}.scala"
        f.write_bytes(("\n".join(head) + "\n" + program).encode("utf-8"))
        cmd = [CLI, "run", str(f), "--scala", "2.13.12"]
    try:
        r = subprocess.run(cmd, cwd=work, env=env, capture_output=True, text=True, encoding="utf-8", errors="replace",
                           timeout=TIMEOUT, stdin=subprocess.DEVNULL)
        rc, out, err = r.returncode, ansi(r.stdout), ansi(r.stderr)
    except subprocess.TimeoutExpired:
        rc, out, err = -1, "", "TIMEOUT"
    ok = rc == 0
    bad += not ok
    results.append(dict(id=it["id"], ok=ok, output=out.rstrip(), n_lines=len(lines), blank_lines=[b[0] for b in blanks],
                        stderr_tail="" if ok else err[-800:]))
    print(f"{it['id']:4s} {'OK ' if ok else 'FAIL'} lines={len(lines)} blanks={[b[0] for b in blanks]}", flush=True)
    if not ok:
        print(err[-800:])
    else:
        print("   " + "\n   ".join(out.rstrip().split("\n")[:8]))

name = "fill_results.json" if not only else "fill_results_partial.json"
(HERE / name).write_text(json.dumps(results, indent=1, ensure_ascii=False), encoding="utf-8")
print(f"\nprograms: {len(results)}, failed: {bad}, work dir: {work}")
