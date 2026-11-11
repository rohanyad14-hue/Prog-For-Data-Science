"""Answers to the three Module 1 sample questions (Python data structures, REST APIs, NLTK and ChatterBot)."""
from dsl import B, CODE, H3, H4, NOTE, OUT, P, T, TIP, WARN

QUESTIONS = []


def question(qid, title, image, blocks):
    QUESTIONS.append(dict(id=qid, module=1, title=title, image=image, blocks=blocks))


# ------------------------------------------------------------------------------------------------ Q1
question("M1-Q1", "Library Borrowing System: lists, dictionaries, sets, queues and priority queues",
         ["6260159273853719032.jpg", "6260159273853719033.jpg", "6260159273853719035.jpg", "6260159273853719036.jpg", "6260159273853719037.jpg"], [
    NOTE("This question arrives as five screenshots (Books, Members, Borrow Request and Waiting List datasets, then the seven tasks). The picture numbered ...034 that would hold the opening scenario text is not in the folder, "
         "so the answer works from the datasets and the seven tasks. The waiting list is consistent with the borrow requests: it holds exactly the requests for books with 0 copies (B102 and B104), in order."),
    H3("Answer, task by task"),
    H4("1. Store the Books dataset using a suitable Python data structure"),
    P("A <b>dictionary of dictionaries</b> keyed by BookID: `books[\"B103\"][\"title\"]`. The BookID is the natural key, a lookup by key takes the same time for 5 or 5 million books, and the inner dictionary gives every field a name."),
    T(["Structure", "Fits?", "Reason"], [
        ["<b>dict of dicts</b> (chosen)", "yes", "O(1) lookup by BookID, readable field names, easy to update `copies`"],
        ["list of dicts", "partly", "keeps order and is easy to loop over, but finding B103 means scanning the list (O(n))"],
        ["list of tuples / namedtuple", "partly", "compact; tuples are immutable, so a changing `copies` needs a new tuple"],
        ["pandas DataFrame", "for analysis", "best once you filter and group whole columns (Module 2); heavy for a few look-ups"]], [0.28, 0.14, 0.58]),
    P("The other datasets follow the same rule: Members in a dictionary (`MemberID -> (name, type)`), the Borrow Requests in a <b>list of tuples</b> (an ordered log in which the same member may appear many times), the Waiting List in a queue."),
    H4("2. Maintain the Waiting List using a Queue"),
    B(["A queue is first in, first out. Use `collections.deque`: `append(x)` joins at the back, `popleft()` serves the front, both in O(1). `list.pop(0)` shifts every element and is O(n); `queue.Queue` is meant for threads.",
       "The output shows the dataset as a queue, a new request joining at the back, and `popleft()` serving ('M001', 'B102') first when a copy of B102 returns.",
       "<b>Design point:</b> when a copy of B104 returns, the member to serve is the first one waiting for <b>B104</b> (M003), not the front of the global queue (M001 waits for B102). A dictionary with one deque per book, `{book: deque}`, gives exactly that; the code prints it."]),
    H4("3. Identify books that are currently unavailable"),
    P("A list comprehension over the dictionary: `[b for b, d in books.items() if d[\"copies\"] == 0]` returns <b>B102 (Data Structures)</b> and <b>B104 (Database Systems)</b>."),
    H4("4. Display all requests made by Premium members"),
    P("Build a <b>set</b> of Premium member ids (`{m for m, (_, kind) in members.items() if kind == \"Premium\"}`), because \"is this member in the set?\" is a constant-time test, then filter the request list with it. Result: <b>R001</b> (Ravi Kumar, Data Structures), <b>R003</b> (Arjun Das, Database Systems), <b>R005</b> (Ravi Kumar, Database Systems)."),
    H4("5. Handle the exception when a user requests a non-existing book (B110)"),
    B(["Define your own exception, `class BookNotFoundError(Exception)`, and turn the low-level `KeyError` into it inside `find_book`: `except KeyError: raise BookNotFoundError(...) from None`. The caller then catches one meaningful error.",
       "The program prints \"book B110 does not exist in the catalogue\" and continues: in the transaction loop request R006 for B110 is skipped, not fatal.",
       "Running out of copies is <b>not</b> an exception but a normal outcome: that request goes to the waiting list."]),
    H4("6. Record all successful borrow transactions in a text file"),
    B(["A request succeeds if a copy is in stock when it is processed. The loop reduces the stock by one and writes a line with `with open(path, \"w\") as f: f.write(...)` (use mode `\"a\"` to append to an existing log).",
       "Result in the file: <b>R002</b> (M002, B103) and <b>R004</b> (M004, B101). The other requests had no copy and went to the waiting list, which reproduces the Waiting List dataset exactly (the program prints `True`).",
       "`with` closes the file even if an error occurs; the file is read back to prove what was written."]),
    H4("7. Where can Lists, Dictionaries, Sets, Queues and Priority Queues be applied?"),
    T(["Structure", "Use in the library system"], [
        ["<b>List</b>", "ordered log of requests and transactions (append, loop, slice), results of searches"],
        ["<b>Dictionary</b>", "books by BookID, members by MemberID, copies in stock, one waiting queue per book, counts of borrows per category"],
        ["<b>Set</b>", "Premium member ids (fast membership test), the distinct categories, members who have ever borrowed, members who requested but never borrowed (set difference)"],
        ["<b>Queue</b> (deque)", "the waiting list: first come, first served"],
        ["<b>Priority queue</b> (`heapq`)", "serve Premium members before Standard members for the same book, ties broken by arrival order"]], [0.22, 0.78]),
    P("The last row is run in the code as an illustration: if Priya (Standard) had asked for B104 first, the priority queue still serves Arjun Das and Ravi Kumar (Premium) before her. The entries are tuples `(rank, arrival counter, member, book)`; the counter keeps arrival order among equal ranks."),
    WARN("A priority queue changes fairness: Standard members can wait much longer. State the rule explicitly (for example, Premium first but nobody waits more than 7 days)."),
    H3("Code, run on the datasets of the question"),
    CODE("sa_m1_q1.py", "Code: code/sa_m1_q1.py"),
    OUT("sa_m1_q1.out.txt", "Real output", maxlines=60),
])

# ------------------------------------------------------------------------------------------------ Q2
question("M1-Q2", "Weather Monitoring and Analysis using REST APIs", "6260159273853719038.jpg", [
    H3("Answer"),
    H4("The complete workflow"),
    T(["Step", "What happens", "Python tools"], [
        ["1 Configure", "list of cities, base URL, timeout and retry limit; the API key comes from an environment variable, never from the source code", "`os.environ`, constants"],
        ["2 Request", "one HTTP GET per city with query parameters, over one reused connection and with a timeout", "`requests.Session`, `session.get(url, params=..., timeout=...)`"],
        ["3 Check the answer", "status code, JSON parsing, required fields, types and plausible ranges", "`resp.status_code`, `raise_for_status`, `resp.json()`, `validate()`"],
        ["4 Process and store", "valid readings go into one dictionary (city -> reading), failures into another (city -> reason)", "`dict`"],
        ["5 Handle failures", "transient problems are retried with a growing pause; invalid answers are recorded, not retried; one bad city never stops the others", "`try / except`, custom exceptions, `time.sleep`"],
        ["6 Summarise", "counts, average, hottest and coldest city, list of problems", "`statistics`, `max`, `min`"],
        ["7 Save", "summary as text, readings as JSON", "`with open(...)`, `json.dump`"]], [0.17, 0.53, 0.30]),
    H4("How APIs, exception handling, dictionaries and file handling work together"),
    B(["The <b>API</b> is the source of the data but cannot be trusted: it may be slow, down, or send nonsense. Everything that crosses this boundary is checked.",
       "<b>Exception handling</b> is the safety net around each external step. A small hierarchy (`WeatherError` with `NetworkError` and `InvalidResponse` below it) lets the program decide: retry transient problems, only record invalid ones. A broad `except Exception` would hide programming errors, so the handlers are specific.",
       "<b>Dictionaries</b> hold the result in a form that is easy to use: `results[city]` for readings, `failures[city]` for reasons. Together they account for every city requested (4 + 5 = 9).",
       "<b>File handling</b> makes the outcome durable and auditable: `summary.txt` for people, `readings.json` for other programs. `with` guarantees the files are closed even when something fails."]),
    H4("What makes it robust and reliable"),
    T(["Problem", "In the test run", "Handled by"], [
        ["Server error HTTP 503 (busy)", "Bengaluru fails once, then works", "retry with a pause: \"ok after 2 attempt(s)\""],
        ["Slow server", "Slowtown answers after 2.5 s, timeout is 1 s", "`timeout=` raises `ReadTimeout`; after the retries it is recorded as a network problem"],
        ["Client error HTTP 404", "Atlantis", "not retried (our request is wrong): \"request rejected: HTTP 404\""],
        ["Answer is not JSON", "Brokenville returns an HTML page", "`resp.json()` fails, turned into `InvalidResponse`"],
        ["Field missing", "Nulltown has no `temp_c`", "`validate()` raises `InvalidResponse`"],
        ["Impossible value", "Hotville says 999 C", "range check in `validate()`"],
        ["Connection refused or lost", "same family as the timeout", "`requests.ConnectionError` is retried like a timeout"]], [0.26, 0.34, 0.40]),
    TIP("Never call `requests.get` without `timeout=`: by default it can wait forever. Retry only what can change on a second try (timeouts, 5xx), never 4xx errors or invalid data."),
    NOTE("The weather service is a small local stand-in server (`sa_m1_q2_stub.py`) that misbehaves on purpose for the cities above, so that every failure can be reproduced offline. With a real provider only `BASE_URL` and the API key change."),
    H3("Code, run against the stand-in service"),
    CODE("sa_m1_q2.py", "Code: code/sa_m1_q2.py (the client)"),
    CODE("sa_m1_q2_stub.py", "Code: code/sa_m1_q2_stub.py (the stand-in service)"),
    OUT("sa_m1_q2.out.txt", "Real output", maxlines=60),
])

# ------------------------------------------------------------------------------------------------ Q3
question("M1-Q3", "Intelligent Student Support Chatbot using NLTK and ChatterBot", "6260159273853719039.jpg", [
    H3("Answer"),
    H4("Object-oriented design: classes, attributes and methods"),
    T(["Class", "Attributes", "Methods", "Responsibility"], [
        ["`Preprocessor`", "`stop` (set of stop words), `stem` (stemmer)", "`keywords(text)`", "NLTK: tokenise, lower-case, drop stop words and punctuation, stem; raises `EmptyQueryError`"],
        ["`KnowledgeBase`", "`answers` (dict intent -> answer), `index` (dict keyword -> set of intents)", "`add(intent, examples, answer)`, `rank(keywords)`", "stores the FAQ and finds the intents that share keywords with a question"],
        ["`SupportBot`", "`kb`, `prep`, `brain` (ChatterBot), `history` (list), `unanswered` (Counter), `review_queue` (deque)", "`ask(text)`, `learn(question, answer)`", "the controller: chooses between FAQ, ChatterBot, clarification and fallback"],
        ["`Interaction`", "`query`, `answer`, `source`", "(a dataclass)", "one line of the conversation history"],
        ["`EmptyQueryError`", "", "", "custom exception for empty input"]], [0.17, 0.30, 0.24, 0.29]),
    H4("1. Process user input and identify keywords"),
    P("NLTK's `word_tokenize` splits the text, stop words (\"which\", \"and\", \"are\", \"there\") and punctuation are removed, and `PorterStemmer` reduces words to their stem, so \"exams\" and \"exam\" match. \"Which courses and exams are there?\" becomes the set {`cours`, `exam`} (printed in the output). The same preprocessing is applied to the stored example questions, so both sides use the same vocabulary."),
    H4("2. Store frequently asked questions and responses"),
    B(["In the <b>KnowledgeBase</b>: a dictionary intent -> answer, plus an <b>inverted index</b> (keyword -> set of intents), so that finding the candidate answers for a question costs a few dictionary look-ups, not a scan of all FAQs.",
       "In <b>ChatterBot</b>: question-answer pairs trained with `ListTrainer` and stored in its SQLite database. It finds the stored question that is most similar to the user's wording, which covers phrasings the keyword index misses (the library timings in the output)."]),
    H4("3. Handle invalid or ambiguous queries"),
    T(["Situation", "Example in the run", "Reaction"], [
        ["Empty input", "`'   '`", "`EmptyQueryError` is raised in `keywords()` and caught in `ask()`: \"Please type your question.\""],
        ["Ambiguous: two intents fit equally", "\"Which courses and exams are there?\"", "ask instead of guessing: \"Do you mean courses or exams?\""],
        ["Unknown", "\"How is the weather on campus?\"", "polite fallback; the question goes to a review queue and is counted"]], [0.26, 0.34, 0.40]),
    H4("4. Continuously learn from user interactions"),
    B(["Unknown questions are collected in a <b>deque</b> (`review_queue`, first in first out) and counted in a `Counter`, so staff can answer the most frequent ones first.",
       "A staff answer is added with `learn(question, answer)`, which calls `ListTrainer.train`. In the output the same question is answered correctly after that.",
       "Why not learn from everything automatically? ChatterBot can store every conversation, but then wrong or abusive inputs become \"knowledge\". Human-in-the-loop learning keeps accuracy under control (the demo bot is created with `read_only=True`)."]),
    H4("How NLTK, ChatterBot, exceptions and data structures improve accuracy and user experience"),
    T(["Part", "Contribution"], [
        ["NLTK preprocessing", "stemming and stop-word removal make \"exam\", \"exams\" and \"Exam dates?\" meet; fewer false matches"],
        ["Two-layer matching", "exact keyword match first (fast, predictable), ChatterBot similarity second (flexible)"],
        ["Exceptions", "bad input never crashes the conversation; every problem has a friendly reply"],
        ["dict / set / Counter / deque / list", "O(1) look-ups, no duplicates, frequency statistics, a fair review queue, a full history for analysis"],
        ["Clarification and fallback", "the bot asks or admits it does not know, instead of giving a wrong answer with confidence"]], [0.28, 0.72]),
    WARN("Honest limits: keyword matching does not understand meaning or synonyms, and ChatterBot is retrieval-based (it returns stored answers, it does not generate them). For better accuracy later, add an intent classifier (TF-IDF with logistic regression) or sentence embeddings."),
    H3("Code, run in an environment with NLTK and ChatterBot"),
    CODE("sa_m1_q3.py", "Code: code/sa_m1_q3.py"),
    OUT("sa_m1_q3.out.txt", "Real output"),
])
