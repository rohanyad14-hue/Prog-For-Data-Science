"""Assemble each Scala group of cheat_scala.py into one program, compile and run it with scala-cli.
usage: python verify_scala.py [group ids...]
"""
import os
import subprocess
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, os.path.dirname(__file__))
from cheat_scala import SGROUPS

CLI = str(Path(os.environ["TEMP"]) / "pds" / "scala" / "scala-cli.exe")
want = set(sys.argv[1:])
work = Path(tempfile.mkdtemp(prefix="cheat_scala_"))
results = {}


def indent(code, n):
    return "\n".join((" " * n + l) if l.strip() else l for l in code.split("\n"))


for g in SGROUPS:
    if want and g["id"] not in want:
        continue
    imports = [r[1] for r in g["rows"] if len(r) > 2 and r[2] == "import"]
    tops = [r[1] for r in g["rows"] if len(r) > 2 and r[2] == "top"]
    # a 4th element, when present, is the variant that is compiled (e.g. headless) instead of the displayed code
    body = [(r[3] if len(r) > 3 else r[1]) for r in g["rows"] if len(r) < 3 or r[2] == ""]
    header = ["//> using scala 2.13.12"] + [f"//> using dep {d}" for d in g["deps"]]
    src = "\n".join(header + imports + tops) + "\nobject Experiment {\n  def main(args: Array[String]): Unit = {\n" + \
        "\n".join(indent(b, 4) for b in body) + "\n  }\n}\n"
    f = work / f"{g['id']}.scala"
    f.write_bytes(src.encode("utf-8"))  # no BOM
    try:
        res = subprocess.run([CLI, "run", str(f), "--scala", "2.13.12"], cwd=work, capture_output=True, text=True,
                             encoding="utf-8", errors="replace", timeout=int(os.environ.get("GROUP_TIMEOUT", "400")), stdin=subprocess.DEVNULL)
    except subprocess.TimeoutExpired as e:
        print(f"===== {g['id']} TIMEOUT"); print((e.stdout or b"")[-1500:] if isinstance(e.stdout, (bytes, str)) else "")
        results[g["id"]] = False
        continue
    ok = res.returncode == 0
    results[g["id"]] = ok
    print(f"===== {g['id']} {g['title']}: {'OK' if ok else 'FAILED'}")
    if ok:
        print("\n".join(res.stdout.split("\n")[:12]))
    else:
        errs = [l for l in (res.stdout + res.stderr).split("\n") if "[error]" in l or "Exception" in l]
        print("\n".join(errs[:25]))
print("\nsummary:", results)
print("work dir:", work)
