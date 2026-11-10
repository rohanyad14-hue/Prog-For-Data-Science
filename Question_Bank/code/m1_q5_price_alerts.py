"""M1-Q5  Asset price alert system (REST polling + retries).
Uses a MockSession that returns real requests.Response objects so the error
handling is the same code that would run against a live API.
Topics: GET, status codes (200/404/429/5xx), JSON, try/except/else/finally,
list/tuple/dict, conditionals, file modes (a for the alert log).
"""
import io
import json
from collections import deque

import requests

BASE_URL = "https://api.example-prices.test/price"          # placeholder host
LIMITS = {"BTC": (60000, 70000), "GOLD": (1900, 2100), "ETH": (1500, 2500), "OIL": (70, 90)}


def _resp(status, body, headers=None):
    r = requests.Response()
    r.status_code = status
    r._content = body.encode()
    r.raw = io.BytesIO(b"")          # a real response owns a socket-backed 'raw' stream
    r.headers.update(headers or {})
    return r


def _price(asset, p):
    return _resp(200, json.dumps({"asset": asset, "price": p}))


class MockSession:
    """One scripted outcome per call, per asset."""

    def __init__(self):
        self.n = {}
        self.script = {
            "BTC": [_price("BTC", p) for p in (64000, 65500, 70500, 66000, 59000, 61000)],
            "GOLD": [requests.exceptions.Timeout("slow"), _price("GOLD", 2000),
                     _resp(429, "slow down", {"Retry-After": "1"}), _price("GOLD", 2050),
                     _price("GOLD", 2110), _price("GOLD", 2080), _price("GOLD", 2060)],
            "ETH": [_resp(404, "unknown asset")],
            "OIL": [_price("OIL", 80), _resp(200, "{oops"), _price("OIL", 91),
                    _price("OIL", 85), _price("OIL", 69), _price("OIL", 75), _price("OIL", 78)],
        }

    def get(self, url, params=None, timeout=None):
        a = params["asset"]
        i = self.n.get(a, 0)
        self.n[a] = i + 1
        out = self.script[a][min(i, len(self.script[a]) - 1)]
        if isinstance(out, Exception):
            raise out
        return out


def fetch_price(asset, session, max_tries=3):
    """Return a float, or None when the asset must be skipped this cycle."""
    for attempt in range(1, max_tries + 1):
        resp = None
        try:
            resp = session.get(BASE_URL, params={"asset": asset}, timeout=3)
            resp.raise_for_status()
            price = float(resp.json()["price"])
        except requests.exceptions.Timeout:
            print(f"    {asset}: timeout (try {attempt}/{max_tries}) -> retry")
        except requests.exceptions.HTTPError:
            code = resp.status_code
            if code == 429:
                wait = int(resp.headers.get("Retry-After", 1))
                print(f"    {asset}: 429 Too Many Requests -> wait {wait}s, retry")
            elif code >= 500:
                print(f"    {asset}: {code} server error -> retry")
            else:                                   # 404 etc. -> client error, retrying is useless
                print(f"    {asset}: HTTP {code} -> skip, no retry")
                return None
        except (ValueError, KeyError, TypeError):
            print(f"    {asset}: invalid JSON / missing price -> skip this cycle")
            return None
        else:
            return price                            # only runs when no exception happened
        finally:
            if resp is not None:                    # always release the connection
                resp.close()
    print(f"    {asset}: gave up after {max_tries} tries")
    return None


session = MockSession()
history = {a: deque(maxlen=5) for a in LIMITS}      # last 5 (timestamp, price) tuples per asset
alerts = []
clock = ["10:00", "10:01", "10:02", "10:03", "10:04", "10:05"]

for stamp in clock:                                 # a real app would loop with time.sleep(interval)
    print(f"Cycle {stamp}")
    for asset, (low, high) in LIMITS.items():
        price = fetch_price(asset, session)
        if price is None:
            continue
        history[asset].append((stamp, price))
        if price > high:
            alerts.append(f"{stamp} {asset} ABOVE upper limit {high}: {price}")
        elif price < low:
            alerts.append(f"{stamp} {asset} BELOW lower limit {low}: {price}")

with open("alerts.log", "a", encoding="utf-8") as log:      # 'a' keeps old alerts
    for line in alerts:
        log.write(line + "\n")

print("\nLast five readings per asset")
for a, h in history.items():
    print(f"  {a:<5}", list(h))
print("\nAlerts raised")
for line in alerts:
    print(" ", line)
