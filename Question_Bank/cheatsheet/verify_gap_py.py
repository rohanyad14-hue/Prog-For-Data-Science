"""Execute every row of gap_py.py (one namespace and one empty working directory per group) and report failures.

  python verify_gap_py.py                 driver: runs every environment with the right virtualenv, writes gap_py_results.json
  python verify_gap_py.py --env main      worker: runs the groups of one environment in THIS interpreter
  python verify_gap_py.py --env main 1.1 1.2      only those groups

Environments (virtualenvs in %TEMP%\\pds):  main = venv, cb = venv_cb (ChatterBot), sc = venv_sc (Scrapy), dl = venv_dl (TensorFlow, Keras, PyTorch, XGBoost)
"""
import io
import json
import linecache
import os
import subprocess
import sys
import tempfile
import time
import traceback
import warnings
from contextlib import redirect_stdout
from pathlib import Path

HERE = Path(__file__).resolve().parent
ENVS = {"main": "venv", "cb": "venv_cb", "sc": "venv_sc", "dl": "venv_dl"}


def driver():
    results, bad = [], 0
    for env, venv in ENVS.items():
        py = Path(os.environ["TEMP"]) / "pds" / venv / "Scripts" / "python.exe"
        envvars = dict(os.environ, PYTHONIOENCODING="utf-8", NLTK_DATA=str(Path(os.environ["TEMP"]) / "pds" / "nltk_data"), TF_CPP_MIN_LOG_LEVEL="3")
        t0 = time.time()
        r = subprocess.run([str(py), str(HERE / "verify_gap_py.py"), "--env", env], capture_output=True, text=True, encoding="utf-8",
                           errors="replace", env=envvars, timeout=2400, stdin=subprocess.DEVNULL, cwd=str(HERE))
        print(f"===== env {env} ({venv}) {time.time() - t0:.0f}s, exit {r.returncode}")
        print(r.stdout.strip()[-2500:])
        if r.returncode != 0:
            print(r.stderr.strip()[-1500:])
        part = HERE / f"gap_py_results_{env}.json"
        if part.exists():
            data = json.loads(part.read_text(encoding="utf-8"))
            results += data
            bad += sum(1 for d in data if d["status"] == "FAIL")
    (HERE / "gap_py_results.json").write_text(json.dumps(results, indent=1, ensure_ascii=False), encoding="utf-8")
    print(f"\nTOTAL rows: {len(results)}, executed ok: {sum(d['status'] == 'ok' for d in results)}, skipped: {sum(d['status'] == 'skip' for d in results)}, FAILED: {bad}")


def worker(env, only):
    warnings.filterwarnings("ignore")
    os.environ["MPLBACKEND"] = "Agg"
    sys.path.insert(0, str(HERE))
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        plt.show = lambda *a, **k: None
    except Exception:
        pass
    from gap_py import GROUPS
    results = []
    for g in GROUPS:
        if g["env"] != env or (only and g["id"] not in only):
            continue
        workdir = tempfile.mkdtemp(prefix=f"gap_{g['id'].replace('.', '_')}_")
        os.chdir(workdir)
        # Scrapy resolves '__main__.CleanPipeline', so that group runs in the module namespace of this script
        ns = vars(sys.modules["__main__"]) if env == "sc" else {"__name__": "__gap__"}
        old_stdin = sys.stdin
        if g["stdin"]:
            sys.stdin = io.StringIO(g["stdin"])
        try:
            if g["setup"]:
                exec(compile(g["setup"], f"<{g['id']}-setup>", "exec"), ns)
            for i, row in enumerate(g["rows"], 1):
                task, shown = row[0], row[1]
                flag = row[2] if len(row) > 2 else ""
                code = row[3] if len(row) > 3 else shown
                rec = dict(group=g["id"], row=i, task=task, status="ok", output="", error="")
                if flag == "skip":
                    rec["status"] = "skip"
                    results.append(rec)
                    continue
                buf = io.StringIO()
                fname = f"<{g['id']}-{i}>"
                linecache.cache[fname] = (len(code), None, code.splitlines(True), fname)   # inspect.getsource() works for exec'd code (Scrapy needs it)
                try:
                    with redirect_stdout(buf):
                        exec(compile(code, fname, "exec"), ns)
                except BaseException as e:  # noqa: BLE001 (SystemExit from a crawler, ...)
                    rec["status"] = "FAIL"
                    rec["error"] = f"{type(e).__name__}: {str(e).splitlines()[0][:200] if str(e) else ''}"
                    traceback.print_exc(limit=2)
                rec["output"] = buf.getvalue()[-900:]
                results.append(rec)
        finally:
            sys.stdin = old_stdin
        print(f"group {g['id']:5s} {g['title'][:60]:60s} rows={len(g['rows'])} failures={sum(r['status'] == 'FAIL' for r in results if r['group'] == g['id'])}", flush=True)
    for r in results:
        if r["status"] == "FAIL":
            print("FAIL", r["group"], r["row"], r["task"], "|", r["error"])
    (HERE / f"gap_py_results_{env}.json").write_text(json.dumps(results, indent=1, ensure_ascii=False), encoding="utf-8")
    print(f"env {env}: rows {len(results)}, ok {sum(r['status'] == 'ok' for r in results)}, skipped {sum(r['status'] == 'skip' for r in results)}, "
          f"FAILED {sum(r['status'] == 'FAIL' for r in results)}")


if __name__ == "__main__":
    args = sys.argv[1:]
    if "--env" in args:
        i = args.index("--env")
        worker(args[i + 1], set(args[i + 2:]))
    else:
        driver()
