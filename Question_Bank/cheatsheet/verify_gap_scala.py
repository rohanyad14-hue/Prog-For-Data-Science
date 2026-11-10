"""Assemble each group of gap_scala.py into one Scala program, compile and run it with scala-cli, store the results.
usage: python verify_gap_scala.py [group ids...]      (env GAP_TIMEOUT = seconds per group, default 600)
REPL rows ("repl" flag) are checked by feeding the typed lines to the real Scala 2.13 REPL engine (ILoop) and comparing its replies.
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
from gap_scala import SGROUPS  # noqa: E402

CLI = str(Path(os.environ["TEMP"]) / "pds" / "scala" / "scala-cli.exe")
TIMEOUT = int(os.environ.get("GAP_TIMEOUT", "600"))
only = set(sys.argv[1:])
work_root = Path(tempfile.mkdtemp(prefix="gap_scala_"))
ansi = lambda s: re.sub(r"\x1b\[[0-9;?]*[A-Za-z]", "", s)  # noqa: E731


def indent(code, n):
    return "\n".join((" " * n + l) if l.strip() else l for l in code.split("\n"))


def run_cli(src_file, cwd, stdin_text="", timeout=TIMEOUT):
    try:
        r = subprocess.run([CLI, "run", str(src_file), "--scala", "2.13.12"], cwd=cwd, input=stdin_text, capture_output=True, text=True,
                           encoding="utf-8", errors="replace", timeout=timeout)
        return r.returncode, ansi(r.stdout), ansi(r.stderr)
    except subprocess.TimeoutExpired:
        return -1, "", "TIMEOUT"


def compile_errors(text):
    return "\n".join(l for l in text.splitlines() if l.startswith("[error]"))[:2500]


REPL_SRC = """//> using scala 2.13.12
//> using dep org.scala-lang:scala-compiler:2.13.12
import scala.tools.nsc.Settings
import scala.tools.nsc.interpreter.shell.{ILoop, ShellConfig}
import java.io.{BufferedReader, PrintWriter, StringReader, StringWriter}
import java.nio.file.{Files, Paths}

object ReplCheck {
  def main(args: Array[String]): Unit = {
    val input = new String(Files.readAllBytes(Paths.get("repl_input.txt")), "UTF-8")
    val settings = new Settings
    settings.usejavacp.value = true
    val out = new StringWriter
    val repl = new ILoop(ShellConfig(settings), new BufferedReader(new StringReader(input)), new PrintWriter(out))
    repl.run(settings)
    println(out.toString)
  }
}
"""


def check_repl(transcript, workdir):
    """-> (ok, message). Typed lines start with 'scala> '; the lines that follow (up to the next prompt) are the expected reply."""
    typed, expected = [], []
    for line in transcript.splitlines():
        if line.startswith("scala> "):
            typed.append(line[len("scala> "):])
            expected.append([])
        elif line.strip() and expected:
            expected[-1].append(line.strip())
    (workdir / "repl_input.txt").write_bytes(("\n".join(typed) + "\n:quit\n").encode("utf-8"))
    (workdir / "ReplCheck.scala").write_bytes(REPL_SRC.encode("utf-8"))
    rc, out, err = run_cli(workdir / "ReplCheck.scala", workdir, timeout=300)
    if rc != 0:
        return False, "REPL harness failed: " + (err or out)[-400:]
    replies = [re.sub(r"^scala> ?", "", l).strip() for l in out.splitlines() if l.startswith("scala>")]
    actual = [[r] if r else [] for r in replies[:len(typed)]]
    if actual != expected:
        return False, f"REPL replies differ:\nexpected {expected}\nactual   {actual}"
    return True, f"{len(typed)} inputs, replies match"


results, bad = [], 0
for g in SGROUPS:
    if only and g["id"] not in only:
        continue
    rows = g["rows"]
    imports = [r[1] for r in rows if len(r) > 2 and r[2] == "import"]
    tops = [r[1] for r in rows if len(r) > 2 and r[2] == "top"]
    body = [(r[3] if len(r) > 3 else r[1]) for r in rows if len(r) < 3 or r[2] == ""]
    header = ["//> using scala 2.13.12"] + [f"//> using dep {d}" for d in g["deps"]] + g["directives"]
    src = "\n".join(header + imports + tops) + "\nobject Experiment {\n  def main(args: Array[String]): Unit = {\n" + \
        "\n".join(indent(b, 4) for b in body) + "\n  }\n}\n"
    wd = work_root / g["id"].replace(".", "_")
    wd.mkdir()
    f = wd / "Experiment.scala"
    f.write_bytes(src.encode("utf-8"))
    rc, out, err = run_cli(f, wd, g["stdin"])
    ok = rc == 0
    def failure_text():
        ce = compile_errors(out + "\n" + err)
        if ce:
            return ce
        lines = [l for l in err.splitlines() if "Exception in thread" in l or l.startswith("Caused by") or " ERROR " in l]
        return "\n".join(lines[:12]) or err[-1500:]

    rec = dict(group=g["id"], title=g["title"], ok=ok, rows=len(rows), output=out[-8000:], errors="" if ok else failure_text())
    for r in rows:
        if len(r) > 2 and r[2] == "repl":
            rok, msg = check_repl(r[1], wd)
            rec["repl"] = msg
            rec["ok"] = rec["ok"] and rok
            ok = rec["ok"]
    bad += not ok
    results.append(rec)
    print(f"{g['id']:5s} {'OK ' if ok else 'FAIL'} rows={len(rows)}  {g['title'][:70]}", flush=True)
    if not ok:
        print(rec["errors"][:1800])
        if rec.get("repl"):
            print(rec["repl"])

name = "gap_scala_results.json" if not only else "gap_scala_results_partial.json"
(HERE / name).write_text(json.dumps(results, indent=1, ensure_ascii=False), encoding="utf-8")
print(f"\ngroups: {len(results)}, failed: {bad}, work dir: {work_root}")
