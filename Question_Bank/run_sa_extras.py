"""Two helpers for the sample-answers document (run_and_capture.py handles the ordinary programs).

  python run_sa_extras.py errors  sa_m3_q2_final_error.scala ...   compile files that are MEANT to fail, store the compiler messages
  python run_sa_extras.py repl    sa_m3_q5_repl.txt ...            feed the lines of a .txt file to the real Scala 2.13 REPL, store a transcript

Results go to outputs/<name>.out.txt (UTF-8).
"""
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

root = Path(__file__).parent
code_dir, out_dir = root / "code", root / "outputs"
CLI = str(Path(os.environ["TEMP"]) / "pds" / "scala" / "scala-cli.exe")
ansi = lambda s: re.sub(r"\x1b\[[0-9;?]*[A-Za-z]", "", s)  # noqa: E731
LOC = re.compile(r"\.scala:\d+:\d+\s*$")
CARET = re.compile(r"^\s*\^+\s*$")


def compiler_messages(text, filename):
    """Every compiler error as 'file:line:col' + its message lines (the echoed source line is dropped)."""
    lines = [re.sub(r"^\[error\]\s?", "", l.rstrip()) for l in text.splitlines() if l.startswith("[error]")]
    out, i = [], 0
    while i < len(lines):
        if LOC.search(lines[i].strip()):
            pos = re.search(r"(\d+):(\d+)\s*$", lines[i]).groups()
            block, i = [], i + 1
            while i < len(lines) and not LOC.search(lines[i].strip()):
                block.append(lines[i])
                i += 1
            for j, l in enumerate(block):
                if CARET.match(l):
                    block = block[:max(j - 1, 1)]
                    break
            out.append(f"{filename}:{pos[0]}:{pos[1]}\n" + "\n".join("  " + b.strip() for b in block if b.strip()))
        else:
            i += 1
    return "\n".join(out)


def errors(names):
    for name in names:
        r = subprocess.run([CLI, "compile", str(code_dir / name), "--scala", "2.13.12"], capture_output=True, text=True,
                           encoding="utf-8", errors="replace", stdin=subprocess.DEVNULL, timeout=600)
        text = ansi(r.stdout + "\n" + r.stderr)
        msg = compiler_messages(text, name)
        status = "compilation FAILED (as intended)" if r.returncode != 0 else "UNEXPECTED: it compiled"
        (out_dir / (Path(name).stem + ".out.txt")).write_text(f"{status}\n{msg}\n", encoding="utf-8")
        print(name, status, "|", len(msg.splitlines()), "message lines")


REPL_SRC = """//> using scala 2.13.12
//> using dep org.scala-lang:scala-compiler:2.13.12
import scala.tools.nsc.Settings
import scala.tools.nsc.interpreter.shell.{ILoop, ShellConfig}
import java.io.{BufferedReader, PrintWriter, StringReader, StringWriter}
import java.nio.file.{Files, Paths}

object ReplRun {
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


def repl(names):
    for name in names:
        typed = [l.rstrip("\n") for l in (code_dir / name).read_text(encoding="utf-8").splitlines() if l.strip()]
        work = Path(tempfile.mkdtemp(prefix="sa_repl_"))
        (work / "repl_input.txt").write_bytes(("\n".join(typed) + "\n:quit\n").encode("utf-8"))
        (work / "ReplRun.scala").write_bytes(REPL_SRC.encode("utf-8"))
        r = subprocess.run([CLI, "run", str(work / "ReplRun.scala"), "--scala", "2.13.12"], cwd=work, capture_output=True, text=True,
                           encoding="utf-8", errors="replace", stdin=subprocess.DEVNULL, timeout=600)
        replies = [re.sub(r"^scala> ?", "", l).rstrip() for l in ansi(r.stdout).splitlines() if l.startswith("scala>")]
        transcript = []
        for k, line in enumerate(typed):
            transcript.append("scala> " + line)
            if k < len(replies) and replies[k]:
                transcript.append(replies[k])
        (out_dir / (Path(name).stem + ".out.txt")).write_text("\n".join(transcript) + "\n", encoding="utf-8")
        print(name, "rc", r.returncode, "|", len(typed), "inputs,", sum(1 for x in replies[:len(typed)] if x), "replies")


if __name__ == "__main__":
    mode, files = sys.argv[1], sys.argv[2:]
    {"errors": errors, "repl": repl}[mode](files)
