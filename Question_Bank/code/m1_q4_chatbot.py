"""M1-Q4  Hostel complaint chatbot.
NLTK does the language work, a heapq priority queue orders complaints, a
dictionary answers FAQs, and ChatterBot (optional) handles small talk.
Topics: OOP, NLTK, priority queue, exceptions, file handling.
"""
import heapq
import itertools
from datetime import datetime

import nltk
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize

for pkg, path in [("punkt_tab", "tokenizers/punkt_tab"), ("wordnet", "corpora/wordnet")]:
    try:
        nltk.data.find(path)
    except LookupError:
        nltk.download(pkg, quiet=True)

URGENT, ROUTINE = 0, 1            # smaller number = served first by heapq


class Complaint:
    def __init__(self, cid, text, category, priority):
        self.cid, self.text, self.category, self.priority = cid, text, category, priority

    def __str__(self):
        level = "URGENT " if self.priority == URGENT else "routine"
        return f"#{self.cid} [{level}] {self.category:<11} {self.text}"


class Classifier:
    CATEGORIES = {
        "water": {"water", "tap", "geyser", "bathroom", "leak", "drinking"},
        "wifi": {"wifi", "internet", "network", "router", "signal"},
        "electricity": {"electricity", "power", "light", "fan", "socket", "switch", "fuse"},
        "mess": {"mess", "food", "breakfast", "lunch", "dinner", "stale", "menu"},
    }
    URGENT_TOKENS = {"emergency", "urgent", "fire", "spark", "shock", "flood"}

    def __init__(self):
        self.lemma = WordNetLemmatizer()

    def tokens(self, text):
        text = text.lower().replace("wi-fi", "wifi")
        return [self.lemma.lemmatize(t) for t in word_tokenize(text) if t.isalnum()]

    def category(self, tokens):
        scores = {c: len(words & set(tokens)) for c, words in self.CATEGORIES.items()}
        best = max(scores, key=scores.get)
        return best if scores[best] > 0 else None

    def is_urgent(self, tokens):
        t = set(tokens)
        no_service = "no" in t and ("water" in t or "electricity" in t or "power" in t)
        power_loss = "power" in t and bool({"failure", "cut", "outage", "off"} & t)
        return bool(self.URGENT_TOKENS & t) or no_service or power_loss


class FaqBook:
    ENTRIES = [   # (keywords that must all appear, answer)  -- sample data, not real hostel data
        ({"mess", "timing"}, "Mess: breakfast 7:30-9:00, lunch 12:30-2:00, dinner 7:30-9:00."),
        ({"warden", "contact"}, "Warden office: ext. 2145 (9am-6pm). Emergencies: security desk, ext. 2100."),
        ({"warden", "number"}, "Warden office: ext. 2145 (9am-6pm). Emergencies: security desk, ext. 2100."),
    ]

    def answer(self, tokens):
        t = set(tokens)
        for needed, reply in self.ENTRIES:
            if needed <= t:
                return reply
        return None


class ComplaintLog:
    def __init__(self, path, clock=datetime.now):
        self.path, self.clock = path, clock

    def write(self, c):
        with open(self.path, "a", encoding="utf-8") as f:          # append, never overwrite
            f.write(f"{self.clock()} | #{c.cid} | {c.category} | "
                    f"{'URGENT' if c.priority == URGENT else 'routine'} | {c.text}\n")


class HostelChatbot:
    def __init__(self, log_path, small_talk=None):
        self.clf, self.faq = Classifier(), FaqBook()
        self.log = ComplaintLog(log_path, clock=lambda: "2026-07-06 21:00:00")
        self.heap, self.counter = [], itertools.count(1)            # counter breaks ties -> FIFO
        self.small_talk = small_talk                                # optional ChatterBot instance

    def handle(self, message):
        if not isinstance(message, str) or not message.strip():
            raise ValueError("empty or non-text message")
        tokens = self.clf.tokens(message)
        reply = self.faq.answer(tokens)
        if reply:
            return f"FAQ  -> {reply}"
        category = self.clf.category(tokens)
        if category is None:
            if self.small_talk is not None:
                answer = self.small_talk.get_response(message)
                if answer.confidence >= 0.6:            # trust ChatterBot only when it is sure
                    return f"BOT  -> {answer}"
            return "BOT  -> Sorry, I did not understand. Is it about water, Wi-Fi, electricity or the mess?"
        priority = URGENT if self.clf.is_urgent(tokens) else ROUTINE
        cid = next(self.counter)
        c = Complaint(cid, message.strip(), category, priority)
        heapq.heappush(self.heap, (priority, cid, c))               # (priority, arrival order)
        self.log.write(c)
        return f"LOGGED -> {c}"

    def process_all(self):
        while self.heap:
            _, _, c = heapq.heappop(self.heap)
            yield c


def build_chatterbot():
    """Optional: only used when the 'chatterbot' package is installed."""
    try:
        from chatterbot import ChatBot
        from chatterbot.trainers import ListTrainer
    except ImportError:
        return None
    bot = ChatBot("HostelBot",
                  storage_adapter="chatterbot.storage.SQLStorageAdapter",
                  database_uri="sqlite:///hostelbot.sqlite3",
                  read_only=True)                       # do not learn from live users
    ListTrainer(bot).train(["Hi", "Hello! How can I help you today?",
                            "Thanks", "You are welcome!"])
    return bot


if __name__ == "__main__":
    open("complaints.log", "w").close()                              # fresh log for the demo run
    bot = HostelChatbot("complaints.log", small_talk=build_chatterbot())
    messages = [
        "The mess food was stale at dinner",
        "There is no water in the bathroom of block B",
        "Wi-Fi is very slow in my room",
        "What are the mess timings?",
        "Hi",
        "Power failure in block C since evening",
        "asdf qwerty",
        "",
        "Who is the warden and what is the contact number?",
        "The fan in room 204 is not working",
    ]
    print("Incoming messages")
    for m in messages:
        try:
            print(f"  {m!r:<55} {bot.handle(m)}")
        except ValueError as err:
            print(f"  {m!r:<55} INVALID -> {err}")

    print("\nProcessing order from the priority queue")
    for c in bot.process_all():
        print(" ", c)

    print("\ncomplaints.log")
    print(open("complaints.log", encoding="utf-8").read(), end="")
