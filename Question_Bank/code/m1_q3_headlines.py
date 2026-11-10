"""M1-Q3  Trending keywords from news headlines (REST API + NLTK).
The HTTP layer is a MockSession that returns genuine requests.Response objects,
so every error path below is the same code that would run against a live API.
Topics: REST/GET, status codes, JSON, exceptions, NLTK, dict/set/Counter, files.
"""
import json
import time
from collections import Counter

import nltk
import requests
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize

for pkg, path in [("punkt_tab", "tokenizers/punkt_tab"), ("stopwords", "corpora/stopwords"),
                  ("wordnet", "corpora/wordnet")]:
    try:
        nltk.data.find(path)
    except LookupError:
        nltk.download(pkg, quiet=True)

BASE_URL = "https://api.example-news.test/headlines"      # placeholder host


# ------------------------------------------------------------------ mock API
def _response(status, body):
    r = requests.Response()
    r.status_code = status
    r._content = body.encode() if isinstance(body, str) else body
    r.url = BASE_URL
    return r


def _ok(category, headlines):
    return _response(200, json.dumps({"category": category, "headlines": headlines}))


class MockSession:
    """Scripted behaviour per category; a list means 'one outcome per call'."""

    def __init__(self):
        self.calls = {}
        self.script = {
            "tech": [_ok("tech", [
                "AI chips drive record profits for chipmakers",
                "New AI model beats humans at coding tests",
                "Cybersecurity firms warn of rising ransomware attacks",
                "Startups adopt AI assistants for customer support",
                "Record funding for AI startups in the cloud"])],
            "sports": [_ok("sports", [
                "Local team wins championship after dramatic final",
                "Star striker signs record transfer deal",
                "Coach praises young players after the final",
                "Champions celebrate record crowd at the stadium"])],
            "business": [_ok("business", [
                "Markets rally as record profits lift banks",
                "Startups raise funding despite rising interest rates",
                "Airline profits climb on record travel demand"])],
            "politics": [requests.exceptions.Timeout("read timed out"),     # 1st call
                         _ok("politics", ["Parliament debates new data protection law",
                                          "Leaders meet to discuss trade deal",
                                          "Voters react to new law on privacy"])],
            "health": [_ok("health", [])],                                  # empty list
            "science": [_response(200, "<html>Service busy</html>")],       # not JSON
            "travel": [_response(404, "not found")],
            "weather": [requests.exceptions.ConnectionError("network down")] * 3,
        }

    def get(self, url, params=None, timeout=None):
        cat = params["category"]
        n = self.calls.get(cat, 0)
        self.calls[cat] = n + 1
        scripted = self.script[cat]
        outcome = scripted[min(n, len(scripted) - 1)]
        if isinstance(outcome, Exception):
            raise outcome
        return outcome


# ------------------------------------------------------------------ fetching
class ApiError(Exception):
    pass


def fetch_headlines(category, session, retries=2):
    """GET /headlines?category=... ; returns list[str] or raises ApiError."""
    last_problem = None
    for attempt in range(1, retries + 1):
        try:
            resp = session.get(BASE_URL, params={"category": category}, timeout=5)
            resp.raise_for_status()                    # 4xx / 5xx -> HTTPError
            data = resp.json()                         # bad JSON -> ValueError
            headlines = data["headlines"]              # missing key -> KeyError
            if not isinstance(headlines, list) or not headlines:
                raise ApiError("empty headline list")
            return [h for h in headlines if isinstance(h, str) and h.strip()]
        except (requests.exceptions.Timeout, requests.exceptions.ConnectionError) as err:
            last_problem = f"network problem ({type(err).__name__})"      # worth retrying
            time.sleep(0)                              # real code: back off (e.g. 2**attempt)
        except requests.exceptions.HTTPError as err:
            raise ApiError(f"HTTP {err.response.status_code}") from err   # do not retry 404
        except ValueError as err:
            raise ApiError("invalid JSON") from err
        except KeyError as err:
            raise ApiError(f"missing field {err}") from err
    raise ApiError(f"{last_problem} after {retries} attempts")


# ------------------------------------------------------------------ NLTK
STOP = set(stopwords.words("english"))
LEMMA = WordNetLemmatizer()


def keywords(headline):
    tokens = word_tokenize(headline.lower())
    return [LEMMA.lemmatize(t) for t in tokens if t.isalpha() and t not in STOP and len(t) > 2]


# ------------------------------------------------------------------ workflow
session = MockSession()
counts = {}                       # category -> Counter
failures = {}
for cat in ["tech", "sports", "business", "politics", "health", "science", "travel", "weather"]:
    try:
        heads = fetch_headlines(cat, session)
    except ApiError as err:
        failures[cat] = str(err)
        print(f"[skip] {cat:<9}: {err}")
        continue
    c = Counter()
    for h in heads:
        c.update(keywords(h))
    counts[cat] = c
    print(f"[ok]   {cat:<9}: {len(heads)} headlines, {len(c)} distinct keywords")

print("\nExample: ", keywords("Startups adopt AI assistants for customer support"))

print("\nTop 5 keywords per category")
for cat, c in counts.items():
    print(f"  {cat:<9}", c.most_common(5))

print("\nKeywords unique to one category")
for cat, c in counts.items():
    others = set().union(*(set(o) for k, o in counts.items() if k != cat))
    unique = set(c) - others
    print(f"  {cat:<9} {len(unique)} unique, e.g. {sorted(unique)[:6]}")

with open("top_keywords.txt", "w", encoding="utf-8") as f:
    for cat, c in counts.items():
        f.write(f"{cat}: " + ", ".join(f"{w}({n})" for w, n in c.most_common(5)) + "\n")

print("\ntop_keywords.txt")
print(open("top_keywords.txt", encoding="utf-8").read(), end="")
print("\nFailed categories:", failures)
