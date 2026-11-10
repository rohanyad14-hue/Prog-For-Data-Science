from dsl import *

# ---------------------------------------------------------------------------------------------- MCQ
mcqs = [
    MCQ("Which built-in structure is the best choice to test whether a roll number is among 10 million stored roll numbers?",
        ["list", "tuple", "set", "str"], 2,
        "A set is a hash table, so `in` is O(1) on average. A list or tuple scans every element, O(n)."),
    MCQ("`heapq.heappop(h)` on a list `h` managed by heapq returns:",
        ["the largest item", "the smallest item", "the most recently pushed item", "the oldest item"], 1,
        "heapq implements a min-heap. For a max-heap push negated priorities."),
    MCQ("`d = {'a': 1}; d.get('z', 0)` evaluates to:",
        ["KeyError", "None", "0", "'z'"], 2,
        "`get` returns the default (0) when the key is missing; `d['z']` would raise KeyError."),
    MCQ("Which statement about `finally` is correct?",
        ["It runs only if an exception occurs", "It runs only if no exception occurs",
         "It runs whether or not an exception occurs", "It replaces `except`"], 2,
        "`finally` always runs (even after `return`), so it is the place for clean-up such as closing a connection."),
    MCQ("Which HTTP status code means \"Too Many Requests\"?", ["401", "404", "429", "503"], 2,
        "429 is rate limiting. 401 = unauthorised, 404 = not found, 503 = service unavailable."),
    MCQ("File mode `\"a\"` does what?",
        ["Reads the file", "Truncates the file then writes", "Appends to the end and creates the file if missing",
         "Opens for read and write without creating"], 2,
        "`\"w\"` truncates, `\"a\"` appends, `\"r\"` reads (error if missing), `\"r+\"` reads and writes an existing file."),
    MCQ("Inside `class A`, the attribute `self.__x` is stored under the name:",
        ["`__x`", "`_A__x`", "`A.__x`", "`x`"], 1,
        "Name mangling rewrites `__x` to `_ClassName__x` to avoid accidental clashes in subclasses. It is not true privacy."),
    MCQ("Which operation turns \"geese\" into \"goose\"?",
        ["Tokenization", "Stemming (Porter)", "Lemmatization", "Stopword removal"], 2,
        "A lemmatizer uses a dictionary (WordNet) and returns a real word. A stemmer only chops suffixes."),
    MCQ("Which can be used as a dictionary key?",
        ["`[1, 2]`", "`{1, 2}`", "`(1, 2)`", "`{'a': 1}`"], 2,
        "Keys must be hashable. Tuples of hashable items are; lists, sets and dicts are mutable and unhashable."),
    MCQ("Removing the first element repeatedly from a very long Python `list` (`pop(0)`) is slow because:",
        ["lists are immutable", "all remaining elements are shifted, O(n) per pop",
         "pop(0) copies the whole list to disk", "Python locks the list"], 1,
        "Use `collections.deque` and `popleft()` (O(1)) for queues."),
]

# ---------------------------------------------------------------------------------------------- SHORT
shorts = [
    SHORT("Differentiate between a list and a tuple. When would you prefer a tuple?", 3, [
        T(["Point", "List", "Tuple"], [
            ["Mutability", "Mutable: append, insert, remove, item assignment", "Immutable: fixed after creation"],
            ["Syntax", "`[1, 2, 3]`", "`(1, 2, 3)`; a one-item tuple needs a comma: `(1,)`"],
            ["Hashable", "No, cannot be a dict key or set member", "Yes, if all its items are hashable"],
            ["Speed / memory", "Over-allocates for growth", "Slightly smaller and faster to create"]], [0.2, 0.4, 0.4]),
        P("Prefer a tuple for a fixed record such as `(name, cgpa, backlogs)`, for dictionary keys such as "
          "`(row, col)`, and for returning several values from a function.")]),
    SHORT("Explain `try`, `except`, `else` and `finally` with a small example.", 5, [
        P("`try` holds the risky code. `except` handles a named exception. `else` runs only when the `try` block raised nothing. "
          "`finally` always runs, so it holds clean-up code."),
        SNIP('def read_int(text):\n    try:\n        n = int(text)             # may raise ValueError\n'
             '    except ValueError:\n        print("not a number"); return None\n'
             '    else:\n        print("parsed OK"); return n     # only when no exception\n'
             '    finally:\n        print("done")                 # always, even after return'),
        P("Good practice: catch the narrowest exception, keep the `try` block small, never use a bare `except:`, "
          "and raise custom exceptions (`class AppError(Exception)`) for domain errors.")]),
    SHORT("Implement a stack and a queue using Python built-ins and state the cost of each operation.", 5, [
        SNIP("from collections import deque\n\nstack = []                  # LIFO\nstack.append(1); stack.append(2)\n"
             "top = stack.pop()           # 2, O(1) at the end\n\nqueue = deque()             # FIFO\n"
             "queue.append(1); queue.append(2)\nfirst = queue.popleft()    # 1, O(1)"),
        P("A list is a good stack. For a queue use `deque` because `list.pop(0)` shifts every element (O(n)). "
          "Stack uses: undo/redo, bracket matching, recursion. Queue uses: task scheduling, BFS, print spooling.")]),
    SHORT("How is a priority queue built in Python? How do you get highest-priority-first behaviour?", 3, [
        P("`heapq` keeps a list arranged as a binary min-heap: `heappush` and `heappop` cost O(log n), looking at `h[0]` is O(1)."),
        SNIP("import heapq\nh = []\nheapq.heappush(h, (-9.1, 'Sneha'))   # negate for max-first\n"
             "heapq.heappush(h, (-8.6, 'Ananya'))\nprint(heapq.heappop(h))        # (-9.1, 'Sneha')"),
        P("Tuples compare element by element, so ties on priority fall back to the next item; add a running counter "
          "`(priority, counter, item)` to keep first-come-first-served order and to avoid comparing non-comparable objects.")]),
    SHORT("Compare HTTP GET and POST.", 3, [
        T(["", "GET", "POST"], [
            ["Purpose", "Read a resource", "Create or submit data"],
            ["Data location", "URL query string (`?category=tech`)", "Request body (JSON, form)"],
            ["Idempotent / safe", "Yes, repeating it changes nothing", "No, repeating can create duplicates"],
            ["Caching / bookmarking", "Can be cached and bookmarked", "Normally not cached"],
            ["Size / secrecy", "URL length limits; data visible in logs", "Large bodies; not shown in the URL"]],
          [0.22, 0.39, 0.39])]),
    SHORT("Explain public, protected and private members in Python. What do `@classmethod` and `@staticmethod` do?", 5, [
        B(["`name`: public. `_name`: protected by convention (a hint, not enforced). `__name`: private by name mangling "
           "(stored as `_Class__name`).",
           "`@classmethod` receives the class (`cls`) and is used for alternative constructors, e.g. `from_dict(cls, d)`.",
           "`@staticmethod` receives neither `self` nor `cls`; it is a plain utility function placed in the class namespace, "
           "e.g. `validate_name(name)`.",
           "Instance methods receive `self` and work on one object's data."]),
        SNIP("class Pipeline:\n    def __init__(self, name):\n        self.name = name\n"
             "        self.__key = 'token'              # mangled to _Pipeline__key\n"
             "    @classmethod\n    def from_dict(cls, d):\n        return cls(d['name'])\n"
             "    @staticmethod\n    def validate_name(n):\n        return n.isalnum()")]),
    SHORT("List the common file modes and explain why `with open(...)` is preferred.", 3, [
        B(["`r` read (error if missing), `w` write (creates or truncates), `a` append, `x` create (error if exists), "
           "`r+` read and write; add `b` for binary and `encoding='utf-8'` for text.",
           "`with` closes the file automatically, even when an exception occurs, so data is flushed and the handle is released."])]),
    SHORT("Define tokenization, stopwords, stemming and lemmatization (NLTK).", 5, [
        T(["Term", "Meaning", "Example"], [
            ["Tokenization", "Split text into words or sentences (`word_tokenize`)", "\"AI is fun\" -> ['AI','is','fun']"],
            ["Stopwords", "Very common words with little meaning (`stopwords.words('english')`)", "the, is, of"],
            ["Stemming", "Rule-based suffix chopping (`PorterStemmer`); output may not be a word", "studies -> studi"],
            ["Lemmatization", "Dictionary-based reduction to a valid base form (`WordNetLemmatizer`); better with a POS tag",
             "geese -> goose; `lemmatize('running', pos='v')` -> run"]], [0.18, 0.5, 0.32])]),
    SHORT("State the five classes of HTTP status codes and give one example for each.", 2, [
        P("1xx informational (100 Continue), 2xx success (200 OK, 201 Created), 3xx redirection (301 Moved Permanently), "
          "4xx client error (400, 401, 403, 404, 429), 5xx server error (500, 503).")]),
]

# ---------------------------------------------------------------------------------------------- LONG
STUDENT_TABLE = T(["Roll No", "Name", "CGPA", "Backlogs"], [
    ["26AIM1001", "Ananya Rao", "8.6", "0"], ["26AIM1002", "Rahul Verma", "7.8", "1"], ["26CSE1003", "Sneha Iyer", "9.1", "0"],
    ["26DSC1004", "Kabir Shah", "7.2", "0"], ["26ECE1005", "Meera Nair", "8.2", "0"]], [0.25, 0.35, 0.2, 0.2])
COMPANY_TABLE = T(["Company", "Minimum CGPA", "Openings"], [["TechNova", "8.0", "2"], ["DataWorks", "7.5", "1"],
                                                            ["CloudSys", "7.0", "3"]], [0.4, 0.3, 0.3])

c1_prompt = [
    P("A placement cell shortlists students for companies. A student is eligible for a company if the CGPA is at least the "
      "company's minimum and the student has no backlogs."),
    STUDENT_TABLE, COMPANY_TABLE,
    N(["Store the students and companies using suitable built-in data structures.",
       "Use conditional statements to find the eligible students for each company and keep them as sets.",
       "Using set operations, find the students eligible for all three companies, for none, and for CloudSys only.",
       "Use a priority queue (highest CGPA first) to shortlist students up to each company's openings.",
       "Using string handling, validate each roll number (2 digits, 3 letters, 4 digits) and extract the branch code.",
       "Handle the exception when a user asks about a company that is not in the dataset.",
       "Write the shortlists to a file, then read the file back and display it.",
       "Suggest where lists, tuples, dictionaries, sets, stacks, queues and priority queues can be applied in the system."]),
]
c1_answer = [
    H3("1. Choosing the structures"),
    T(["Data", "Structure", "Reason"], [
        ["Students", "`dict`: roll no -> `tuple (name, cgpa, backlogs)`", "O(1) lookup by roll number; a tuple is a fixed, read-only record"],
        ["Companies", "`dict`: name -> `tuple (min_cgpa, openings)`", "O(1) lookup by company; fixed record"],
        ["Eligible students", "`set` of roll numbers per company", "unique members and built-in set algebra"],
        ["Shortlist order", "`heapq` priority queue of `(-cgpa, roll)`", "pops the best CGPA first in O(log n)"]], [0.18, 0.4, 0.42]),
    H3("2. Eligibility and set operations"),
    P("A loop with an `if cgpa >= min_cgpa and backlogs == 0` test adds the roll number to the company's set. "
      "Then, with `E` the dictionary of eligible sets:"),
    B(["all three: `set.intersection(*E.values())`",
       "none: `all_students - set.union(*E.values())`",
       "CloudSys only: `E['CloudSys'] - E['TechNova'] - E['DataWorks']`"]),
    H3("3. Priority queue"),
    P("`heapq` is a min-heap, so each entry is pushed as `(-cgpa, roll)`. Popping repeatedly returns the highest CGPA first; "
      "stop after `openings` pops. The roll number acts as the tie-breaker."),
    H3("4. Strings, exception, file"),
    B(["Validation uses `len(roll) == 9`, `roll[:2].isdigit()`, `roll[2:5].isalpha()`, `roll[5:].isdigit()`; the branch is the slice `roll[2:5]`. "
       "A regular expression `^\\d{2}[A-Za-z]{3}\\d{4}$` does the same in one line.",
       "An unknown company raises a custom `CompanyNotFoundError`; `try / except / else / finally` reports it without crashing.",
       "`with open('shortlists.txt', 'w')` writes; reopening with `'r'` reads the content back."]),
    H3("5. Where each structure applies"),
    T(["Structure", "Use in this system"], [
        ["List", "Ordered shortlist for display; list of companies in application order"],
        ["Tuple", "Immutable student record; heap entries `(-cgpa, roll)`; `(company, openings)` pairs"],
        ["Dictionary", "Roll number -> student, company -> rules, company -> eligible set"],
        ["Set", "Eligibility, removing duplicate applications, set algebra across companies"],
        ["Stack", "Undo the last allocation; \"back\" navigation in the placement portal; checking nested rule expressions"],
        ["Queue (FIFO)", "Interview slots or application processing in arrival order"],
        ["Priority queue", "Ranking by CGPA; later, urgent or premium applications first"]], [0.2, 0.8]),
    CODE("m1_q1_placement.py"),
    OUT("m1_q1_placement.out.txt"),
]
c1_split = ("structures 2, eligibility and set operations 2, priority queue 2, strings 1, exception 1, file 1, "
            "applications of structures 1.")

# ---------------------------------------------------------------------------------------------- C2
c2_prompt = [
    P("A lightweight text editor must support: typing text (appended to the document), deleting the last n characters, "
      "undo and redo of the last operations, and saving to and loading from a file."),
    P("Propose an object-oriented design by identifying suitable classes, attributes and methods. Explain how two stacks "
      "implement undo and redo, how string handling performs the edits, and how exception handling (deleting more "
      "characters than exist, a missing file) and file handling make the editor reliable."),
    P("Trace this sequence and show the document text and both stacks after each step: "
      "`type(\"Hello\")`, `type(\" World\")`, `delete(5)`, `undo()`, `undo()`, `redo()`."),
]
c2_answer = [
    H3("1. Class design"),
    T(["Class", "Attributes", "Methods"], [
        ["`TextEditor`", "`_text: str`, `_undo: list` (stack), `_redo: list` (stack)",
         "`type_text(s)`, `delete(n)`, `undo()`, `redo()`, `save(path)`, `load(path)`, `text` (read-only property)"],
        ["`EditorError(Exception)`", "message", "raised for a bad delete length, empty undo or redo, and file problems"]],
      [0.2, 0.37, 0.43]),
    P("Each stack entry is a tuple `(kind, data)`: `('T', 'Hello')` for typing and `('D', 'World')` for a deletion. "
      "A deletion stores the removed text, because that is the only way to reverse it."),
    H3("2. How two stacks work"),
    N(["A new edit applies the change, pushes its record on the <b>undo</b> stack and clears the <b>redo</b> stack "
       "(a fresh edit makes the old redo history invalid).",
       "<b>Undo</b> pops the top of the undo stack, applies the reverse action (remove typed text, or re-append deleted text) "
       "and pushes the record on the redo stack.",
       "<b>Redo</b> pops the redo stack, re-applies the action and pushes it back on the undo stack.",
       "Both stacks are Python lists used LIFO: `append` to push, `pop` to pop, each O(1)."]),
    H3("3. Strings, exceptions, files"),
    B(["Strings are immutable, so every edit builds a new string: typing is `text + s`, deleting n characters is the slice "
       "`text[:len(text) - n]`, and the deleted part is `text[len(text) - n:]`. (`text[:-n]` is wrong when n is 0.)",
       "`delete(n)` raises `EditorError` when `n < 0` or `n > len(text)`; `undo` and `redo` raise `EditorError` on an empty stack.",
       "`save` uses `with open(path, 'w', encoding='utf-8')`. `load` catches `FileNotFoundError` and re-raises it as "
       "`EditorError('file not found')`; a successful load clears both stacks because the old history no longer matches the text."]),
    H3("4. Trace"),
    T(["Step", "Document text", "Undo stack (bottom to top)", "Redo stack"], [
        ["type(\"Hello\")", "Hello", "T:Hello", "empty"],
        ["type(\" World\")", "Hello World", "T:Hello, T: World", "empty"],
        ["delete(5)", "Hello (with trailing space)", "T:Hello, T: World, D:World", "empty"],
        ["undo()", "Hello World", "T:Hello, T: World", "D:World"],
        ["undo()", "Hello", "T:Hello", "D:World, T: World"],
        ["redo()", "Hello World", "T:Hello, T: World", "D:World"]], [0.17, 0.25, 0.33, 0.25]),
    CODE("m1_q2_editor.py"),
    OUT("m1_q2_editor.out.txt"),
]
c2_split = "classes and methods 3, two-stack logic 3, trace 2, string handling 1, exceptions and files 1."

# ---------------------------------------------------------------------------------------------- C3
c3_prompt = [
    P("A media company collects news headlines through a REST API (for example, `GET /headlines?category=tech`) and wants to "
      "find trending keywords. The application should send HTTP requests for several categories; handle network failures "
      "and invalid or empty JSON; use NLTK to tokenize each headline, remove stopwords and lemmatize; count keyword "
      "frequency per category and find keywords unique to one category; and save the top five keywords per category to a file."),
    P("Explain the complete workflow. Discuss how the API, NLTK, exception handling, dictionaries, sets and file handling "
      "work together to produce reliable results."),
]
c3_answer = [
    FLOW(["GET /headlines per category", "Check status and parse JSON", "NLTK: tokenize, drop stopwords, lemmatize",
          "Counter per category (dict)", "Sets: unique keywords", "Write top 5 to file"],
         "Workflow of the keyword application."),
    H3("1. Fetching"),
    B(["`requests.get(url, params={'category': cat}, timeout=5)`. The timeout is mandatory: without it a dead server hangs the program.",
       "`resp.raise_for_status()` turns 4xx and 5xx into `HTTPError`. `resp.json()` raises `ValueError` on invalid JSON. "
       "The code then checks that the key `headlines` exists and is a non-empty list.",
       "Network errors (`Timeout`, `ConnectionError`) are transient: retry a few times with a delay. A 404 or invalid JSON will not "
       "improve on retry, so skip that category and record the reason."]),
    T(["Failure", "Exception raised", "Action"], [
        ["Server unreachable or slow", "`ConnectionError`, `Timeout`", "retry (2 attempts here), then skip the category"],
        ["404 Not Found", "`HTTPError`", "skip, do not retry"],
        ["Body is not JSON", "`ValueError` (`JSONDecodeError`)", "skip category"],
        ["JSON without `headlines`", "`KeyError`", "skip category"],
        ["Empty list", "own `ApiError`", "skip category (nothing to count)"]], [0.28, 0.32, 0.4]),
    H3("2. NLTK pipeline"),
    P("For every headline: lower-case, `word_tokenize`, keep alphabetic tokens that are not in `stopwords.words('english')` "
      "(and are longer than two letters), then `WordNetLemmatizer().lemmatize`. This makes \"startups\" and \"startup\" count as one keyword."),
    H3("3. Dictionaries and sets"),
    B(["`counts = {category: Counter(...)}`. `Counter.most_common(5)` gives the top five.",
       "Keywords unique to a category: `set(counts[c]) - set().union(*other_counters)`. Keywords in every category are an intersection.",
       "Writing the file with mode `'w'` regenerates the report each run; `with` guarantees it is closed."]),
    WARN("`lemmatize()` assumes a noun unless you pass a POS tag, so the verb \"discuss\" becomes \"discus\" in the output below. "
         "Mention it in the viva: tag with `nltk.pos_tag` and map to WordNet POS for better lemmas."),
    CODE("m1_q3_headlines.py"),
    OUT("m1_q3_headlines.out.txt"),
    NOTE("The API is simulated by a mock session that returns genuine `requests.Response` objects, so the error handling "
         "shown is the same code that runs against a live service. The host name is a placeholder."),
]
c3_split = "workflow and API handling 3, NLTK pipeline 3, dict/set logic 2, exception handling 1, file output 1."

# ---------------------------------------------------------------------------------------------- C4
c4_prompt = [
    P("A hostel plans a chatbot using NLTK and ChatterBot to handle student complaints and queries. The chatbot should "
      "identify the complaint type from keywords (water, Wi-Fi, electricity, mess); treat urgent complaints (no water, "
      "power failure) before routine ones; answer common questions such as mess timings and the warden's contact; "
      "handle unclear or invalid messages; and log every complaint to a file."),
    P("Propose an object-oriented design with classes, attributes and methods. Explain how NLTK, ChatterBot, a priority "
      "queue, exception handling and file handling can be combined to improve accuracy and user experience."),
]
c4_answer = [
    H3("1. Class design"),
    T(["Class", "Attributes", "Methods / role"], [
        ["`Complaint`", "`cid`, `text`, `category`, `priority`", "`__str__`; one object per logged complaint"],
        ["`Classifier`", "category keyword sets, urgent tokens, lemmatizer", "`tokens(text)`, `category(tokens)`, `is_urgent(tokens)`"],
        ["`FaqBook`", "list of (required keywords, answer)", "`answer(tokens)` for mess timings, warden contact"],
        ["`ComplaintLog`", "file path, clock", "`write(complaint)` appends one line"],
        ["`HostelChatbot`", "classifier, FAQ book, heap, counter, optional ChatterBot", "`handle(message)`, `process_all()`"]],
      [0.17, 0.38, 0.45]),
    H3("2. How the technologies combine"),
    T(["Component", "Role", "Why it helps"], [
        ["NLTK", "lower-case, `word_tokenize`, lemmatize (\"timings\" -> \"timing\", \"leaks\" -> \"leak\")",
         "keyword matching works on base forms, so spelling variants still match"],
        ["Rules + dictionary", "keyword sets decide category; \"no\" + water, or \"power\" + failure, marks urgency",
         "predictable and explainable for complaints that must be routed correctly"],
        ["Priority queue", "`heapq` entries `(priority, arrival_no, complaint)`; urgent = 0, routine = 1",
         "urgent complaints are served first; the counter keeps routine ones in arrival order"],
        ["ChatterBot", "`ListTrainer` on greeting pairs; reply used only when `confidence >= 0.6`",
         "friendly small talk without letting it answer complaints; low confidence falls back to a clarification"],
        ["Exceptions", "`ValueError` for empty or non-text input; guarded optional import of ChatterBot",
         "the bot never crashes on bad input and still works if ChatterBot is missing"],
        ["File handling", "`ComplaintLog` appends `time | id | category | priority | text` (mode `'a'`)",
         "complete audit trail; the log can be re-read after a restart"]], [0.17, 0.43, 0.4]),
    P("Accuracy improves because lemmatization and tokenization remove surface differences; user experience improves because "
      "FAQs get an instant answer, unclear messages get a helpful prompt instead of a wrong guess, and urgent complaints are not "
      "stuck behind routine ones."),
    CODE("m1_q4_chatbot.py"),
    OUT("m1_q4_chatbot.out.txt"),
    NOTE("Tested with ChatterBot 1.2.15. That version needs the spaCy model: `pip install chatterbot`, then "
         "`python -m spacy download en_core_web_sm`. FAQ answers and phone extensions in the code are made-up sample data."),
]
c4_split = "class design 3, NLTK and rules 2, priority queue 2, ChatterBot 1, exceptions 1, file logging 1."

# ---------------------------------------------------------------------------------------------- C5
c5_prompt = [
    P("An application tracks the prices of several assets through a REST API. It should send HTTP GET requests at regular "
      "intervals; keep the last five readings of each asset as `(timestamp, price)` pairs; raise an alert when a price goes "
      "above an upper limit or below a lower limit; handle timeouts, HTTP errors (such as 404 and 429) and invalid JSON, "
      "retrying where sensible; and append every alert to a log file."),
    P("Explain the workflow. Discuss GET versus POST, the meaning of common status codes, JSON parsing, "
      "`try / except / else / finally`, and how lists, tuples, dictionaries, conditionals and file modes (r, w, a) work "
      "together to keep the system robust."),
]
c5_answer = [
    FLOW(["Timer: every N seconds", "GET price per asset", "Status check, retry rules", "Parse JSON, validate",
          "Store (time, price) in last-5 buffer", "Compare with limits, append alert"],
         "Workflow of the price alert application."),
    H3("1. GET versus POST"),
    P("Prices are read-only data, so the app uses <b>GET</b> with the asset in the query string (`?asset=BTC`). GET is safe and "
      "idempotent, so retrying cannot duplicate anything. POST would be used to create something, for example to register "
      "an alert subscription, and sends its data in the body; retrying a POST blindly can create duplicates."),
    H3("2. Status codes and retry policy"),
    T(["Code", "Meaning", "Action in this app"], [
        ["200 OK", "request succeeded", "parse JSON"],
        ["400 / 404", "bad request / unknown asset", "skip, do not retry (it will never succeed)"],
        ["401 / 403", "not authenticated / not allowed", "stop and fix the API key"],
        ["429", "too many requests", "wait for the `Retry-After` seconds, retry"],
        ["500 / 503", "server error / unavailable", "retry a limited number of times, with back-off"],
        ["Timeout (no code)", "no answer in time", "retry, then skip this cycle"]], [0.2, 0.32, 0.48]),
    H3("3. JSON parsing"),
    P("`resp.json()` converts the text into dict/list/float objects (JSON object -> dict, array -> list, number -> int or float, "
      "null -> None). Invalid text raises `ValueError`; a missing field raises `KeyError`; a non-numeric price raises `ValueError` "
      "or `TypeError` on `float(...)`. All three mean \"skip this reading\"."),
    H3("4. try / except / else / finally in `fetch_price`"),
    B(["<b>try</b>: GET, `raise_for_status`, parse.",
       "<b>except</b>: separate handlers for `Timeout`, `HTTPError` (branch on the code) and `ValueError/KeyError/TypeError`.",
       "<b>else</b>: returns the price only when nothing failed, so success logic is not mixed with error handling.",
       "<b>finally</b>: closes the response and releases the connection on every path."]),
    H3("5. Data structures, conditionals, file modes"),
    B(["`dict`: asset -> `deque(maxlen=5)`. A deque with `maxlen` drops the oldest reading automatically (a list with slicing `[-5:]` also works).",
       "`tuple (timestamp, price)`: an immutable reading.",
       "`if price > upper ... elif price < lower`: alert conditions. Limits are kept in a dict `asset -> (lower, upper)`.",
       "`open('alerts.log', 'a')`: append mode keeps earlier alerts. `'w'` would erase the history, and `'r'` is for reading it back."]),
    CODE("m1_q5_price_alerts.py"),
    OUT("m1_q5_price_alerts.out.txt"),
    NOTE("Prices come from a mock session that returns real `requests.Response` objects (timeouts, 429 with `Retry-After`, 404 and invalid JSON are scripted). "
         "A real app would wrap the loop in `time.sleep(interval)`."),
]
c5_split = "workflow 2, GET/POST and status codes 3, JSON and exception blocks 3, data structures and file modes 2."

# ---------------------------------------------------------------------------------------------- C6
c6_prompt = [
    P("A department stores student records in a CSV file and processes them in Python."),
    SNIP("reg_no,name,email,marks\nVL2026001,  asha nair ,asha@vit.ac.in,86\nVL2026002,Rohan Das,rohan.vit.ac.in,74\n"
         "VL2026003,Meena Rao,meena@vit.ac.in,abc\nVL2026004,Kabir Shah,kabir@vit.ac.in,58", lang="text"),
    N(["Design a `Person` class and a `Student` class that inherits from it, with attributes and methods for the record.",
       "Read the file using the `csv` module and create `Student` objects.",
       "Using string methods, strip and title-case each name, and validate the email (it must contain `@` and end in `.ac.in`).",
       "Grade with conditionals: 85 and above is A, 70 to 84 is B, 50 to 69 is C, below 50 is Fail.",
       "Handle malformed rows with exception handling (an invalid email or non-numeric marks). Skip them and log the reason to a file.",
       "Store the valid students in a list of objects and a dictionary keyed by register number.",
       "Save the final report as a JSON file using the `json` module.",
       "Explain how OOP, strings, exceptions and file handling work together here."]),
]
c6_answer = [
    H3("1. Class design (inheritance)"),
    T(["Class", "Attributes", "Methods"], [
        ["`Person`", "`name`, `email`", "`__init__` (cleans and validates), `__str__`"],
        ["`Student(Person)`", "inherits `name`, `email`; adds `reg_no`, `marks`",
         "`__init__` calls `super().__init__`, `grade()`, `to_dict()`"]], [0.2, 0.4, 0.4]),
    P("Validation lives in the constructors, so an invalid object can never exist (fail fast). `Student` reuses the name/email "
      "checks of `Person` through `super().__init__(...)`."),
    H3("2. Strings, grading, errors"),
    B(["`name.strip().title()` turns `\"  asha nair \"` into `\"Asha Nair\"`.",
       "Email rule: `\"@\" in email and email.endswith(\".ac.in\")`. `rohan.vit.ac.in` has no `@`, so it is rejected.",
       "`float(marks)` raises `ValueError` for `\"abc\"`; the constructor re-raises it with a clear message.",
       "Grade ladder: `if m >= 85: 'A' elif m >= 70: 'B' elif m >= 50: 'C' else 'Fail'` (order matters: test the highest bound first)."]),
    H3("3. File flow"),
    N(["`csv.DictReader` reads each row as a dict keyed by the header (open with `newline=''`).",
       "`try: Student(...)`, `except ValueError as err:` records `(line, reg_no, reason)`; `else:` appends to the list and the dict.",
       "`errors.log` is written with `'w'` (one fresh log per run); use `'a'` to accumulate across runs.",
       "`json.dump(report, f, indent=2)` writes the report: counts plus a list of `to_dict()` results."]),
    CODE("m1_q6_students.py"),
    OUT("m1_q6_students.out.txt"),
    H3("4. How the pieces work together"),
    P("OOP packages the data and the rules (constructor validation, `grade()`), inheritance avoids repeating the person checks, "
      "string methods clean raw text before it is stored, exceptions separate bad rows from good ones without stopping the run, and "
      "file handling provides the input (CSV), the audit trail (log) and the deliverable (JSON). Each layer is small and testable."),
]
c6_split = "class design 2, CSV and string handling 2, grading 1, exceptions and log 2, list and dict 1, JSON 1, explanation 1."

longs = [
    LONG("Campus placement shortlisting", 10, c1_prompt, c1_answer, c1_split),
    LONG("Text editor with undo and redo", 10, c2_prompt, c2_answer, c2_split),
    LONG("Trending keywords from news headlines", 10, c3_prompt, c3_answer, c3_split),
    LONG("Hostel complaint chatbot", 10, c4_prompt, c4_answer, c4_split),
    LONG("Asset price alert system", 10, c5_prompt, c5_answer, c5_split),
    LONG("Student record manager", 10, c6_prompt, c6_answer, c6_split),
]

MODULE_1 = MODULE(
    1, "Python data structures, OOP, APIs and NLP", "8 hours",
    "conditions and branching; list, tuple, dictionary, set; user-defined stack, queue, priority queue; string handling; "
    "exception handling; object-oriented concepts; APIs and data collection (simple and REST APIs, HTTP requests); file handling; "
    "frameworks and libraries: NLTK, ChatterBot.",
    [H3("Revision table: built-in and user-defined structures"),
     T(["Structure", "Mutable", "Ordered", "Duplicates", "Typical cost", "Use"], [
         ["list", "yes", "yes", "yes", "index O(1); `in` O(n); insert/pop(0) O(n); append O(1) amortised", "sequences, stack"],
         ["tuple", "no", "yes", "yes", "index O(1)", "fixed records, dict keys"],
         ["dict", "yes", "insertion order", "keys unique", "lookup, insert O(1) average", "key -> value lookup"],
         ["set", "yes", "no", "no", "membership O(1) average", "uniqueness, set algebra"],
         ["stack (list)", "yes", "LIFO", "yes", "push/pop at the end O(1)", "undo, recursion, parsing"],
         ["queue (deque)", "yes", "FIFO", "yes", "append / popleft O(1)", "scheduling, BFS"],
         ["priority queue (heapq)", "yes", "by priority", "yes", "push/pop O(log n); peek O(1)", "top-k, scheduling by importance"]],
       [0.17, 0.08, 0.12, 0.1, 0.33, 0.2])],
    mcqs, shorts, longs,
    exam_notes=[
        TIP("Module 1 questions in this bank are written as <b>mini case studies</b>, because that is how applied questions are usually framed: "
            "you must pick structures, justify them, then show code with output. Practise explaining <i>why</i> a structure fits."),
        WARN("Do not write \"tuple is faster than list\" as your only difference. State immutability, hashability and use."),
    ],
)
