"""Execute every Format-1 row of cheat_py.py in order (one namespace per group) and report failures.
Run with the venv that has bokeh / sklearn / plotly / bs4:  python verify_py.py
"""
import io
import os
import sys
import tempfile
import traceback
import warnings
from contextlib import redirect_stdout

warnings.filterwarnings("ignore")
os.environ["MPLBACKEND"] = "Agg"
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.io as pio

plt.show = lambda *a, **k: None                          # never open windows
go.Figure.show = lambda self, *a, **k: None              # never open a browser
pio.show = lambda *a, **k: None
import bokeh.plotting as bp
bp.show = lambda *a, **k: None                           # bokeh show() would open a browser

sys.path.insert(0, os.path.dirname(__file__))
from cheat_py import GROUPS

work = tempfile.mkdtemp(prefix="cheat_")
os.chdir(work)
failures, skipped, ran = [], 0, 0
for g in GROUPS:
    ns = {"__name__": "__cheat__"}
    ns["show"] = lambda *a, **k: None
    for i, row in enumerate(g["rows"], 1):
        task, code = row[0], row[1]
        if len(row) > 2 and row[2] == "skip":
            skipped += 1
            continue
        buf = io.StringIO()
        try:
            with redirect_stdout(buf):
                exec(compile(code, f"<{g['id']}-{i}>", "exec"), ns)
            ran += 1
        except Exception as e:
            failures.append((g["id"], i, task, type(e).__name__, str(e).splitlines()[0][:160]))
            traceback.print_exc(limit=1)
print(f"rows executed: {ran}, skipped (marked skip): {skipped}, failures: {len(failures)}")
for f in failures:
    print("FAIL", f)
