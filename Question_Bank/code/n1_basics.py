"""Notes M1: conditions and branching, list methods, comprehensions, and how Python passes arguments."""
print("--- truthiness and short-circuit (and / or return an OPERAND, not True/False) ---")
print("falsy values:", [bool(x) for x in (0, 0.0, "", [], {}, set(), None)], "| truthy:", [bool(x) for x in (1, -1, "0", [0], " ")])
print("0 or 'x' ->", repr(0 or "x"), "| '' and 5 ->", repr("" and 5), "| 3 and 4 ->", repr(3 and 4), "| None or [] ->", repr(None or []))
calls = []
def noisy(v):
    calls.append(v); return v
noisy(False) and noisy(True); noisy(True) or noisy(False)
print("short-circuit: right-hand side skipped, calls made =", calls)
x = 7
print("chained comparison 1 < x < 10:", 1 < x < 10, "| not x == 7:", not x == 7, "| x != 7:", x != 7)
print("ternary:", "even" if x % 2 == 0 else "odd", "| 'in':", 3 in [1, 2, 3], "'z' not in 'abc':", "z" not in "abc")
a = None
print("None test: a is None ->", a is None, "| [] == None ->", [] == None, "| 0.1 + 0.2 == 0.3 ->", 0.1 + 0.2 == 0.3)
import math
print("math.isclose(0.1 + 0.2, 0.3) ->", math.isclose(0.1 + 0.2, 0.3))

print("\n--- if / elif order matters ---")
def grade_wrong(m):
    if m >= 50: return "C"
    elif m >= 70: return "B"          # never reached
    elif m >= 85: return "A"          # never reached
    return "Fail"
def grade(m):
    if m >= 85: return "A"
    elif m >= 70: return "B"
    elif m >= 50: return "C"
    return "Fail"
print("wrong order for 90, 75, 55, 30:", [grade_wrong(m) for m in (90, 75, 55, 30)])
print("right order for 90, 75, 55, 30:", [grade(m) for m in (90, 75, 55, 30)])
def kind(p):
    match p:
        case (0, 0): return "origin"
        case (x, 0): return f"on x-axis at {x}"
        case (0, y): return f"on y-axis at {y}"
        case {"name": n}: return f"dict with name {n}"
        case _: return "elsewhere"
print("match statement (Python 3.10+):", [kind(p) for p in ((0, 0), (3, 0), (0, 4), {"name": "A"}, (1, 1))])

print("\n--- list methods ---")
L = [1, 2, 3]
L.append([4, 5]); print("append adds ONE element:", L)
L = [1, 2, 3]; L.extend([4, 5]); print("extend adds each element:", L, "| L + [6] makes a new list:", L + [6], "| L:", L)
L.insert(1, 99); print("insert(1, 99):", L)
L.remove(99); print("remove(99) deletes the first match:", L)
print("pop() ->", L.pop(), "| pop(0) ->", L.pop(0), "| list now:", L)
try:
    L.remove(1000)
except ValueError as err:
    print("remove of a missing item ->", err)
M = [5, 3, 5, 1]
print("index(5):", M.index(5), "(first match) | count(5):", M.count(5), "| reverse in place:", (M.reverse(), M)[1], "| len:", len(M), "| min/max/sum:", min(M), max(M), sum(M))
del M[0]; print("del M[0]:", M)
print("sorted(key=len):", sorted(["bb", "a", "ccc"], key=len), "| reverse=True:", sorted([3, 1, 2], reverse=True), "| sort is stable:", sorted([(1, "b"), (0, "z"), (1, "a")], key=lambda t: t[0]))
print("enumerate:", list(enumerate("ab", start=1)), "| zip:", list(zip([1, 2, 3], "ab")), "| unzip:", list(zip(*[(1, "a"), (2, "b")])))

print("\n--- comprehensions ---")
print("squares of evens:", [n * n for n in range(10) if n % 2 == 0], "| nested:", [(i, j) for i in range(2) for j in range(2)])
print("if-else goes BEFORE for:", ["even" if n % 2 == 0 else "odd" for n in range(4)], "| filter goes AFTER:", [n for n in range(6) if n > 3])
print("dict comp:", {w: len(w) for w in ["ab", "cde"]}, "| set comp:", {n % 3 for n in range(10)}, "| generator sum:", sum(n for n in range(5)))

print("\n--- how arguments are passed: by object reference ---")
def grow(lst):
    lst.append(1)               # mutates the caller's object
def rebind(lst):
    lst = [99]                  # rebinds the local name only
def bump(n):
    n += 1                      # ints are immutable: creates a new int
data, num = [], 5
grow(data); rebind(data); bump(num)
print("after grow, rebind, bump:", data, num)
s1 = [1]; s2 = s1; s3 = [1]
print("== compares values, is compares identity:", s1 == s3, s1 is s3, s1 is s2, "| id equal for aliases:", id(s1) == id(s2))
print("rule: use == for values; use `is` only for None, True and False")
