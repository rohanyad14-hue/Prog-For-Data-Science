"""Notes M1: string handling and exception handling behaviours."""
print("--- strings ---")
s = "  Data Science  "
try:
    s[0] = "x"
except TypeError as err:
    print("immutable:", err)
print(repr(s.strip()), repr(s.lstrip()), repr("xxhixx".strip("x")), "<- strip('x') removes a SET of characters, not a prefix")
print("abcabc".strip("ba"), "<- strips any a/b from both ends")
t = "Programming for Data Science"
print(t[::-1][:7], "|", t[-7:], "|", t[3:11], "|", t.find("Data"), t.find("xyz"))
try:
    t.index("xyz")
except ValueError as err:
    print("index raises:", err)
print(t.split(), "|", t.split(" ", 1), "|", t.rsplit(" ", 1), "|", t.partition(" for "))
print("-".join(["a", "b", "c"]), "|", "a,b,,c".split(","), "|", " a  b ".split(), "|", " a  b ".split(" "))
print(t.replace("a", "A", 2), "|", t.count("a"), "|", t.startswith(("Prog", "Data")), "|", "5".zfill(3), "|", "ab".center(6, "*"))
name, gpa = "Rohan", 8.4567
print(f"{name:>8}|{gpa:.2f}|{gpa:8.1f}|{42:05d}|{1234567:,}|{0.256:.1%}")
print("%s scored %.1f" % (name, gpa), "|", "{} scored {:.1f}".format(name, gpa))
print("Python".casefold() == "PYTHON".casefold(), "| 'a' < 'B':", "a" < "B", "| ord/chr:", ord("A"), chr(98))
print("isdigit/isalpha/isalnum:", "123".isdigit(), "12.5".isdigit(), "abc".isalpha(), "ab1".isalnum())
a = "".join(["hel", "lo"]); b = "hello"
print("== vs is:", a == b, a is b, "(use == for values)")
print("sorted words by length:", sorted("a quick brown fox".split(), key=len))

print("\n--- exceptions: order, else, finally ---")
def parse(x):
    try:
        v = int(x)
    except ValueError:
        return "ValueError"
    except (TypeError, KeyError):
        return "TypeError/KeyError"
    else:
        return f"ok {v}"
    finally:
        print("   finally for", repr(x))
print(parse("12"), "|", parse("a"), "|", parse(None))

def f():
    try:
        return "from try"
    finally:
        print("   finally runs before the value is returned")
print(f())
def g():
    try:
        return "from try"
    finally:
        return "from finally"       # overrides - avoid this
print("finally can override return:", g())

print("\n--- hierarchy: specific before general ---")
for risky in (lambda: 1 / 0, lambda: [][1], lambda: {}["k"], lambda: int("x")):
    try:
        risky()
    except ZeroDivisionError as e:
        print("ZeroDivisionError is an ArithmeticError:", isinstance(e, ArithmeticError))
    except LookupError as e:
        print(type(e).__name__, "is a LookupError (IndexError and KeyError share this parent)")
    except Exception as e:
        print("other:", type(e).__name__)

print("\n--- custom exception, chaining, assert, with ---")
class InsufficientFunds(Exception):
    def __init__(self, balance, amount):
        super().__init__(f"balance {balance} < {amount}")
        self.balance, self.amount = balance, amount
def withdraw(bal, amt):
    if amt > bal:
        raise InsufficientFunds(bal, amt)
    return bal - amt
try:
    withdraw(100, 250)
except InsufficientFunds as e:
    print("custom:", e, "| attrs:", e.balance, e.amount)
try:
    try:
        int("x")
    except ValueError as e:
        raise RuntimeError("config invalid") from e
except RuntimeError as e:
    print("chained:", e, "| cause:", repr(e.__cause__))
try:
    assert 1 + 1 == 3, "math broke"
except AssertionError as e:
    print("AssertionError:", e)
with open("tmp_with.txt", "w") as fh:
    fh.write("x")
print("file closed after with:", fh.closed)
print("KeyboardInterrupt is NOT an Exception:", not issubclass(KeyboardInterrupt, Exception))
