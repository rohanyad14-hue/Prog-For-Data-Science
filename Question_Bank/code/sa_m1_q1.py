"""Sample answer M1-Q1: library borrowing system with a dictionary, list, set, queue, priority queue, exceptions and a text file."""
import heapq
import itertools
import os
import tempfile
from collections import deque

# The datasets of the question, each in the structure that suits it
books = {                                                    # dictionary of dictionaries: BookID -> details
    "B101": {"title": "Python Programming", "author": "John Smith", "category": "Programming", "copies": 2},
    "B102": {"title": "Data Structures", "author": "Robert Brown", "category": "Computer Science", "copies": 0},
    "B103": {"title": "Machine Learning Basics", "author": "Alice Green", "category": "AI", "copies": 1},
    "B104": {"title": "Database Systems", "author": "David Lee", "category": "Database", "copies": 0},
    "B105": {"title": "Web Development", "author": "Emma Wilson", "category": "Programming", "copies": 3}}
members = {"M001": ("Ravi Kumar", "Premium"), "M002": ("Priya Singh", "Standard"),
           "M003": ("Arjun Das", "Premium"), "M004": ("Meena Rao", "Standard")}      # MemberID -> (name, type)
requests = [("R001", "M001", "B102", "10-10-2026"), ("R002", "M002", "B103", "11-10-2026"), ("R003", "M003", "B104", "11-10-2026"),
            ("R004", "M004", "B101", "12-10-2026"), ("R005", "M001", "B104", "12-10-2026")]    # list of tuples: ordered, repeats allowed
waiting = deque([("M001", "B102"), ("M003", "B104"), ("M001", "B104")])                  # queue: position = order in the deque

print("--- 1. the Books dataset in a dictionary keyed by BookID ---")
print(len(books), "books | title of B103:", books["B103"]["title"], "| copies of B105:", books["B105"]["copies"])
print("categories (a set removes repeats):", sorted({d["category"] for d in books.values()}))

print("\n--- 2. the waiting list is a FIFO queue (collections.deque) ---")
initial_waiting = list(waiting)
print("front to back:", list(waiting))
waiting.append(("M002", "B102"))                             # a new request joins at the back
print("a copy of B102 comes back -> serve:", waiting.popleft(), "| still waiting:", list(waiting))
waiting = deque(initial_waiting)                             # restore for the next steps
per_book = {}                                                # a dictionary of queues: one FIFO queue per book
for member, book in initial_waiting:
    per_book.setdefault(book, deque()).append(member)
print("one queue per book:", {b: list(q) for b, q in per_book.items()})
print("a copy of B104 comes back -> serve:", per_book["B104"].popleft(), "(the front of the global queue waits for B102, not B104)")

print("\n--- 3. books that are currently unavailable ---")
unavailable = [b for b, d in books.items() if d["copies"] == 0]
print(unavailable, [books[b]["title"] for b in unavailable])

print("\n--- 4. requests made by Premium members ---")
premium_ids = {m for m, (_, kind) in members.items() if kind == "Premium"}      # a set: fast "is this member Premium?"
for rid, mid, bid, date in (r for r in requests if r[1] in premium_ids):
    print(rid, members[mid][0], "asked for", books[bid]["title"], "on", date)


print("\n--- 5. exception for a non-existing book ---")
class BookNotFoundError(Exception):
    pass


def find_book(book_id):
    try:
        return books[book_id]
    except KeyError:
        raise BookNotFoundError(f"book {book_id} does not exist in the catalogue") from None


for bid in ("B101", "B110"):
    try:
        print(bid, "->", find_book(bid)["title"])
    except BookNotFoundError as e:
        print("error:", e)

print("\n--- 6. successful borrow transactions are written to a text file ---")
log_path = os.path.join(tempfile.mkdtemp(), "borrow_log.txt")
stock = {b: d["copies"] for b, d in books.items()}           # working copy of the stock
unserved = []
with open(log_path, "w", encoding="utf-8") as f:
    for rid, mid, bid, date in requests + [("R006", "M004", "B110", "13-10-2026")]:      # R006 asks for a book that does not exist
        try:
            find_book(bid)
        except BookNotFoundError as e:
            print("skipped", rid, "->", e)
            continue
        if stock[bid] > 0:
            stock[bid] -= 1
            f.write(f"{rid},{mid},{bid},{date},BORROWED\n")
        else:
            unserved.append((mid, bid))
with open(log_path, encoding="utf-8") as f:
    print(f.read().strip())
print("stock afterwards:", stock)
print("requests that had to wait equal the waiting-list dataset:", unserved == initial_waiting)

print("\n--- 7. a priority queue: Premium members are served before Standard members ---")
order, pq = itertools.count(), []                            # the counter keeps arrival order among equals


def enqueue(member, book):
    rank = 0 if members[member][1] == "Premium" else 1
    heapq.heappush(pq, (rank, next(order), member, book))


for m, b in [("M002", "B104"), ("M003", "B104"), ("M001", "B104")]:       # illustration: Priya (Standard) asked first
    enqueue(m, b)
print("served in this order:", [members[heapq.heappop(pq)[2]][0] for _ in range(3)])
