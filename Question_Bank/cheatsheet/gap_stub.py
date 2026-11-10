"""A tiny local REST server that copies the routes of https://jsonplaceholder.typicode.com (posts only).
Used by verify_gap_py.py so that the requests code of group 1.8 can be checked without internet access.
  GET /posts, GET /posts?userId=1, GET /posts/<id> (404 if unknown), POST /posts (201, id 101), PUT /posts/<id>, DELETE /posts/<id>
"""
import json
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlparse

POSTS = [{"userId": (i - 1) // 10 + 1, "id": i, "title": f"post title {i}", "body": f"post body {i}"} for i in range(1, 101)]


class Handler(BaseHTTPRequestHandler):
    def log_message(self, *args):  # keep the console quiet
        pass

    def _send(self, code, payload):
        body = json.dumps(payload).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _post_id(self, path):
        parts = path.strip("/").split("/")
        if len(parts) == 2 and parts[0] == "posts" and parts[1].isdigit():
            n = int(parts[1])
            return n if 1 <= n <= 100 else -1
        return None

    def do_GET(self):
        url = urlparse(self.path)
        if url.path == "/posts":
            q = parse_qs(url.query)
            rows = POSTS
            if "userId" in q:
                rows = [p for p in rows if str(p["userId"]) == q["userId"][0]]
            return self._send(200, rows)
        n = self._post_id(url.path)
        if n is None or n == -1:
            return self._send(404, {})
        return self._send(200, POSTS[n - 1])

    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0))
        body = json.loads(self.rfile.read(length) or b"{}")
        if urlparse(self.path).path != "/posts":
            return self._send(404, {})
        return self._send(201, {**body, "id": 101})

    def do_PUT(self):
        length = int(self.headers.get("Content-Length", 0))
        body = json.loads(self.rfile.read(length) or b"{}")
        n = self._post_id(urlparse(self.path).path)
        if n is None or n == -1:
            return self._send(404, {})
        return self._send(200, {**body, "id": n})

    def do_DELETE(self):
        n = self._post_id(urlparse(self.path).path)
        if n is None or n == -1:
            return self._send(404, {})
        return self._send(200, {})


_server = None


def start_stub(port=8765):
    """Start the server in a background thread (once) and return it."""
    global _server
    if _server is None:
        _server = ThreadingHTTPServer(("127.0.0.1", port), Handler)
        threading.Thread(target=_server.serve_forever, daemon=True).start()
    return _server
