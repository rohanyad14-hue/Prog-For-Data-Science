"""A tiny weather service that stands in for a real REST API, so that sa_m1_q2.py can be tested offline.
It misbehaves on purpose for some cities: one error, one slow answer, one flaky answer, three kinds of invalid answer."""
import json
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlparse

DATA = {"Chennai": (33.5, 70, "Sunny"), "Mumbai": (31.0, 78, "Humid"), "Delhi": (24.5, 40, "Haze"), "Bengaluru": (26.0, 60, "Cloudy")}
_hits = {}


class Handler(BaseHTTPRequestHandler):
    def log_message(self, *args):
        pass

    def _send(self, code, body, ctype="application/json"):
        raw = body.encode("utf-8")
        try:
            self.send_response(code)
            self.send_header("Content-Type", ctype)
            self.send_header("Content-Length", str(len(raw)))
            self.end_headers()
            self.wfile.write(raw)
        except OSError:                                   # the client gave up (timeout): nothing to do
            pass

    def do_GET(self):
        url = urlparse(self.path)
        city = parse_qs(url.query).get("city", [""])[0]
        if url.path != "/weather":
            return self._send(404, "{}")
        _hits[city] = _hits.get(city, 0) + 1
        if city == "Bengaluru" and _hits[city] == 1:                       # flaky: the first call fails, the retry works
            return self._send(503, json.dumps({"error": "busy"}))
        if city == "Slowtown":
            time.sleep(2.5)
            return self._send(200, json.dumps({"city": city, "temp_c": 30, "humidity": 50}))
        if city == "Brokenville":
            return self._send(200, "<html>maintenance page</html>", "text/html")
        if city == "Nulltown":
            return self._send(200, json.dumps({"city": city, "humidity": 50}))      # temperature missing
        if city == "Hotville":
            return self._send(200, json.dumps({"city": city, "temp_c": 999, "humidity": 10}))
        if city in DATA:
            t, h, c = DATA[city]
            return self._send(200, json.dumps({"city": city, "temp_c": t, "humidity": h, "condition": c}))
        return self._send(404, json.dumps({"error": "unknown city"}))


def start_stub(port=8771):
    server = ThreadingHTTPServer(("127.0.0.1", port), Handler)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    return f"http://127.0.0.1:{port}"
