"""Notes M1: list / tuple / dict / set behaviours and the classic traps."""
import copy
import timeit
from collections import Counter, defaultdict, namedtuple

print("--- list: aliasing, copies, sort ---")
a = [3, 1, 2]
b = a                       # same object
c = a[:]                    # new list (shallow copy)
b.append(9)
print("a =", a, "| c =", c, "| a is b:", a is b)
print("sorted(a) ->", sorted(a), "| a unchanged:", a)
print("a.sort() returns", a.sort(), "| a is now", a)
s = list(range(10))
print("s[2:8:2] =", s[2:8:2], "| s[::-1] =", s[::-1], "| s[-3:] =", s[-3:])

print("\n--- mutable default argument ---")
def bad(x, acc=[]):
    acc.append(x)
    return acc
def good(x, acc=None):
    acc = [] if acc is None else acc
    acc.append(x)
    return acc
print("bad(1), bad(2)   ->", bad(1), bad(2))
print("good(1), good(2) ->", good(1), good(2))

print("\n--- shallow vs deep copy, list multiplication ---")
nested = [[1, 2], [3]]
shallow, deep = nested.copy(), copy.deepcopy(nested)
nested[0].append(99)
print("shallow:", shallow, "| deep:", deep)
grid = [[0] * 2] * 2
grid[0][0] = 1
print("[[0]*2]*2 then grid[0][0]=1 ->", grid, "(rows are the same object)")
grid = [[0] * 2 for _ in range(2)]
grid[0][0] = 1
print("comprehension version        ->", grid)

print("\n--- tuple ---")
t = ([1], 2)
t[0].append(3)
print("append inside a tuple's list works:", t)
try:
    t[0] += [4]
except TypeError as err:
    print("t[0] += [4] raises TypeError:", err, "| but t is now", t)
print("one-item tuple:", (5,), type((5,)).__name__, type((5)).__name__)
x, y = 1, 2
x, y = y, x
first, *rest = (10, 20, 30)
print("swap:", x, y, "| unpack:", first, rest)
P = namedtuple("P", "name cgpa")
p = P("Asha", 8.6)
print("namedtuple:", p, p.name, p[1])

print("\n--- dict ---")
d = {"a": 1}
print("get missing:", d.get("z"), d.get("z", 0))
d.setdefault("b", []).append(1)
print("setdefault:", d)
dd = defaultdict(list)
for w in "to be or not to be".split():
    dd[w[0]].append(w)
print("defaultdict:", dict(dd))
print("Counter:", Counter("to be or not to be".split()).most_common(2))
try:
    for k in d:
        d[k + "x"] = 0
except RuntimeError as err:
    print("modify while iterating ->", err)
try:
    {[1, 2]: "x"}
except TypeError as err:
    print("list as key ->", err)
print("tuple key OK:", {(1, 2): "x"}, "| merge:", {"a": 1} | {"a": 2, "b": 3})

print("\n--- set ---")
print("type({}) =", type({}).__name__, "| type(set()) =", type(set()).__name__)
A, B = {1, 2, 3, 4}, {3, 4, 5}
print("A|B", A | B, "A&B", A & B, "A-B", A - B, "A^B", A ^ B, "A<=B", A <= B)
try:
    {[1], [2]}
except TypeError as err:
    print("set of lists ->", err)
print("frozenset usable as key:", {frozenset({1, 2}): "ok"})
print("duplicates removed:", set([1, 1, 2, 3, 3]))

print("\n--- membership speed (100000 items, 200 lookups of the worst case) ---")
lst = list(range(100000)); st = set(lst)
t_l = timeit.timeit(lambda: 99999 in lst, number=200)
t_s = timeit.timeit(lambda: 99999 in st, number=200)
print(f"list {t_l*1000:.2f} ms, set {t_s*1000:.4f} ms -> set is about {t_l/t_s:,.0f}x faster here")
