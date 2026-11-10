"""Notes M1: file handling, csv/json, and REST calls against a REAL local HTTP server.
The server runs inside this script on localhost, so every status code below is a genuine HTTP response.
"""
import csv
import json
import os
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlparse

import requests

# =============================================================== files
print("--- file modes ---")
with open("demo.txt", "w", encoding="utf-8") as f:
    f.write("line1\nline2\n")
with open("demo.txt", "a", encoding="utf-8") as f:
    f.write("line3\n")
with open("demo.txt", "w", encoding="utf-8") as f:
    pass
print("'w' truncates: size after reopening with 'w' =", os.path.getsize("demo.txt"))
with open("demo.txt", "w", encoding="utf-8") as f:
    f.write("line1\nline2\nline3\n")
try:
    open("demo.txt", "x")
except FileExistsError as err:
    print("'x' on an existing file ->", type(err).__name__)
try:
    open("missing.txt")
except FileNotFoundError as err:
    print("'r' on a missing file ->", type(err).__name__)

print("\n--- reading styles ---")
with open("demo.txt", encoding="utf-8") as f:
    print("read():", repr(f.read()))
with open("demo.txt", encoding="utf-8") as f:
    print("readline():", repr(f.readline()), "| readlines():", f.readlines())
with open("demo.txt", encoding="utf-8") as f:
    print("iterate:", [ln.rstrip() for ln in f], "(memory friendly for big files)")
with open("demo.txt", "r+", encoding="utf-8") as f:
    f.seek(6)
    print("seek(6) then read(5):", f.read(5), "| tell():", f.tell())
    f.seek(0)
    f.write("LINE1")
    f.seek(0)
    print("'r+' overwrote in place:", f.readline().rstrip())

print("\n--- csv and json ---")
rows = [{"reg": "VL1", "name": "Asha", "marks": "86"}, {"reg": "VL2", "name": "Kabir, S", "marks": "58"}]
with open("s.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=["reg", "name", "marks"])
    w.writeheader()
    w.writerows(rows)
print(open("s.csv", encoding="utf-8").read().strip())
with open("s.csv", newline="", encoding="utf-8") as f:
    back = list(csv.DictReader(f))
print("csv returns strings:", back[1], "| comma inside a field is quoted automatically")
obj = {"id": 1, "tags": ("a", "b"), 2: "int key", "ok": True, "none": None}
text = json.dumps(obj)
print("dumps:", text)
print("loads:", json.loads(text), "<- tuple became list, int key became str, True->true->True")
with open("o.json", "w", encoding="utf-8") as f:
    json.dump({"a": [1, 2]}, f, indent=2)
with open("o.json", encoding="utf-8") as f:
    print("dump/load (file) vs dumps/loads (string):", json.load(f))
try:
    json.loads("{'a': 1}")
except json.JSONDecodeError as err:
    print("single quotes are not JSON:", err.msg)


# =============================================================== local REST server
ITEMS = {1: {"id": 1, "name": "Laptop", "category": "tech"}, 2: {"id": 2, "name": "Novel", "category": "books"}}
STATE = {"limited_calls": 0}


class Handler(BaseHTTPRequestHandler):
    def log_message(self, *args):
        pass

    def send(self, code, body=None, headers=None):
        data = b"" if body is None else json.dumps(body).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(data)))
        for k, v in (headers or {}).items():
            self.send_header(k, v)
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        u = urlparse(self.path)
        if u.path == "/items":
            cat = parse_qs(u.query).get("category", [None])[0]
            rows = [i for i in ITEMS.values() if cat is None or i["category"] == cat]
            return self.send(200, {"count": len(rows), "items": rows})
        if u.path.startswith("/items/"):
            i = int(u.path.split("/")[-1])
            return self.send(200, ITEMS[i]) if i in ITEMS else self.send(404, {"error": "not found"})
        if u.path == "/secure":
            if self.headers.get("Authorization") != "Bearer secret-token":
                return self.send(401, {"error": "missing or bad token"})
            return self.send(200, {"data": "private"})
        if u.path == "/limited":
            STATE["limited_calls"] += 1
            if STATE["limited_calls"] <= 2:
                return self.send(429, {"error": "slow down"}, {"Retry-After": "1"})
            return self.send(200, {"ok": True})
        if u.path == "/slow":
            time.sleep(1.5)
            return self.send(200, {"ok": True})
        if u.path == "/bad-json":
            self.send_response(200)
            self.send_header("Content-Length", "6")
            self.end_headers()
            self.wfile.write(b"{oops!")
            return
        self.send(404, {"error": "no such route"})

    def do_POST(self):
        n = int(self.headers.get("Content-Length", 0))
        try:
            body = json.loads(self.rfile.read(n) or b"{}")
        except ValueError:
            return self.send(400, {"error": "invalid JSON"})
        new_id = max(ITEMS) + 1
        ITEMS[new_id] = {"id": new_id, **body}
        self.send(201, ITEMS[new_id], {"Location": f"/items/{new_id}"})

    def do_PUT(self):
        n = int(self.headers.get("Content-Length", 0))
        body = json.loads(self.rfile.read(n))
        ITEMS[2] = {"id": 2, **body}
        self.send(200, ITEMS[2])

    def do_DELETE(self):
        ITEMS.pop(int(self.path.split("/")[-1]), None)
        self.send(204)


server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
base = f"http://127.0.0.1:{server.server_port}"
threading.Thread(target=server.serve_forever, daemon=True).start()
shown = base.replace(str(server.server_port), "PORT")

print("\n--- GET with query parameters ---")
r = requests.get(f"{base}/items", params={"category": "tech", "q": "a b&c"}, timeout=3)
print("url sent  :", r.url.replace(str(server.server_port), "PORT"), "(params are URL-encoded)")
print("status    :", r.status_code, r.reason, "| Content-Type:", r.headers["Content-Type"])
print("r.json()  :", r.json())
print("r.text type:", type(r.text).__name__, "| r.json() type:", type(r.json()).__name__)

print("\n--- status codes ---")
for method, path, kw in [("get", "/items/1", {}), ("get", "/items/99", {}), ("get", "/nowhere", {}),
                         ("post", "/items", {"json": {"name": "Pen", "category": "stationery"}}),
                         ("put", "/items/2", {"json": {"name": "Novel 2nd ed", "category": "books"}}),
                         ("delete", "/items/1", {})]:
    resp = getattr(requests, method)(base + path, timeout=3, **kw)
    extra = f" Location={resp.headers['Location']}" if "Location" in resp.headers else ""
    print(f"{method.upper():<6} {path:<10} -> {resp.status_code} {resp.reason}{extra}")
r = requests.post(f"{base}/items", data="not json", timeout=3)
print("POST with a bad body        ->", r.status_code, r.json())

print("\n--- errors: raise_for_status, auth, rate limit, timeout, bad JSON ---")
r = requests.get(f"{base}/items/99", timeout=3)
try:
    r.raise_for_status()
except requests.HTTPError as err:
    print("raise_for_status ->", type(err).__name__, "| code:", err.response.status_code)
print("no token ->", requests.get(f"{base}/secure", timeout=3).status_code,
      "| with Bearer token ->", requests.get(f"{base}/secure", headers={"Authorization": "Bearer secret-token"}, timeout=3).status_code)
for attempt in range(1, 4):
    r = requests.get(f"{base}/limited", timeout=3)
    print(f"/limited try {attempt}: {r.status_code}", f"Retry-After={r.headers['Retry-After']}" if r.status_code == 429 else "")
    if r.status_code == 429:
        time.sleep(0.05)       # real code sleeps int(Retry-After) seconds
try:
    requests.get(f"{base}/slow", timeout=0.5)
except requests.Timeout as err:
    print("timeout=0.5 on a 1.5 s endpoint ->", type(err).__name__)
try:
    requests.get(f"{base}/bad-json", timeout=3).json()
except ValueError as err:
    print("invalid JSON body -> ValueError subclass:", type(err).__name__)
try:
    requests.get("http://127.0.0.1:9/", timeout=2)
except requests.ConnectionError as err:
    print("nothing listening -> ", type(err).__name__)

with requests.Session() as s:
    s.headers.update({"Authorization": "Bearer secret-token"})
    print("Session reuses the connection and default headers:", s.get(f"{base}/secure", timeout=3).json())
server.shutdown()
