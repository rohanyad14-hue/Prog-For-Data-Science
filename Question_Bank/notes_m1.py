from dsl import *
from notes_util import between, pick

# =====================================================================================================
sub_1_1 = SUB("1.1", "Conditions and branching", [
    B(["`if / elif / else` run the first branch whose condition is true; indentation (4 spaces) defines the block. Order the tests from most specific to least specific.",
       "Comparison: `== != < > <= >=`, chained `1 < x < 10`. Logical: `and or not`. Membership: `in`, `not in`. Identity: `is`.",
       "<b>Truthiness</b>: `0, 0.0, '', [], {}, set(), None` are false; everything else is true.",
       "`and` / `or` short-circuit and <b>return one of their operands</b>, not necessarily `True` or `False`.",
       "Conditional expression: `a if cond else b`. The `match` statement (Python 3.10+) does structural pattern matching."]),
    OUT("n1_basics.out.txt", "Verified output", transform=pick("truthiness", "if / elif")),
    QA("What does `print(0 or 'x', '' and 5, 3 and 4)` print?", [
        P("`x  4` (the middle item is the empty string, so there are two spaces). `0 or 'x'` returns the first truthy operand `'x'`; `'' and 5` stops at the first falsy operand and returns `''`; "
          "`3 and 4` has no falsy operand so it returns the last one, `4`.")], "predict the output"),
    QA("A grading function uses `if m >= 50: 'C' elif m >= 70: 'B' elif m >= 85: 'A'`. What is wrong?", [
        P("The first test already catches every mark of 50 or more, so `B` and `A` can never be returned. In the output above the wrong order gives `C, C, C, Fail` for 90, 75, 55, 30. "
          "Test the highest bound first: `>= 85`, then `>= 70`, then `>= 50`.")], "tricky"),
    QA("Why is `if x == None` discouraged, and when is `is` correct?", [
        P("`==` can be overridden by a class; `is` tests identity, and there is exactly one `None`, so write `x is None`. Use `is` only for `None`, `True`, `False`. "
          "For numbers and strings use `==` (identity of equal values is an implementation detail).")], "2 marks"),
    QA("Why does `0.1 + 0.2 == 0.3` give `False`, and how do you compare floats?", [
        P("Binary floating point cannot store 0.1 or 0.2 exactly, so the sum is 0.30000000000000004. Compare with a tolerance: `math.isclose(a, b)` (or `abs(a - b) < 1e-9`).")], "tricky"),
    QA("Rewrite `if n % 2 == 0: label = 'even' else: label = 'odd'` as one line.", [
        SNIP("label = 'even' if n % 2 == 0 else 'odd'    # condition goes in the middle")], "1 mark"),
])

# =====================================================================================================
sub_1_2 = SUB("1.2", "Lists", [
    B(["Ordered, mutable, allow duplicates, any mix of types. Implemented as a dynamic array of references.",
       "Indexing from 0, negative indexes from the end, slicing `a[start:stop:step]` (stop excluded) returns a new list."]),
    T(["Operation", "Cost", "Note"], [
        ["`a[i]`, `a[i] = x`, `len(a)`", "O(1)", ""],
        ["`a.append(x)`, `a.pop()`", "O(1) amortised", "work at the right end"],
        ["`a.insert(i, x)`, `a.pop(0)`, `del a[0]`", "O(n)", "every later element shifts"],
        ["`x in a`, `a.index(x)`, `a.count(x)`, `a.remove(x)`", "O(n)", "linear scan"],
        ["`a.sort()`, `sorted(a)`", "O(n log n)", "stable; `sort` returns None"],
        ["slice `a[i:j]`", "O(j - i)", "creates a new list"]], [0.5, 0.17, 0.33]),
    OUT("n1_basics.out.txt", "Verified output", transform=pick("list methods", "comprehensions")),
    OUT("n1_structures.out.txt", "Verified output", transform=pick("list:")),
    QA("Difference between `append` and `extend`? Between `a + b` and `a += b`?", [
        P("`append(x)` adds one element (even a list: `[1,2,3,[4,5]]`); `extend(it)` adds each element. `a + b` builds a new list; `a += b` extends `a` in place, so other names bound to `a` see the change.")], "2 marks"),
    QA("After `a = [3, 1, 2]; b = a; c = a[:]; b.append(9)`, what are `a` and `c`?", [
        P("`a` is `[3, 1, 2, 9]` and `c` is `[3, 1, 2]`. `b = a` copies the reference (same object); `a[:]` makes a new list. Check with `a is b` (True).")], "tricky"),
    QA("What does `grid = [[0] * 2] * 2; grid[0][0] = 1` give? How do you build a real 2 x 2 grid?", [
        P("`[[1, 0], [1, 0]]`: multiplication repeats the <i>same</i> inner list twice, so both rows are one object. Build rows independently with a comprehension: `[[0] * 2 for _ in range(2)]`.")], "tricky"),
    QA("What is the output of `bad(1), bad(2)` for `def bad(x, acc=[]): acc.append(x); return acc`?", [
        P("`[1, 2] [1, 2]`. The default list is created once, when the function is defined, and shared by all calls. Use `acc=None` and create the list inside (output above shows `good` returns `[1] [2]`).")], "tricky"),
    QA("What does `print(a.sort())` print and why?", [
        P("`None`. `list.sort()` sorts in place and returns `None`; `sorted(a)` returns a new sorted list. Writing `a = a.sort()` destroys your list.")], "tricky"),
    QA("Write a comprehension for the squares of the even numbers below 10, and one that labels each of 0..3 as even or odd.", [
        SNIP("[n * n for n in range(10) if n % 2 == 0]              # [0, 4, 16, 36, 64]   (filter AFTER the loop)\n"
             "['even' if n % 2 == 0 else 'odd' for n in range(4)]   # if-else goes BEFORE the loop")], "2 marks"),
    QA("Why is repeated `pop(0)` on a long list a performance bug?", [
        P("Each call shifts all remaining elements (O(n)). In the run above, 20,000 removals from the front of a 100,000-item list took about 3,300 ms with `list.pop(0)` and 1.3 ms with `deque.popleft()` (one machine, your numbers will differ).")], "2 marks"),
])

# =====================================================================================================
sub_1_3 = SUB("1.3", "Tuples", [
    B(["Ordered, <b>immutable</b>, allow duplicates. Created with commas: `(1, 2)`; a one-element tuple needs a trailing comma: `(5,)`.",
       "Hashable when every element is hashable, so tuples can be dictionary keys and set members.",
       "Typical uses: fixed records `(name, cgpa)`, returning several values, unpacking `a, b = b, a`, `first, *rest = t`, `collections.namedtuple` for named fields."]),
    OUT("n1_structures.out.txt", "Verified output", transform=pick("tuple")),
    QA("Differentiate list and tuple.", [
        T(["", "List", "Tuple"], [["Mutable", "yes", "no"], ["Syntax", "`[1, 2]`", "`(1, 2)` or `1, 2`"], ["Hashable", "no", "yes if items are"],
                                  ["Use", "collection that changes", "fixed record, dict key, return value"]], [0.2, 0.4, 0.4])], "3 marks"),
    QA("`t = ([1], 2)`. Does `t[0].append(3)` work? What does `t[0] += [4]` do?", [
        P("`t[0].append(3)` works: the tuple still holds the same list, and the list is mutable, giving `([1, 3], 2)`. `t[0] += [4]` raises `TypeError` because the assignment half tries to rebind `t[0]`, "
          "<b>but the list was already extended</b>, so `t` becomes `([1, 3, 4], 2)`. Immutability applies to the tuple's references, not to the objects they point to.")], "tricky"),
    QA("What is the type of `(5)` and of `(5,)`?", [P("`int` and `tuple`. The comma makes the tuple, not the brackets.")], "1 mark"),
    QA("Swap two variables without a temporary, and unpack `10, 20, 30` into a head and a tail.", [
        SNIP("x, y = y, x\nfirst, *rest = (10, 20, 30)     # first = 10, rest = [20, 30]")], "2 marks"),
])

# =====================================================================================================
sub_1_4 = SUB("1.4", "Dictionaries", [
    B(["Key-value mapping; keys unique and <b>hashable</b>; insertion order is preserved (Python 3.7+). Lookup, insert, delete are O(1) on average (hash table).",
       "`d[k]` raises `KeyError` if missing; `d.get(k, default)` does not; `d.setdefault(k, v)` inserts if missing; `d.items()`, `.keys()`, `.values()` are live views.",
       "`collections.defaultdict(list)` creates missing entries automatically; `collections.Counter` counts items.",
       "Merge: `d1 | d2` (3.9+) or `{**d1, **d2}`; later keys win. Comprehension: `{k: f(k) for k in xs}`."]),
    OUT("n1_structures.out.txt", "Verified output", transform=pick("dict")),
    QA("Why can a tuple but not a list be a dictionary key?", [
        P("Keys are located by their hash, which must not change. Lists are mutable and unhashable (`TypeError: unhashable type: 'list'`, shown above); a tuple of hashable items is hashable.")], "tricky"),
    QA("What happens if you add keys to a dictionary while looping over it?", [
        P("`RuntimeError: dictionary changed size during iteration`. Loop over a copy (`list(d)`) or build a new dict.")], "tricky"),
    QA("Count the words in a sentence with and without `Counter`.", [
        SNIP("counts = {}\nfor w in text.split():\n    counts[w] = counts.get(w, 0) + 1\n\nfrom collections import Counter\nCounter(text.split()).most_common(2)")], "2 marks"),
    QA("Difference between `d[k]`, `d.get(k)` and `d.setdefault(k, v)`.", [
        P("`d[k]` raises `KeyError` when missing; `d.get(k)` returns `None` (or a given default) and does not change `d`; `setdefault` returns the value and <i>inserts</i> `v` when the key is missing.")], "2 marks"),
    QA("Why is dictionary lookup O(1) on average but not always?", [
        P("A hash maps the key to a slot. Collisions (two keys, same slot) are resolved by probing, so the cost is constant on average and degrades only when many keys collide.")], "2 marks"),
])

# =====================================================================================================
sub_1_5 = SUB("1.5", "Sets", [
    B(["Unordered collection of unique, hashable items; membership test O(1) on average. `{}` is an empty <b>dict</b>; use `set()` for an empty set.",
       "Algebra: union `|`, intersection `&`, difference `-`, symmetric difference `^`, subset `<=`. `frozenset` is the immutable version (usable as a dict key).",
       "Use for removing duplicates, fast membership, and comparing groups (eligible-for-all, eligible-for-none questions)."]),
    OUT("n1_structures.out.txt", "Verified output", transform=pick("set", "membership")),
    QA("What are `type({})` and `type(set())`?", [P("`dict` and `set`. There is no literal for an empty set.")], "tricky"),
    QA("Why can a set contain tuples but not lists?", [P("Set members must be hashable; lists are mutable and unhashable (`TypeError`, shown above).")], "2 marks"),
    QA("Given A = {1,2,3,4} and B = {3,4,5}, evaluate A|B, A&B, A-B, A^B.", [
        P("`{1,2,3,4,5}`, `{3,4}`, `{1,2}`, `{1,2,5}` (see the output).")], "2 marks"),
    QA("Why is a set preferred over a list for 'is this roll number registered?'", [
        P("Hashing gives O(1) average membership. In the run above a worst-case lookup in a 100,000-item list took about 0.67 ms per call against roughly 0.00007 ms for the set (about 10,000 times faster on this machine).")], "2 marks"),
])

# =====================================================================================================
sub_1_6 = SUB("1.6", "Mutability, aliasing and copying (cross-cutting traps)", [
    T(["Immutable", "Mutable"], [["`int, float, bool, str, tuple, frozenset, bytes, None`", "`list, dict, set, bytearray`, most user-defined objects"]], [0.5, 0.5]),
    B(["Python passes <b>references to objects</b> (\"pass by object reference\"). A function can mutate a mutable argument; rebinding the parameter name changes only the local name.",
       "`b = a` shares the object. `a.copy()` / `a[:]` / `list(a)` make a <b>shallow</b> copy (new outer container, same inner objects). `copy.deepcopy(a)` copies everything."]),
    OUT("n1_basics.out.txt", "Verified output", transform=pick("how arguments")),
    OUT("n1_structures.out.txt", "Verified output", transform=pick("shallow")),
    QA("Predict `data` and `num` after `grow(data)`, `rebind(data)`, `bump(num)` for the three functions in the output.", [
        P("`[1] 5`. `grow` mutates the caller's list; `rebind` assigns a new list to the local name only; `bump` makes a new int because ints are immutable.")], "predict the output"),
    QA("`nested = [[1, 2], [3]]; sh = nested.copy(); nested[0].append(99)`. What is `sh`?", [
        P("`[[1, 2, 99], [3]]`. A shallow copy duplicates only the outer list; the inner lists are shared. `copy.deepcopy(nested)` would still be `[[1, 2], [3]]`.")], "tricky"),
    QA("When do you use `==` and when `is`?", [P("`==` compares values, `is` compares identity (same object). Use `is` for `None` only.")], "1 mark"),
])

# =====================================================================================================
sub_1_7 = SUB("1.7", "Stack (user-defined structure)", [
    B(["LIFO: last in, first out. Operations: `push`, `pop`, `peek`, `is_empty`, `size`, all O(1) when the top is the <i>end</i> of a list.",
       "Applications: undo/redo, function-call stack and recursion, bracket matching, expression evaluation and conversion, back button, depth-first search."]),
    CODE("n1_queues.py", "Stack, Queue and PriorityQueue classes (from n1_queues.py)", transform=between("class Stack", "return heapq.heappop(self._h)[2]")),
    OUT("n1_queues.out.txt", "Verified output", transform=pick("stack (LIFO)", "user-defined")),
    QA("Write a stack class with `push`, `pop`, `peek`, `is_empty`; what should `pop` do on an empty stack?", [
        P("See the class above. Raise a clear exception (`IndexError('pop from empty stack')`) instead of returning a silent value; the caller can catch it.")], "5 marks"),
    QA("Check whether the brackets in a string are balanced using a stack.", [
        P("Push every opening bracket; for each closing bracket pop and compare with the matching opener; the string is balanced if no mismatch occurs and the stack is empty at the end. "
          "Output above: `{[()]}` True, `([)]` False, `((` False, empty string True.")], "5 marks"),
    QA("How are two stacks used for undo and redo?", [
        P("Every new edit goes on the undo stack and clears the redo stack; undo pops the undo stack and pushes the same action on the redo stack; redo does the reverse (see the question bank, M1-C2).")], "3 marks"),
])

sub_1_8 = SUB("1.8", "Queue (user-defined structure)", [
    B(["FIFO: first in, first out. Operations `enqueue` (append at the rear) and `dequeue` (remove at the front).",
       "Use `collections.deque`: `append` and `popleft` are O(1). `deque(maxlen=n)` keeps only the newest n items; `rotate(k)` rotates.",
       "`queue.Queue` (FIFO), `LifoQueue` (stack) and `PriorityQueue` are the <b>thread-safe</b> versions for producer/consumer programs.",
       "Applications: CPU/job scheduling, printer spooling, breadth-first search, buffering, call-centre waiting lines."]),
    OUT("n1_queues.out.txt", "Verified output", transform=pick("queue (FIFO)", "library queues")),
    QA("Why should a queue not be built with `list.pop(0)`?", [P("It is O(n) per removal because every item shifts; `deque.popleft()` is O(1). Measured above: about 3,300 ms versus 1.3 ms for 20,000 removals.")], "2 marks"),
    QA("What is a circular queue and why is it used?", [
        P("A fixed-size array treated as a ring, with `front` and `rear` indexes that wrap around using modulo. It reuses freed slots, avoiding the wasted space of a plain array queue. "
          "`deque(maxlen=n)` behaves similarly for a buffer of the latest n items.")], "3 marks"),
    QA("Difference between `collections.deque` and `queue.Queue`.", [P("`deque` is a fast single-thread container. `queue.Queue` adds locking so several threads can `put` and `get` safely, and can block or time out.")], "2 marks"),
    QA("Compare a stack and a queue.", [
        T(["", "Stack", "Queue"], [["Order", "LIFO", "FIFO"], ["Insert / remove", "same end (top)", "rear / front"], ["Python", "list `append`/`pop`", "`deque` `append`/`popleft`"],
                                   ["Uses", "undo, recursion, brackets", "scheduling, BFS, buffering"]], [0.2, 0.4, 0.4])], "3 marks"),
])

sub_1_9 = SUB("1.9", "Priority queue and heapq", [
    B(["Each item has a priority; the item with the best priority leaves first. Python: `heapq` keeps a list arranged as a binary <b>min-heap</b>.",
       "`heappush`, `heappop` O(log n); `h[0]` (peek) O(1); `heapify(list)` O(n); `nlargest(k, xs)`, `nsmallest`.",
       "Max-heap: push negated priorities. Ties: `(priority, counter, item)` keeps arrival order and avoids comparing the items themselves.",
       "A heap list is <b>not sorted</b>; only `h[0]` is guaranteed smallest (parent <= children)."]),
    OUT("n1_queues.out.txt", "Verified output", transform=pick("priority queue with heapq", "tie-breaking")),
    QA("`data = [5, 3, 8, 1, 9, 2]; heapq.heapify(data)`. Is `data` now sorted?", [
        P("No. It is `[1, 3, 2, 5, 9, 8]`: a valid heap (every parent <= its children) with the minimum at index 0. Repeated `heappop` returns sorted order.")], "tricky"),
    QA("Two tasks have the same priority and the second field is a custom object. What goes wrong with `heappush((1, obj))`?", [
        P("When priorities tie, Python compares the next tuple field; objects without `__lt__` raise `TypeError: '<' not supported between instances of 'Job' and 'Job'`. "
          "Insert a unique counter as the second field: `(priority, next(counter), obj)`, which also gives first-come-first-served among equals.")], "tricky"),
    QA("How do you get highest-priority-first (a max-heap) from `heapq`?", [P("Push the negated priority, e.g. `(-cgpa, roll)`, and negate again after popping.")], "2 marks"),
    QA("Where is a priority queue used?", [P("CPU scheduling, Dijkstra and A* shortest paths, event simulation, hospital triage, top-k queries, merging sorted streams, the urgent-before-routine complaint chatbot.")], "2 marks"),
])

# =====================================================================================================
sub_1_10 = SUB("1.10", "String handling", [
    B(["Immutable sequences of Unicode characters; every 'change' creates a new string. Slicing and indexing like lists: `s[::-1]` reverses.",
       "Cleaning: `strip lstrip rstrip lower upper title casefold replace`. Splitting: `split rsplit partition splitlines`; joining: `sep.join(items)`.",
       "Searching: `find` (returns -1) vs `index` (raises `ValueError`); `startswith/endswith(tuple)`; `count`. Tests: `isdigit isalpha isalnum isspace`.",
       "Formatting: f-strings `f'{x:.2f}'`, `format`, `%`. Padding: `zfill`, `center`, `ljust`, width specifiers `{x:>8}`."]),
    OUT("n1_strings_exceptions.out.txt", "Verified output", transform=pick("strings")),
    QA("What does `'xxhixx'.strip('x')` return? What does `'abcabc'.strip('ba')` return?", [
        P("`'hi'` and `'cabc'`. The argument is a <i>set of characters</i> to remove from both ends, not a prefix string.")], "tricky"),
    QA("Difference between `find` and `index`; `split()` and `split(' ')`.", [
        P("`find` returns -1 when absent, `index` raises `ValueError`. `' a  b '.split()` splits on any run of whitespace and ignores the ends: `['a','b']`; "
          "`' a  b '.split(' ')` keeps empty strings: `['', 'a', '', 'b', '']`.")], "tricky"),
    QA("Why does `s[0] = 'x'` fail, and how do you change a character?", [
        P("Strings are immutable (`TypeError`). Build a new string: `s = 'x' + s[1:]` or `s.replace(...)`.")], "2 marks"),
    QA("Format `8.4567` to two decimals right-aligned in width 8, and a percentage.", [
        SNIP("f'{gpa:8.2f}'      # '    8.46'\nf'{0.256:.1%}'     # '25.6%'\nf'{1234567:,}'     # '1,234,567'")], "2 marks"),
    QA("Validate a roll number of the form 2 digits + 3 letters + 4 digits using string methods.", [
        SNIP("ok = len(r) == 9 and r[:2].isdigit() and r[2:5].isalpha() and r[5:].isdigit()\nbranch = r[2:5] if ok else None")], "3 marks"),
])

# =====================================================================================================
sub_1_11 = SUB("1.11", "Exception handling", [
    B(["`try` (risky code) / `except Type as e` (handle) / `else` (no exception happened) / `finally` (always runs). Raise with `raise`; chain with `raise New from old`.",
       "Handlers are checked top to bottom: put <b>specific</b> exceptions before general ones. A bare `except:` also catches `KeyboardInterrupt`; prefer `except Exception`.",
       "Hierarchy: `BaseException` > `Exception` > `ArithmeticError` (`ZeroDivisionError`), `LookupError` (`IndexError`, `KeyError`), `ValueError`, `TypeError`, `OSError` (`FileNotFoundError`).",
       "Custom exception: `class AppError(Exception): ...`. Context managers (`with`) release resources even on errors."]),
    OUT("n1_strings_exceptions.out.txt", "Verified output", transform=pick("exceptions", "hierarchy", "custom")),
    QA("What is printed by `parse(None)` for the function in the output and in what order do the messages appear?", [
        P("`TypeError/KeyError`, preceded by the `finally` message. The `finally` block runs for every call, even when `except` returns.")], "predict the output"),
    QA("What does `g()` return: `try: return 'from try'  finally: return 'from finally'`?", [
        P("`'from finally'`. A `return` in `finally` overrides the earlier return (and can even swallow an exception); avoid it.")], "tricky"),
    QA("Explain the roles of `else` and `finally`.", [
        P("`else` runs only if the `try` block finished without raising; it keeps success code out of the guarded block. `finally` always runs (after return, break or an unhandled exception) and is for clean-up.")], "3 marks"),
    QA("Why is the order `except Exception` then `except ValueError` a mistake?", [
        P("`Exception` catches everything first, so the more specific handler is unreachable. Order handlers from most specific to most general.")], "2 marks"),
    QA("How do you define and raise a custom exception with data, and chain an error?", [
        P("Subclass `Exception`, pass a message to `super().__init__`, store extra attributes (`balance`, `amount` in the output). `raise RuntimeError('config invalid') from e` keeps the original error as `__cause__`.")], "3 marks"),
])

# =====================================================================================================
sub_1_12 = SUB("1.12", "Object-oriented concepts", [
    B(["<b>Class</b> = blueprint; <b>object</b> = instance. `__init__(self, ...)` initialises an instance; `self` is the instance.",
       "<b>Encapsulation</b>: `name` public, `_name` protected by convention, `__name` name-mangled to `_Class__name` (discourages access, not real privacy); `@property` for controlled access.",
       "<b>Inheritance</b>: `class B(A)`, `super().__init__()`. Python allows multiple inheritance; the method resolution order (MRO) uses C3 linearization.",
       "<b>Polymorphism</b>: same method name, different behaviour (overriding, duck typing). <b>Abstraction</b>: `abc.ABC` with `@abstractmethod` cannot be instantiated.",
       "`@classmethod` gets the class (`cls`), `@staticmethod` gets nothing. Dunder methods: `__str__`, `__repr__`, `__eq__` (define `__hash__` too), `__lt__`, `__add__`, `__len__`."]),
    OUT("n1_oop.out.txt", "Verified output", transform=pick("class attribute", "encapsulation", "inheritance", "multiple")),
    OUT("n1_oop.out.txt", "Verified output (continued)", transform=pick("classmethod", "duck")),
    QA("A class has `items = []` at class level and `add` appends to `self.items`. What goes wrong with two objects?", [
        P("`items` is a class attribute shared by every instance, so `b2.items` shows what `b1` added (output: `Bad : ['x']`). Create the list in `__init__` (`self.items = []`).")], "tricky"),
    QA("What is name mangling? Is `__balance` really private?", [
        P("Inside `class Account`, `self.__balance` is stored as `_Account__balance`. Outside, `acc.__balance` raises `AttributeError`, but `acc._Account__balance` still works, so it prevents accidental clashes only.")], "3 marks"),
    QA("For `class D(B, C)` where both extend `A`, in what order are `who()` methods called, and why?", [
        P("`D > B > C > A`. The MRO from C3 linearization is `[D, B, C, A, object]`, and each `super()` call moves one step along it. Compare Scala trait linearization, which orders mix-ins right to left.")], "tricky"),
    QA("What happens if you try `Shape()` where `Shape` has an `@abstractmethod`?", [
        P("`TypeError: Can't instantiate abstract class Shape with abstract method area`. Subclasses must implement the method.")], "2 marks"),
    QA("Difference between `@classmethod`, `@staticmethod` and an instance method.", [
        T(["", "First parameter", "Typical use"], [["instance method", "`self`", "work on one object's data"], ["`@classmethod`", "`cls`", "alternative constructors (`Temp.from_f`)"],
                                                   ["`@staticmethod`", "none", "utility related to the class (`Temp.is_valid`)"]], [0.25, 0.25, 0.5])], "3 marks"),
    QA("Why define `__hash__` when you define `__eq__`?", [
        P("Defining `__eq__` alone makes instances unhashable. Objects that compare equal must have equal hashes if they are to be used in sets or as dict keys (output: `in set: 1`).")], "tricky"),
])

# =====================================================================================================
sub_1_13 = SUB("1.13", "APIs, REST and HTTP requests", [
    B(["An <b>API</b> is a contract for programs to talk to each other. A <b>REST API</b> exposes <i>resources</i> at URLs and uses HTTP methods; it is stateless (each request carries everything needed), usually returns JSON.",
       "URL anatomy: `https://host/items/3?category=tech&page=2` = scheme, host, <b>path</b> (identifies the resource), <b>query string</b> (filters). Requests also have headers (`Authorization`, `Content-Type`) and an optional body.",
       "<b>Safe</b> methods do not change data (GET). <b>Idempotent</b> methods give the same result when repeated (GET, PUT, DELETE). POST is neither."]),
    T(["Method", "Meaning", "Typical success code"], [["GET", "read a resource or list", "200"], ["POST", "create a resource", "201 Created + `Location`"], ["PUT", "replace a resource", "200 / 204"],
                                                   ["PATCH", "change part of a resource", "200"], ["DELETE", "remove", "204 No Content"]], [0.15, 0.55, 0.3]),
    T(["Class", "Meaning", "Examples"], [["2xx", "success", "200 OK, 201 Created, 204 No Content"], ["3xx", "redirection", "301, 302, 304"],
                                          ["4xx", "client error (fix the request)", "400 Bad Request, 401 Unauthorized, 403 Forbidden, 404 Not Found, 429 Too Many Requests"],
                                          ["5xx", "server error (maybe retry)", "500, 502, 503, 504"]], [0.1, 0.3, 0.6]),
    OUT("n1_files_rest.out.txt", "Verified output (real requests to a local server)", transform=pick("GET with query", "status codes", "errors:")),
    QA("Differentiate GET and POST; PUT and POST.", [
        P("GET reads and puts parameters in the URL; it is safe and idempotent. POST creates and sends a body; repeating it can create duplicates (the output shows `POST /items -> 201 Created Location=/items/3`). "
          "PUT replaces a known resource at a known URL and is idempotent: sending the same PUT twice leaves the same state.")], "3 marks"),
    QA("Why does the printed URL contain `q=a+b%26c`?", [
        P("`requests` URL-encodes `params`: a space becomes `+` (or `%20`) and `&` becomes `%26` so that it cannot be mistaken for the separator between parameters.")], "tricky"),
    QA("A call returns 429 with `Retry-After: 1`. What should the client do? What about a 404, a 401, a 500?", [
        P("429: wait the given time and retry. 404: the resource does not exist, do not retry. 401: authentication missing or wrong (add the `Authorization: Bearer ...` header). "
          "500/503: server problem, retry a limited number of times with back-off. The output shows the local server rejecting two calls with 429, then accepting the third.")], "3 marks"),
    QA("Which exceptions can `requests.get` raise, and what does `raise_for_status()` do?", [
        P("`Timeout` (`ConnectTimeout`, `ReadTimeout`), `ConnectionError`, `HTTPError` (only after `raise_for_status()`), `JSONDecodeError`/`ValueError` from `.json()`. "
          "`raise_for_status()` turns a 4xx/5xx response into `HTTPError`; without it a 404 is just a response with `status_code == 404`. Always pass `timeout=`: without it a hung server blocks forever.")], "3 marks"),
    QA("What is the difference between `r.text` and `r.json()`?", [P("`r.text` is the body as a string; `r.json()` parses it into dict/list/numbers and raises `ValueError` if the body is not valid JSON (the `/bad-json` test above).")], "2 marks"),
    QA("What are `requests.Session`, query parameters versus path parameters, and an API key?", [
        P("A `Session` reuses the TCP connection and default headers across calls (faster, and carries the token). A path parameter identifies a resource (`/items/3`); query parameters filter or page (`?category=tech`). "
          "An API key or bearer token in a header identifies the caller; never hard-code it in source code (use an environment variable).")], "3 marks"),
])

# =====================================================================================================
sub_1_14 = SUB("1.14", "File handling (text, CSV, JSON)", [
    B(["`open(path, mode, encoding='utf-8')`. Modes: `r` read (error if missing), `w` write (<b>truncates</b>), `a` append, `x` create (error if exists), `r+` read and write, `b` binary.",
       "Prefer `with open(...) as f:` so the file closes automatically, even after an error. Read big files by iterating (`for line in f`).",
       "`csv.DictReader/DictWriter` handle quoting (open with `newline=''`); `json.dump/load` use files, `json.dumps/loads` use strings.",
       "JSON limits: tuples become lists, dict keys become strings, single quotes are invalid."]),
    OUT("n1_files_rest.out.txt", "Verified output", transform=pick("file modes", "reading styles", "csv and json")),
    QA("What does opening an existing file with mode `'w'` do?", [P("It truncates it to zero length immediately, before you write anything (output: size 0). Use `'a'` to keep the content.")], "tricky"),
    QA("Compare `read()`, `readline()`, `readlines()` and iterating over the file.", [
        P("`read()` returns the whole text; `readline()` one line (with `\\n`); `readlines()` a list of all lines; iterating yields one line at a time and is memory friendly for large files.")], "3 marks"),
    QA("Why can `f.seek(6)` land in the wrong place on Windows in text mode?", [
        P("Windows writes `\\n` as `\\r\\n`, so byte offsets differ from character counts; in the output `seek(6); read(5)` returned `'\\nline'` instead of `'line2'`. In text mode only seek to 0 or to a value returned by `tell()`.")], "tricky"),
    QA("What changes when a Python object goes through `json.dumps` and `json.loads`?", [
        P("`{'id': 1, 'tags': ('a','b'), 2: 'int key', 'ok': True, 'none': None}` comes back as `{'id': 1, 'tags': ['a','b'], '2': 'int key', 'ok': True, 'none': None}`: tuple to list, int key to string; `True`/`None` map to `true`/`null` in the text.")], "tricky"),
    QA("Why does a CSV field `Kabir, S` not break the file?", [P("`csv.writer` wraps fields that contain the delimiter in quotes (`\"Kabir, S\"`), and `csv.reader` removes them again. Splitting on commas yourself would break it.")], "2 marks"),
])

# =====================================================================================================
sub_1_15 = SUB("1.15", "NLTK (natural language processing)", [
    B(["Pipeline: raw text > sentence/word tokenization > lower-casing > remove punctuation and stopwords > stem or lemmatize > features (counts, TF-IDF) > model.",
       "<b>Stemming</b> chops suffixes by rules (`PorterStemmer`, `LancasterStemmer`; output may not be a word). <b>Lemmatization</b> maps to a dictionary form (`WordNetLemmatizer`) and needs the part of speech to be accurate.",
       "POS tagging: `pos_tag(tokens)` gives Penn Treebank tags (NN noun, VB verb, JJ adjective, RB adverb). `FreqDist` counts tokens; `bigrams`/`ngrams` make n-grams.",
       "Vectorisation (scikit-learn): bag of words counts; TF-IDF = term frequency x inverse document frequency, so words found in few documents weigh more.",
       "Data packages needed once: `punkt_tab`, `stopwords`, `wordnet`, `averaged_perceptron_tagger_eng` (`nltk.download`)."]),
    OUT("n1_nlp.out.txt", "Verified output", transform=pick("tokenization", "cleaning", "stemming", "POS")),
    OUT("n1_nlp.out.txt", "Verified output (continued)", transform=pick("frequency", "bag of words")),
    QA("Stemming versus lemmatization: compare the outputs for `studies, studying, geese, running, better, was`.", [
        T(["word", "Porter stem", "default lemma", "lemma with POS"], [["studies", "studi", "study", "-"], ["studying", "studi", "studying", "study (v)"], ["geese", "gees", "goose", "-"],
                                                                        ["running", "run", "running", "run (v)"], ["better", "better", "better", "good (a)"], ["was", "wa", "wa", "be (v)"]],
          [0.2, 0.25, 0.25, 0.3]),
        P("Stemming is faster but can produce non-words (`studi`, `wa`). Lemmatization returns real words but treats every word as a noun unless you pass the POS: `lemmatize('better', 'a')` gives `good`.")], "tricky"),
    QA("Why can removing stopwords hurt sentiment analysis?", [
        P("The NLTK English list contains negations such as `not` (checked above: True), so 'not good' becomes 'good'. Keep negations or use a custom list.")], "tricky"),
    QA("How does `word_tokenize` treat \"isn't\" and \"Rao's\"?", [P("As `is`, `n't` and `Rao`, `'s` (Treebank tokenizer), and punctuation becomes separate tokens. Filter with `token.isalpha()` if you only want words.")], "2 marks"),
    QA("Explain TF-IDF with the three-document example.", [
        P("TF-IDF weights a word by how often it occurs in a document and how rare it is across documents. In the output the words found in only one document (`games`, `is`, `needs`) have the highest idf (1.69) "
          "and words in two documents have 1.29, so a common word contributes less to a document's vector.")], "3 marks"),
    QA("List the steps to clean headlines for keyword counting.", [P("Lower-case, `word_tokenize`, keep alphabetic tokens, drop stopwords and very short words, lemmatize (with POS if possible), count with `Counter`.")], "3 marks"),
])

sub_1_16 = SUB("1.16", "ChatterBot", [
    B(["ChatterBot is a <b>retrieval</b> chatbot library: it finds the stored statement most similar to the input and returns a stored reply. It does not generate new sentences (version 1.2 adds experimental LLM adapters).",
       "<b>Training</b>: `ListTrainer` (list of alternating statements and replies), `ChatterBotCorpusTrainer` (ready-made corpora), `CsvFileTrainer`, `JsonFileTrainer`, `UbuntuCorpusTrainer`.",
       "<b>Logic adapters</b> choose the reply: `BestMatch` (default), `TimeLogicAdapter`, `MathematicalEvaluation`, `SpecificResponseAdapter`, `UnitConversion`. <b>Storage adapters</b>: `SQLStorageAdapter` (SQLite by default), MongoDB, Redis, Django.",
       "Similarity is computed by a comparison class; in the installed 1.2.15 the default is `LevenshteinDistance` (edit distance). `BestMatch` stops searching at `maximum_similarity_threshold` (default 0.95).",
       "Every response carries a `confidence` between 0 and 1. `read_only=True` stops the bot from learning from live conversations. 1.2 needs the spaCy model `en_core_web_sm`."]),
    OUT("n1_chatterbot.out.txt", "Verified output (ChatterBot 1.2.15)"),
    QA("How does ChatterBot decide what to reply?", [
        P("It preprocesses the input, searches its stored statements for the closest match (Levenshtein similarity by default), picks a stored response to that statement (first one by default), and returns it with a confidence score. "
          "In the output 'what are the mess timing' (a typo) still matches the trained question with confidence 0.96.")], "5 marks"),
    QA("Why did 'tell me a joke' get the default reply?", [P("Nothing in the training data was similar enough, so the `BestMatch` adapter returned its `default_response` with confidence 0.00. For production, use the confidence value to fall back to a menu or a human.")], "2 marks"),
    QA("What are the limitations of ChatterBot for a complaint system?", [
        P("It only repeats what it was trained on, has no memory of intent, and can answer confidently with a wrong stored reply. Complaint type and urgency are better handled by explicit rules or a classifier "
          "(NLTK keywords), with ChatterBot only for FAQs and small talk, which is how the hostel chatbot in the question bank is built.")], "3 marks"),
])

NOTES_1 = NMODULE(
    1, "Python data structures, OOP, APIs and NLP", "8 hours",
    "conditions and branching; list, tuple, dictionary, set; stack, queue, priority queue; string handling methods; exception handling; object-oriented concepts; APIs and data collection, simple and REST APIs, HTTP requests; file handling; NLTK; ChatterBot.",
    [("Condition and branching statements", "1.1"), ("Built-in data structures: list, tuple, dictionary, set", "1.2 to 1.5 (copying traps: 1.6)"),
     ("User-defined data structures: stack, queue, priority queue", "1.7, 1.8, 1.9"), ("String handling methods", "1.10"), ("Exception handling", "1.11"),
     ("Object-oriented concepts", "1.12"), ("APIs and data collection, simple API and REST APIs, HTTP requests", "1.13"), ("File handling, read/write", "1.14"),
     ("Frameworks and libraries: NLTK, ChatterBot", "1.15, 1.16")],
    [sub_1_1, sub_1_2, sub_1_3, sub_1_4, sub_1_5, sub_1_6, sub_1_7, sub_1_8, sub_1_9, sub_1_10, sub_1_11, sub_1_12, sub_1_13, sub_1_14, sub_1_15, sub_1_16],
)
