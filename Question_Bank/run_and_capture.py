"""Run a code file from Question_Bank/code and store its console output (UTF-8)
in Question_Bank/outputs/<name>.out.txt so the PDF builder can embed real output.

usage: python run_and_capture.py <file> [--py PATH_TO_PYTHON]
"""
import os
import shutil
import subprocess
import sys
from pathlib import Path

root = Path(__file__).parent
code_dir, out_dir = root / "code", root / "outputs"
out_dir.mkdir(exist_ok=True)
shutil.copy(code_dir / "students.csv", out_dir / "students.csv")

args = sys.argv[1:]
py = sys.executable
if "--py" in args:
    i = args.index("--py")
    py = args[i + 1]
    del args[i:i + 2]
name = args[0]
env = dict(os.environ, PYTHONIOENCODING="utf-8", PYTHONUTF8="1")
if "NLTK_DATA" not in env:
    env["NLTK_DATA"] = str(Path(os.environ["TEMP"]) / "pds" / "nltk_data")

if name.endswith(".py"):
    cmd = [py, str(code_dir / name)]
else:  # scala via scala-cli, extra args passed through
    cli = str(Path(os.environ["TEMP"]) / "pds" / "scala" / "scala-cli.exe")
    cmd = [cli, "run", str(code_dir / name)] + args[1:]

res = subprocess.run(cmd, cwd=out_dir, env=env, capture_output=True, text=True,
                     encoding="utf-8", errors="replace")
stdout = res.stdout
(out_dir / (Path(name).stem + ".out.txt")).write_text(stdout, encoding="utf-8")
print(stdout)
if res.returncode != 0:
    print("---- STDERR (exit", res.returncode, ") ----")
    print(res.stderr[-3000:])
