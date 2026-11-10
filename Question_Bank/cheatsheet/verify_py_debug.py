"""Run every buggy and fixed snippet of debug_py.py and store the REAL messages in debug_py_results.json.
Run with the venv python:  python verify_py_debug.py
"""
import contextlib
import io
import json
import os
import sys
import tempfile
import warnings

os.environ["MPLBACKEND"] = "Agg"
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from debug_py import PY_BUGS, SETUPS  # noqa: E402

os.chdir(tempfile.mkdtemp(prefix="dbg_py_"))


_saved = {}


def _restore_pyplot():
    """buggy snippets such as `plt.title = 'x'` overwrite module attributes; undo that between runs."""
    mod = sys.modules.get("matplotlib.pyplot")
    if mod is None:
        return
    if not _saved:
        _saved.update(vars(mod))
    for k, v in _saved.items():
        if vars(mod).get(k) is not v:
            setattr(mod, k, v)


def run(setup, code, pre=""):
    """exec setup (+pre) and then the snippet in a fresh namespace. Returns (error, warnings, stdout)."""
    _restore_pyplot()
    ns = {}
    exec(compile(SETUPS[setup] + "\n" + pre, "<setup>", "exec"), ns)
    _restore_pyplot()
    buf = io.StringIO()
    err = None
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        try:
            with contextlib.redirect_stdout(buf):
                exec(compile(code, "<cell>", "exec"), ns)
        except BaseException as e:  # noqa: BLE001  (SyntaxError, SystemExit, ...)
            err = f"{type(e).__name__}: {e}"
    warns = [f"{x.category.__name__}: {x.message}" for x in w]
    return err, warns, buf.getvalue()


results, problems = [], []
for i, b in enumerate(PY_BUGS, 1):
    r = dict(n=i, topic=b["topic"], kind=b["kind"])
    err, warns, out = run(b["setup"], b["buggy"])
    r["buggy_error"], r["buggy_warnings"], r["buggy_out"] = err, warns, out
    # does the buggy snippet behave as declared?
    if b["kind"] == "error":
        ok = err is not None and b["contains"] in err
    elif b["kind"] == "warn":
        ok = err is None and any(b["contains"] in x for x in warns)
    else:
        ok = err is None and b["contains"] in out
    r["buggy_ok"] = ok
    if not ok:
        problems.append((i, "buggy", b["buggy"].splitlines()[0], err, warns, out[:200]))
    if b["nofix"]:
        r["fixed_checked"] = False
        r["fixed_ok"] = True
        r["fixed_out"] = ""
        r["fixed_error"] = None
    else:
        ferr, fwarns, fout = run(b["setup"], b["fixed"], b["fixed_pre"])
        r["fixed_checked"] = True
        r["fixed_error"], r["fixed_out"] = ferr, fout
        fixed_ok = ferr is None and b["fixed_contains"] in fout
        if b["kind"] == "warn":
            fixed_ok = fixed_ok and not any(b["contains"] in x for x in fwarns)
        r["fixed_ok"] = fixed_ok
        if not fixed_ok:
            problems.append((i, "fixed", b["fixed"].splitlines()[0], ferr, fwarns, fout[:200]))
    results.append(r)

with open(os.path.join(HERE, "debug_py_results.json"), "w", encoding="utf-8") as f:
    json.dump(results, f, indent=1, ensure_ascii=False)

print(f"items: {len(PY_BUGS)}, problems: {len(problems)}")
for p in problems:
    print("----", p)
