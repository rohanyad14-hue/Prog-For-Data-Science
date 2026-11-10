r"""Task tables (Task | Code) for the PYTHON syllabus topics that the lab-based cheat sheet does not cover.
A row is (task, code), (task, code, flag) or (task, code, flag, verify_code):
  flag "skip"     shown but not executed (the reason is in SKIP_REASON)
  verify_code     what is executed instead of the displayed code (e.g. a local stub server instead of a public website)
Group fields: env = which virtualenv runs it (main, cb = ChatterBot, sc = Scrapy, dl = Keras / PyTorch / TensorFlow / XGBoost),
setup = hidden code run first, stdin = text fed to input().
verify_gap_py.py executes every group in order, one namespace and one empty working directory per group.
"""

GROUPS = []
SKIP_REASON = {}


def c(s):
    return s.strip("\n")


def group(gid, title, topics, env, rows, note="", setup="", stdin=""):
    GROUPS.append(dict(id=gid, title=title, topics=topics, env=env, rows=rows, note=note, setup=setup, stdin=stdin))


# =============================================================================================== MODULE 1
group("1.1", "Condition and branching statements, loops", "Module 1: Condition and Branching Statements", "main", [
    ("Inputs used below", c(r'''
marks = 72
attendance = 81
''')),
    ("if / elif / else", c(r'''
if marks >= 90:
    grade = 'S'
elif marks >= 80:
    grade = 'A'
elif marks >= 70:
    grade = 'B'
else:
    grade = 'C'
print(grade)
''')),
    ("Combine conditions with and / or / not", c(r'''
if marks >= 40 and attendance >= 75:
    result = 'Pass'
elif marks >= 40:
    result = 'Detained (attendance)'
else:
    result = 'Fail'
print(result)
''')),
    ("Conditional expression (one-line if)", "status = 'Eligible' if attendance >= 75 else 'Not eligible'\nprint(status)"),
    ("Chained comparison, membership, identity", "print(70 <= marks < 80, 'B' in ['A', 'B'], marks is None, not marks > 100)"),
    ("Truthiness: what counts as False", "print(bool([]), bool(''), bool(0), bool(None), bool([0]), bool('False'))"),
    ("for loop with range and enumerate", c(r'''
for i in range(1, 6, 2):
    print(i, end=' ')
for position, name in enumerate(['Asha', 'Ravi', 'Meena'], start=1):
    print(position, name)
''')),
    ("while loop with break and continue", c(r'''
n, total = 0, 0
while True:
    n += 1
    if n % 2 == 0:
        continue
    if n > 9:
        break
    total += n
print(total)
''')),
    ("for ... else (else runs when there was no break)", c(r'''
for n in [4, 6, 8]:
    if n % 2:
        print('odd number found')
        break
else:
    print('no odd number')
''')),
    ("Nested loops: multiplication table", "for i in range(1, 4):\n    print([i * j for j in range(1, 6)])"),
    ("List comprehension with a condition", "even_squares = [x * x for x in range(10) if x % 2 == 0]\nprint(even_squares)"),
    ("match / case (Python 3.10+)", c(r'''
command = 'stop'
match command:
    case 'go':
        print('moving')
    case 'stop' | 'halt':
        print('stopping')
    case _:
        print('unknown')
''')),
])

group("1.2", "Built-in data structures: list, tuple, dictionary, set", "Module 1: List, Tuple, Dictionary, Set", "main", [
    ("List: create, index, slice", "nums = [5, 3, 8, 1]\nprint(nums[0], nums[-1], nums[1:3], nums[::-1])"),
    ("List methods", c(r'''
nums.append(9)
nums.insert(1, 7)
nums.extend([2, 2])
nums.remove(2)
last = nums.pop()
nums.sort(reverse=True)
print(nums, len(nums), nums.index(8), nums.count(2))
''')),
    ("sorted(), reversed(), min/max/sum, copy", "ordered = sorted(nums)\nprint(ordered, min(nums), max(nums), sum(nums), list(reversed(nums)))\nbackup = nums.copy()"),
    ("Tuple: packing, unpacking, immutability", c(r'''
point = (3, 4)
x, y = point
first, *rest = (1, 2, 3, 4)
single = (5,)
print(x, y, first, rest, type(single).__name__)
try:
    point[0] = 9
except TypeError as e:
    print('error:', e)
''')),
    ("Dictionary: create, read, add, update, delete", c(r'''
student = {'name': 'Asha', 'age': 20}
print(student['name'], student.get('city', 'unknown'))
student['city'] = 'Pune'
student.update({'age': 21})
del student['age']
print(student, list(student.keys()), list(student.values()))
''')),
    ("Iterate over a dictionary", "for key, value in student.items():\n    print(key, '->', value)"),
    ("Count words with a dictionary", c(r'''
words = ['a', 'b', 'a', 'c', 'a']
counts = {}
for w in words:
    counts[w] = counts.get(w, 0) + 1
print(counts)
''')),
    ("Dictionary comprehension", "lengths = {w: len(w) for w in ['data', 'science']}\nprint(lengths)"),
    ("Counter and defaultdict", c(r'''
from collections import Counter, defaultdict
print(Counter(words).most_common(1))
groups = defaultdict(list)
for w in words:
    groups[w].append(w)
print(dict(groups))
''')),
    ("Set: create, add, remove, operations", c(r'''
a = {1, 2, 3, 3}
b = {3, 4}
print(a | b, a & b, a - b, a ^ b, {1, 2} <= a)
a.add(10)
a.discard(99)
''')),
    ("Remove duplicates with a set", "unique = sorted(set([3, 1, 3, 2, 1]))\nprint(unique)"),
    ("Nested structures: list of dictionaries", c(r'''
records = [{'name': 'Asha', 'marks': [80, 90]}, {'name': 'Ravi', 'marks': [70, 60]}]
average = {r['name']: sum(r['marks']) / len(r['marks']) for r in records}
print(average)
''')),
    ("Shallow copy versus deep copy", c(r'''
import copy
a = [1, [2, 3]]
shallow = a.copy()
deep = copy.deepcopy(a)
a[1].append(4)
print(shallow, deep)
''')),
], note="A list is ordered and mutable, a tuple is ordered and immutable, a dict maps keys to values, a set is unordered with unique items. Keys of a dict and items of a set must be hashable (no lists).")

group("1.3", "User-defined data structures: Stack, Queue, Priority Queue", "Module 1: Stack, Queue, Priority Queue", "main", [
    ("Stack class (last in, first out)", c(r'''
class Stack:
    def __init__(self):
        self._items = []

    def push(self, x):
        self._items.append(x)

    def pop(self):
        if self.is_empty():
            raise IndexError('pop from empty stack')
        return self._items.pop()

    def peek(self):
        return self._items[-1]

    def is_empty(self):
        return not self._items

    def __len__(self):
        return len(self._items)
''')),
    ("Use the stack: balanced brackets", c(r'''
def balanced(text):
    pairs = {')': '(', ']': '[', '}': '{'}
    s = Stack()
    for ch in text:
        if ch in '([{':
            s.push(ch)
        elif ch in pairs:
            if s.is_empty() or s.pop() != pairs[ch]:
                return False
    return s.is_empty()

print(balanced('{[()]}'), balanced('(]'))
''')),
    ("Queue class (first in, first out) on a deque", c(r'''
from collections import deque

class Queue:
    def __init__(self):
        self._items = deque()

    def enqueue(self, x):
        self._items.append(x)

    def dequeue(self):
        return self._items.popleft()

    def is_empty(self):
        return not self._items

    def __len__(self):
        return len(self._items)
''')),
    ("Use the queue", "q = Queue()\nfor name in ['Asha', 'Ravi', 'Meena']:\n    q.enqueue(name)\nprint(q.dequeue(), len(q))"),
    ("Priority queue with heapq (smallest first)", c(r'''
import heapq
pq = []
heapq.heappush(pq, (2, 'write report'))
heapq.heappush(pq, (1, 'fix bug'))
heapq.heappush(pq, (3, 'lunch'))
while pq:
    priority, task = heapq.heappop(pq)
    print(priority, task)
''')),
    ("PriorityQueue class (ties keep arrival order)", c(r'''
import itertools

class PriorityQueue:
    def __init__(self):
        self._heap = []
        self._count = itertools.count()

    def push(self, item, priority):
        heapq.heappush(self._heap, (priority, next(self._count), item))

    def pop(self):
        return heapq.heappop(self._heap)[2]

    def __len__(self):
        return len(self._heap)
''')),
    ("Use it", "pq2 = PriorityQueue()\npq2.push('B', 2)\npq2.push('A', 1)\npq2.push('C', 2)\nprint([pq2.pop() for _ in range(3)])"),
    ("Max-heap trick: store negative priorities", "maxheap = []\nfor v in [4, 9, 2]:\n    heapq.heappush(maxheap, -v)\nprint(-heapq.heappop(maxheap))"),
    ("Ready-made versions in the standard library", c(r'''
from queue import Queue as FifoQueue, LifoQueue, PriorityQueue as PQ
fifo, lifo, pq3 = FifoQueue(), LifoQueue(), PQ()
for x in (1, 2, 3):
    fifo.put(x)
    lifo.put(x)
pq3.put((2, 'b'))
pq3.put((1, 'a'))
print(fifo.get(), lifo.get(), pq3.get())
''')),
], note="list.pop(0) is slow (O(n)); a deque gives O(1) at both ends. heapq is a min-heap: push and pop are O(log n).")

group("1.4", "String handling methods", "Module 1: String handling methods", "main", [
    ("Length and trimming", "s = '  Data Science with Python  '\nprint(len(s), repr(s.strip()), repr(s.lstrip()), repr(s.rstrip()))"),
    ("Change case", "t = s.strip()\nprint(t.upper(), t.lower(), t.title(), t.swapcase(), t.capitalize())"),
    ("Search", "print(t.find('Science'), t.find('xyz'), t.index('with'), t.count('a'), t.startswith('Data'), t.endswith('on'))"),
    ("split, join, replace", "words = t.split()\nprint(words)\nprint('-'.join(words))\nprint(t.replace('Python', 'Scala'))"),
    ("Slicing and reversing", "print(t[0:4], t[-6:], t[::-1], t[::2])"),
    ("Character tests", "print('123'.isdigit(), 'abc'.isalpha(), 'ab12'.isalnum(), ' '.isspace(), 'Abc'.istitle())"),
    ("Formatting: f-string, format(), %", c(r'''
name, score = 'Asha', 92.456
print(f'{name} scored {score:.1f}')
print('{} scored {:.2f}'.format(name, score))
print('%s scored %d' % (name, score))
print(f'{score:>10.2f}|{name:<8}|{42:05d}')
''')),
    ("Parse a CSV-like line", "line = 'Asha,20,Pune'\nname, age, city = line.split(',')\nprint(line.partition(','), line.rsplit(',', 1))"),
    ("Strings are immutable", c(r'''
try:
    t[0] = 'd'
except TypeError as e:
    print('error:', e)
print('apple' < 'banana', 'a' * 3, 'Sci' in t)
''')),
    ("Palindrome check", c(r'''
def is_palindrome(text):
    clean = ''.join(ch.lower() for ch in text if ch.isalnum())
    return clean == clean[::-1]

print(is_palindrome('A man, a plan, a canal: Panama'))
''')),
    ("Regular expressions with re", c(r'''
import re
print(re.findall(r'\d+', 'Order 66 shipped on 12 May'))
print(re.sub(r'\s+', ' ', 'too   many    spaces'))
m = re.search(r'(\w+)@(\w+)\.com', 'mail asha@vit.com now')
print(m.group(1), m.group(2))
''')),
    ("Escapes, raw strings, multi-line text", c(r'''
text = 'line1\nline2\tTabbed'
print(text.splitlines())
print(r'C:\new\table')
poem = """first
second"""
print(len(poem.splitlines()))
''')),
])

group("1.5", "Exception handling in Python", "Module 1: Exception Handling", "main", [
    ("try / except", "try:\n    value = int('abc')\nexcept ValueError:\n    value = 0\nprint(value)"),
    ("Several except blocks", c(r'''
def divide(a, b):
    try:
        return a / b
    except ZeroDivisionError:
        return float('inf')
    except TypeError as e:
        return f'bad types: {e}'

print(divide(1, 0), divide('a', 2))
''')),
    ("else and finally", c(r'''
def read_number(text):
    try:
        n = int(text)
    except ValueError:
        print('not a number')
    else:
        print('parsed', n)
        return n
    finally:
        print('done')

read_number('42')
read_number('x')
''')),
    ("raise an exception yourself", c(r'''
def set_age(age):
    if age < 0:
        raise ValueError('age cannot be negative')
    return age

try:
    set_age(-1)
except ValueError as e:
    print('caught:', e)
''')),
    ("Custom exception class", c(r'''
class InsufficientFunds(Exception):
    def __init__(self, balance, amount):
        super().__init__(f'balance {balance} is less than {amount}')
        self.balance, self.amount = balance, amount
''')),
    ("Use the custom exception", c(r'''
def withdraw(balance, amount):
    if amount > balance:
        raise InsufficientFunds(balance, amount)
    return balance - amount

try:
    withdraw(100, 250)
except InsufficientFunds as e:
    print(e, '| short by', e.amount - e.balance)
''')),
    ("Catch several types at once", "try:\n    [1, 2][5]\nexcept (KeyError, IndexError) as e:\n    print(type(e).__name__, e)"),
    ("Exception chaining with raise ... from", c(r'''
try:
    try:
        {}['x']
    except KeyError as e:
        raise RuntimeError('config value missing') from e
except RuntimeError as err:
    print(err, '| caused by', repr(err.__cause__))
''')),
    ("assert", "try:\n    assert 1 + 1 == 3, 'arithmetic is broken'\nexcept AssertionError as e:\n    print('assertion failed:', e)"),
    ("Exception hierarchy", "print([k.__name__ for k in ZeroDivisionError.__mro__])"),
    ("File errors and the with statement", c(r'''
try:
    with open('missing.txt') as f:
        data = f.read()
except FileNotFoundError as e:
    print('no such file:', e.filename)
''')),
    ("Traceback text for logging", "import traceback\ntry:\n    1 / 0\nexcept ZeroDivisionError:\n    print(traceback.format_exc().splitlines()[-1])"),
], note="Order the except blocks from the most specific to the most general. A bare `except:` also hides KeyboardInterrupt, so catch Exception at most.")

group("1.6", "Object-oriented concepts in Python", "Module 1: Object-Oriented Concepts", "main", [
    ("Class with class and instance attributes", c(r'''
class Student:
    college = 'VIT'                      # class attribute: shared by all objects

    def __init__(self, name, marks):
        self.name = name                 # instance attributes
        self.marks = marks

    def average(self):
        return sum(self.marks) / len(self.marks)

    def __str__(self):
        return f'{self.name} ({self.average():.1f})'
''')),
    ("Create and use objects", "s1 = Student('Asha', [80, 90])\nprint(s1, s1.college, s1.average())"),
    ("Inheritance, super() and overriding", c(r'''
class PGStudent(Student):
    def __init__(self, name, marks, thesis):
        super().__init__(name, marks)
        self.thesis = thesis

    def __str__(self):
        return super().__str__() + ' | thesis: ' + self.thesis

print(PGStudent('Ravi', [70, 75], 'NLP'))
''')),
    ("Abstract class and polymorphism", c(r'''
from abc import ABC, abstractmethod
import math

class Shape(ABC):
    @abstractmethod
    def area(self):
        ...

class Circle(Shape):
    def __init__(self, r):
        self.r = r

    def area(self):
        return math.pi * self.r ** 2

class Rect(Shape):
    def __init__(self, w, h):
        self.w, self.h = w, h

    def area(self):
        return self.w * self.h

for shape in [Circle(1), Rect(2, 3)]:
    print(type(shape).__name__, round(shape.area(), 2))
''')),
    ("The abstract class cannot be instantiated", "try:\n    Shape()\nexcept TypeError as e:\n    print('error:', e)"),
    ("Encapsulation: private attribute and property", c(r'''
class Account:
    def __init__(self, balance):
        self.__balance = balance            # name-mangled to _Account__balance

    @property
    def balance(self):
        return self.__balance

    @balance.setter
    def balance(self, value):
        if value < 0:
            raise ValueError('negative balance')
        self.__balance = value

acc = Account(100)
acc.balance = 150
print(acc.balance)
''')),
    ("classmethod and staticmethod", c(r'''
class Temp:
    count = 0

    def __init__(self, celsius):
        self.celsius = celsius
        Temp.count += 1

    @classmethod
    def from_fahrenheit(cls, f):
        return cls((f - 32) * 5 / 9)

    @staticmethod
    def is_valid(c):
        return c >= -273.15

t = Temp.from_fahrenheit(212)
print(t.celsius, Temp.is_valid(-300), Temp.count)
''')),
    ("Special (dunder) methods", c(r'''
class Vector:
    def __init__(self, x, y):
        self.x, self.y = x, y

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)

    def __eq__(self, other):
        return (self.x, self.y) == (other.x, other.y)

    def __repr__(self):
        return f'Vector({self.x}, {self.y})'

print(Vector(1, 2) + Vector(3, 4), Vector(1, 2) == Vector(1, 2))
''')),
    ("Multiple inheritance and the method resolution order", c(r'''
class A:
    def who(self): return 'A'
class B(A):
    def who(self): return 'B'
class C(A):
    def who(self): return 'C'
class D(B, C):
    pass

print(D().who(), [k.__name__ for k in D.__mro__])
''')),
    ("isinstance, issubclass, hasattr, getattr", "print(isinstance(s1, Student), issubclass(PGStudent, Student), hasattr(s1, 'name'), getattr(s1, 'city', 'n/a'))"),
    ("dataclass: less boilerplate", c(r'''
from dataclasses import dataclass

@dataclass
class Point:
    x: float
    y: float = 0.0

print(Point(1.5), Point(1, 2) == Point(1, 2))
''')),
], note="Python has no real private members: a leading underscore is a convention, a double underscore only mangles the name.")

group("1.7", "File handling: read and write", "Module 1: File Handling - Read/Write", "main", [
    ("Write a text file", c(r'''
with open('notes.txt', 'w', encoding='utf-8') as f:
    f.write('line one\n')
    f.write('line two\n')
    f.writelines(['line three\n', 'line four\n'])
''')),
    ("Read the whole file", "with open('notes.txt', 'r', encoding='utf-8') as f:\n    content = f.read()\nprint(len(content), content.count('\\n'))"),
    ("Read line by line", "with open('notes.txt') as f:\n    for number, line in enumerate(f, start=1):\n        print(number, line.rstrip())"),
    ("Append to the file", "with open('notes.txt', 'a') as f:\n    f.write('line five\\n')"),
    ("readline, readlines, seek", "with open('notes.txt') as f:\n    first = f.readline()\n    f.seek(0)\n    all_lines = f.readlines()\nprint(first.strip(), len(all_lines))"),
    ("Paths and existence checks", c(r'''
import os
from pathlib import Path
print(os.path.exists('notes.txt'), Path('notes.txt').suffix, Path('notes.txt').stat().st_size > 0)
print(Path('notes.txt').read_text().count('line'))
''')),
    ("CSV: write and read with the csv module", c(r'''
import csv
with open('marks.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['name', 'marks'])
    writer.writerows([['Asha', 90], ['Ravi', 75]])
with open('marks.csv', newline='') as f:
    for row in csv.DictReader(f):
        print(row['name'], int(row['marks']) + 5)
''')),
    ("JSON: dump and load", c(r'''
import json
data = {'name': 'Asha', 'courses': ['DS', 'ML'], 'active': True}
with open('student.json', 'w') as f:
    json.dump(data, f, indent=2)
with open('student.json') as f:
    loaded = json.load(f)
print(loaded == data, json.dumps(data))
''')),
    ("pandas: read_csv / to_csv / to_json", c(r'''
import pandas as pd
df = pd.read_csv('marks.csv')
df['grade'] = ['A', 'B']
df.to_csv('marks_out.csv', index=False)
df.to_json('marks.json', orient='records')
print(pd.read_json('marks.json').shape)
''')),
    ("Binary files and pickle", c(r'''
import pickle
with open('data.bin', 'wb') as f:
    f.write(bytes([72, 105]))
with open('data.bin', 'rb') as f:
    print(f.read())
with open('obj.pkl', 'wb') as f:
    pickle.dump({'a': [1, 2]}, f)
with open('obj.pkl', 'rb') as f:
    print(pickle.load(f))
''')),
    ("List and delete files", "print(sorted(name for name in os.listdir('.') if name.endswith('.csv')))\nos.remove('data.bin')"),
    ("Word frequency of a text file", c(r'''
from collections import Counter
with open('notes.txt') as f:
    freq = Counter(f.read().split())
print(freq.most_common(2))
''')),
], note="Modes: 'r' read (default), 'w' write (erases the file), 'a' append, 'x' create only, add 'b' for binary. Always use `with` so the file is closed even after an error.")

REST_SETUP = c(r'''
from gap_stub import start_stub
STUB = start_stub(8765)
''')
group("1.8", "APIs and data collection: simple API and REST APIs (HTTP requests)", "Module 1: APIs and Data Collection, Simple API and REST APIs - HTTP Requests", "main", [
    ("Load packages", "import requests\nimport pandas as pd"),
    ("Base URL of a public test API", "BASE = 'https://jsonplaceholder.typicode.com'", "", "BASE = 'http://127.0.0.1:8765'"),
    ("GET request: status code, headers", "r = requests.get(BASE + '/posts/1', timeout=10)\nprint(r.status_code, r.ok, r.headers['Content-Type'])"),
    ("Parse the JSON body", "post = r.json()\nprint(post['id'], post['title'])"),
    ("Query parameters", "r = requests.get(BASE + '/posts', params={'userId': 1}, timeout=10)\nprint(r.url)\nposts = r.json()\nprint(type(posts).__name__, len(posts) > 0)"),
    ("Send headers (content type, token)", "headers = {'Accept': 'application/json', 'Authorization': 'Bearer <token>'}\nr = requests.get(BASE + '/posts/1', headers=headers, timeout=10)\nprint(r.status_code)"),
    ("POST: create a resource with a JSON body", "new_post = {'title': 'hello', 'body': 'first post', 'userId': 1}\nr = requests.post(BASE + '/posts', json=new_post, timeout=10)\nprint(r.status_code, r.json()['id'])"),
    ("PUT and DELETE", "r = requests.put(BASE + '/posts/1', json={'id': 1, 'title': 'edited', 'body': 'x', 'userId': 1}, timeout=10)\nprint(r.status_code)\nprint(requests.delete(BASE + '/posts/1', timeout=10).status_code)"),
    ("Error status codes and raise_for_status()", c(r'''
r = requests.get(BASE + '/posts/99999', timeout=10)
print(r.status_code)
try:
    r.raise_for_status()
except requests.exceptions.HTTPError as e:
    print('HTTP error:', e)
''')),
    ("Network errors", c(r'''
try:
    requests.get('http://127.0.0.1:9', timeout=2)
except requests.exceptions.RequestException as e:
    print('request failed:', type(e).__name__)
''')),
    ("Reuse a connection with a Session", "s = requests.Session()\ns.headers.update({'Accept': 'application/json'})\nprint(s.get(BASE + '/posts/1', timeout=10).status_code)"),
    ("JSON to DataFrame to CSV", c(r'''
df = pd.DataFrame(requests.get(BASE + '/posts', timeout=10).json())
print(df.columns.tolist())
df.to_csv('posts.csv', index=False)
''')),
    ("The same GET with only the standard library", c(r'''
import json
import urllib.request
with urllib.request.urlopen(BASE + '/posts/1') as resp:
    print(resp.status, json.load(resp)['userId'])
''')),
], note="GET reads, POST creates, PUT replaces, PATCH changes part, DELETE removes. 2xx = success, 3xx = redirect, 4xx = client error (404 not found, 401 unauthorised), 5xx = server error. Always pass timeout=. "
        "Verified against a local stub server that copies the routes of jsonplaceholder.typicode.com (the live site was not contacted).", setup=REST_SETUP)

group("1.9", "NLTK: text processing", "Module 1: Frameworks and Libraries - NLTK", "main", [
    ("Download the resources (once)", "import nltk\nfor pkg in ['punkt', 'punkt_tab', 'stopwords', 'wordnet', 'averaged_perceptron_tagger_eng']:\n    nltk.download(pkg, quiet=True)", "skip"),
    ("Split into sentences and words", c(r'''
from nltk.tokenize import sent_tokenize, word_tokenize
text = "Data science is fun. Python makes it easier, doesn't it?"
sentences = sent_tokenize(text)
tokens = word_tokenize(text)
print(sentences)
print(tokens)
''')),
    ("Lower-case, keep words, remove stopwords", c(r'''
from nltk.corpus import stopwords
stop = set(stopwords.words('english'))
words = [t.lower() for t in tokens if t.isalpha() and t.lower() not in stop]
print(words)
''')),
    ("Stemming (cuts suffixes)", "from nltk.stem import PorterStemmer\nps = PorterStemmer()\nprint([ps.stem(w) for w in ['running', 'flies', 'studies', 'easier']])"),
    ("Lemmatization (dictionary form, needs the part of speech)", "from nltk.stem import WordNetLemmatizer\nwl = WordNetLemmatizer()\nprint(wl.lemmatize('studies'), wl.lemmatize('running', pos='v'), wl.lemmatize('better', pos='a'))"),
    ("Part-of-speech tagging", "from nltk import pos_tag\nprint(pos_tag(word_tokenize('The quick fox jumps')))"),
    ("Word frequencies", "from nltk import FreqDist\nfd = FreqDist(word_tokenize('data data science data python science'))\nprint(fd.most_common(2), fd['data'])"),
    ("n-grams", "from nltk import bigrams, ngrams\nprint(list(bigrams(['a', 'b', 'c'])), list(ngrams(['a', 'b', 'c', 'd'], 3)))"),
    ("Tokenize with a regular expression", "from nltk.tokenize import RegexpTokenizer\nprint(RegexpTokenizer(r'\\w+').tokenize('hello, world! 2026'))"),
    ("WordNet: meanings", "from nltk.corpus import wordnet\nsyn = wordnet.synsets('good')[0]\nprint(syn.name(), '|', syn.definition())"),
    ("Bag of words with scikit-learn", c(r'''
from sklearn.feature_extraction.text import CountVectorizer
cv = CountVectorizer()
X = cv.fit_transform(['data science is fun', 'science needs data'])
print(cv.get_feature_names_out().tolist())
print(X.toarray())
''')),
], note="Typical pipeline: tokenize, lower-case, remove stopwords and punctuation, stem or lemmatize, then count (bag of words / TF-IDF).")
SKIP_REASON["Download the resources (once)"] = "not run: needs internet (the data was already installed)"

CB_ROWS = [
    ("Load packages", "import logging\nfrom chatterbot import ChatBot\nfrom chatterbot.trainers import ListTrainer\nlogging.disable(logging.CRITICAL)"),
    ("Create the bot (SQLite storage, fallback answer)", c(r'''
bot = ChatBot('CampusBot',
              storage_adapter='chatterbot.storage.SQLStorageAdapter',
              database_uri='sqlite:///campus.sqlite3',
              logic_adapters=[{'import_path': 'chatterbot.logic.BestMatch',
                               'default_response': 'Sorry, I do not know that.',
                               'maximum_similarity_threshold': 0.90}],
              read_only=True)
''')),
    ("Train it with question / answer pairs", c(r'''
trainer = ListTrainer(bot)
trainer.train(['Hi', 'Hello! How can I help?',
               'What are the mess timings?', 'Breakfast 7:30-9:00, lunch 12:30-2:00.',
               'Who is the warden?', 'The warden office is in Block A.'])
''')),
    ("Ask a question (a close match is enough)", "print(bot.get_response('Hi'))\nreply = bot.get_response('what are the mess timing')\nprint(reply.text)"),
    ("An unknown question gets the default answer", "print(bot.get_response('tell me a joke'))"),
    ("Chat loop (type bye to stop)", c(r'''
while True:
    user = input('You: ')
    if user.lower() in ('bye', 'quit'):
        break
    print('Bot:', bot.get_response(user))
''')),
    ("Clear the stored knowledge", "bot.storage.drop()"),
]
group("1.10", "ChatterBot: a rule-free retrieval chatbot", "Module 1: Frameworks and Libraries - ChatterBot", "cb", CB_ROWS,
      note="ChatterBot does not generate sentences: it returns the stored answer whose question is closest to yours. read_only=True stops it from learning from every conversation.",
      stdin="Hi\nwho is the warden\nbye\n")


# =============================================================================================== MODULE 2
group("2.1", "pandas Series", "Module 2: Pandas - Series, Handling Missing Values, Built-in Functions", "main", [
    ("Load packages", "import pandas as pd\nimport numpy as np"),
    ("Create a Series with an index", "marks = pd.Series([82, 91, 67, 74], index=['Asha', 'Ravi', 'Meena', 'John'], name='marks')\nprint(marks)"),
    ("From a dictionary, a scalar, an array", "s_dict = pd.Series({'a': 1, 'b': 2, 'c': 3})\nzeros = pd.Series(0, index=range(3))\nfrom_np = pd.Series(np.arange(3) * 1.5)"),
    ("Attributes", "print(marks.index.tolist(), marks.values, marks.dtype, marks.name, marks.shape, marks.size)"),
    ("Access by label and by position", "print(marks['Ravi'], marks.iloc[0], marks[['Asha', 'John']].tolist(), marks['Ravi':'John'].tolist(), marks.iloc[0:2].tolist())"),
    ("Vectorised arithmetic aligns on the index", "bonus = pd.Series({'Asha': 5, 'Ravi': 3, 'Zed': 9})\nprint((marks + bonus).to_dict())\nprint(marks.add(bonus, fill_value=0).to_dict())"),
    ("Filter with a Boolean mask", "print(marks[marks > 70].index.tolist(), marks[(marks > 70) & (marks < 90)].tolist())"),
    ("Statistics", "print(marks.sum(), marks.mean(), marks.median(), round(marks.std(), 2), marks.max(), marks.idxmax(), marks.idxmin(), marks.quantile(0.5))"),
    ("Sort and rank", "print(marks.sort_values(ascending=False).index.tolist())\nprint(marks.sort_index().index.tolist(), marks.rank(ascending=False).tolist())"),
    ("apply and map", "grade = marks.apply(lambda m: 'A' if m >= 80 else 'B')\nprint(grade.to_dict(), marks.map(lambda m: m - 50).tolist())"),
    ("Missing values", "s = pd.Series([1.0, np.nan, 3.0, np.nan])\nprint(s.isna().sum(), s.fillna(s.mean()).tolist(), s.dropna().tolist(), s.ffill().tolist())"),
    ("Cumulative and rolling calculations", "s2 = pd.Series([1, 2, 3, 4, 5])\nprint(s2.cumsum().tolist(), s2.diff().tolist(), s2.pct_change().round(2).tolist(), s2.rolling(2).mean().tolist())"),
    ("Counting and membership", "colors = pd.Series(['r', 'g', 'r', 'b', 'r'])\nprint(colors.value_counts().to_dict(), colors.unique().tolist(), colors.nunique(), colors.isin(['r', 'b']).sum(), marks.between(70, 85).sum())"),
    ("describe() and conversion to a DataFrame", "print(marks.describe().round(2).to_dict())\nframe = marks.to_frame()\nprint(frame.shape)"),
])

group("2.2", "DataFrame: built-in functions, data operations, filtering, extraction", "Module 2: Built-in Functions, Data Operations, Filtering Data in DataFrame, Data Extraction", "main", [
    ("Load packages", "import pandas as pd\nimport numpy as np"),
    ("Create the DataFrame", c(r'''
emp = pd.DataFrame({
    'name': ['Asha', 'Ravi', 'Meena', 'John', 'Sara', 'Kabir', 'Dev', 'Zoya'],
    'dept': ['IT', 'HR', 'IT', 'Sales', 'HR', 'IT', 'Sales', 'IT'],
    'age': [28, 35, 41, 30, 26, 38, 45, 33],
    'salary': [52000, 61000, 75000, 48000, 43000, 68000, 72000, 59000],
    'city': ['Pune', 'Delhi', 'Pune', 'Mumbai', 'Delhi', 'Pune', 'Mumbai', 'Delhi']})
''')),
    ("Inspect: shape, types, summary", "print(emp.shape, emp.columns.tolist())\nemp.info()\nprint(emp.describe().round(1))"),
    ("Extract columns and rows: [], loc, iloc, at", c(r'''
print(emp['name'].tolist()[:2])
print(emp.loc[2, 'name'], emp.iloc[2, 0], emp.at[2, 'salary'])
print(emp.loc[1:3, ['name', 'age']])
print(emp.iloc[:3, [0, 3]])
''')),
    ("Filter with several conditions", "it_high = emp[(emp['dept'] == 'IT') & (emp['salary'] > 55000)]\nprint(it_high['name'].tolist())"),
    ("isin, between, negation", "print(emp[emp['city'].isin(['Pune', 'Goa'])].shape[0], emp[emp['age'].between(30, 40)]['name'].tolist(), emp[~emp['dept'].isin(['IT'])].shape[0])"),
    ("query() with a variable", "print(emp.query(\"dept == 'HR' and age > 30\")['name'].tolist())\nmin_salary = 60000\nprint(emp.query('salary > @min_salary').shape[0])"),
    ("Top / bottom rows and multi-column sort", "print(emp.nlargest(3, 'salary')['name'].tolist(), emp.nsmallest(2, 'age')['name'].tolist())\nprint(emp.sort_values(['dept', 'salary'], ascending=[True, False])['name'].tolist())"),
    ("Add columns: arithmetic, np.where, map, assign", c(r'''
emp['bonus'] = emp['salary'] * 0.1
emp['band'] = np.where(emp['salary'] >= 60000, 'high', 'normal')
emp['initial'] = emp['name'].map(lambda n: n[0])
emp = emp.assign(annual=lambda d: d['salary'] * 12)
print(emp[['name', 'bonus', 'band', 'initial']].head(3))
''')),
    ("Row-wise apply", "emp['label'] = emp.apply(lambda row: f\"{row['name']} ({row['dept']})\", axis=1)\nprint(emp['label'].iloc[0])"),
    ("Drop and rename", "slim = emp.drop(columns=['bonus', 'label', 'initial', 'annual']).rename(columns={'salary': 'pay'})\nprint(slim.columns.tolist())"),
    ("groupby with named aggregations", "summary = emp.groupby('dept').agg(people=('name', 'count'), avg_salary=('salary', 'mean'), oldest=('age', 'max'))\nprint(summary)"),
    ("groupby transform and filter", c(r'''
emp['dept_avg'] = emp.groupby('dept')['salary'].transform('mean')
emp['above_avg'] = emp['salary'] > emp['dept_avg']
big = emp.groupby('dept').filter(lambda g: len(g) >= 3)
print(emp['above_avg'].sum(), big['dept'].unique().tolist())
''')),
    ("Counts, unique values, duplicates", "print(emp['city'].value_counts(normalize=True).round(2).to_dict(), emp['city'].nunique(), emp.duplicated().sum())"),
    ("Rank and quantile bins", "emp['rank'] = emp['salary'].rank(ascending=False).astype(int)\nemp['tier'] = pd.qcut(emp['salary'], 3, labels=['low', 'mid', 'top'])\nprint(emp[['name', 'rank', 'tier']].sort_values('rank').head(3))"),
    ("Use a column as the index", "by_name = emp.set_index('name')\nprint(by_name.loc['Ravi', 'salary'])\nback = by_name.reset_index()"),
    ("Replace values, category type", "emp['dept'] = emp['dept'].replace({'IT': 'Tech'}).astype('category')\nprint(emp['dept'].cat.categories.tolist())"),
    ("Iterate over rows", "for row in emp.head(2).itertuples():\n    print(row.name, row.salary)"),
    ("Sampling and quick tests", "print(emp.sample(3, random_state=1).shape, emp.tail(1)['name'].tolist())\nprint((emp['salary'] > 40000).all(), (emp['age'] > 44).any(), (emp['age'] > 30).sum())"),
], note="Use loc for labels and iloc for positions. Combine conditions with & | ~ and put each condition in brackets.")

group("2.3", "Working with text data in pandas", "Module 2: Working with Text Data", "main", [
    ("Load packages and a text column", "import pandas as pd\nnames = pd.Series([' Asha Rao ', 'ravi KUMAR', 'Meena  Iyer', None, 'John Smith'])"),
    ("Case, whitespace, length", "clean = names.str.strip().str.title()\nprint(clean.tolist())\nprint(names.str.len().tolist(), names.str.lower().iloc[1], names.str.upper().iloc[0])"),
    ("Search: contains, startswith, endswith", "print(clean.str.contains('Rao').tolist())\nprint(clean.str.startswith('J', na=False).tolist(), clean.str.endswith('r').fillna(False).tolist())"),
    ("Replace (with a regular expression)", "print(names.str.replace(r'\\s+', ' ', regex=True).str.strip().tolist())"),
    ("Split into columns", "parts = clean.str.split(expand=True)\nparts.columns = ['first', 'last']\nprint(parts)"),
    ("Extract with capture groups", c(r'''
emails = pd.Series(['asha@vit.ac.in', 'ravi@gmail.com', 'bad.address'])
print(emails.str.extract(r'(\w+)@([\w.]+)'))
''')),
    ("Count, find, slice, get", "print(emails.str.count('a').tolist(), emails.str.find('@').tolist(), emails.str[:4].tolist(), emails.str.split('@').str[0].tolist())"),
    ("Join Series, pad numbers", "first = pd.Series(['A', 'B'])\nlast = pd.Series(['X', 'Y'])\nprint(first.str.cat(last, sep=' ').tolist())\nids = pd.Series(['7', '42', '105'])\nprint(ids.str.zfill(4).tolist(), ids.str.pad(5, side='left', fillchar='*').tolist())"),
    ("Text columns inside a DataFrame", c(r'''
reviews = pd.DataFrame({'review': ['Great product!', 'Bad quality', 'GREAT value', 'ok']})
reviews['positive'] = reviews['review'].str.lower().str.contains('great')
reviews['n_words'] = reviews['review'].str.split().str.len()
reviews['clean'] = reviews['review'].str.lower().str.replace(r'[^a-z ]', '', regex=True)
print(reviews)
''')),
    ("Dummy variables from delimited text", "tags = pd.Series(['a|b', 'b|c', 'a'])\nprint(tags.str.get_dummies())"),
    ("Missing text: na handling", "print(names.isna().sum(), names.fillna('unknown').str.title().tolist())"),
])

group("2.4", "Merging DataFrames: merge, join, concat, pivot", "Module 2: Merging DataFrames", "main", [
    ("Two related tables", c(r'''
import pandas as pd
students = pd.DataFrame({'id': [1, 2, 3, 4], 'name': ['Asha', 'Ravi', 'Meena', 'John']})
marks = pd.DataFrame({'id': [2, 3, 5], 'score': [88, 92, 70]})
''')),
    ("Inner join (matching keys only)", "inner = pd.merge(students, marks, on='id', how='inner')\nprint(inner)"),
    ("Left, right and outer joins", c(r'''
left = students.merge(marks, on='id', how='left')
right = students.merge(marks, on='id', how='right')
outer = students.merge(marks, on='id', how='outer', indicator=True)
print(len(inner), len(left), len(right), len(outer))
print(outer['_merge'].value_counts().to_dict())
''')),
    ("Key columns with different names", "marks2 = marks.rename(columns={'id': 'student_id'})\nm2 = pd.merge(students, marks2, left_on='id', right_on='student_id')\nprint(m2.columns.tolist())"),
    ("Overlapping column names: suffixes", "a = pd.DataFrame({'id': [1, 2], 'v': [10, 20]})\nb = pd.DataFrame({'id': [1, 2], 'v': [1, 2]})\nprint(a.merge(b, on='id', suffixes=('_old', '_new')).columns.tolist())"),
    ("Merge on several keys", c(r'''
x = pd.DataFrame({'dept': ['IT', 'IT', 'HR'], 'year': [2025, 2026, 2026], 'budget': [5, 6, 3]})
y = pd.DataFrame({'dept': ['IT', 'HR'], 'year': [2026, 2026], 'spend': [4, 2]})
print(x.merge(y, on=['dept', 'year'], how='left'))
''')),
    ("join() works on the index", "s_idx = students.set_index('id')\nm_idx = marks.set_index('id')\nprint(s_idx.join(m_idx, how='left'))"),
    ("concat: stack rows or put columns side by side", c(r'''
more = pd.DataFrame({'id': [9], 'name': ['Zed']})
all_students = pd.concat([students, more], ignore_index=True)
side = pd.concat([students, marks], axis=1)
print(all_students.shape, side.shape)
''')),
    ("concat with keys (hierarchical index)", "stacked = pd.concat([students, more], keys=['2025', '2026'])\nprint(stacked.loc['2026'])"),
    ("Anti-join: rows with no match", "only_students = students.merge(marks, on='id', how='left', indicator=True).query(\"_merge == 'left_only'\")\nprint(only_students['name'].tolist())"),
    ("Check the relationship with validate=", c(r'''
try:
    pd.merge(students, pd.concat([marks, marks]), on='id', validate='one_to_one')
except pd.errors.MergeError as e:
    print('MergeError:', e)
''')),
    ("Reshape: pivot_table and melt", c(r'''
sales = pd.DataFrame({'region': ['N', 'N', 'S', 'S'], 'q': ['Q1', 'Q2', 'Q1', 'Q2'], 'amt': [10, 20, 30, 40]})
wide = sales.pivot_table(index='region', columns='q', values='amt', aggfunc='sum')
long = wide.reset_index().melt(id_vars='region', var_name='q', value_name='amt')
print(wide)
print(long.shape)
''')),
], note="merge = SQL join on columns, join = merge on the index, concat = stack along an axis. how='inner' keeps matches only, 'left' keeps every left row (NaN where no match).")

group("2.5", "SciPy: statistics, optimisation, integration, interpolation, linear algebra", "Module 2: SciPy", "main", [
    ("Load packages", "import numpy as np\nfrom scipy import stats, optimize, integrate, interpolate, linalg"),
    ("Descriptive statistics", "data = np.array([12, 15, 14, 10, 18, 20, 11, 16])\nprint(stats.describe(data))\nprint(stats.zscore(data).round(2), round(stats.skew(data), 3))"),
    ("Normal distribution: cdf, ppf, pdf", "print(round(stats.norm.cdf(1.96), 4), round(stats.norm.ppf(0.975), 4), round(stats.norm.pdf(0), 4))"),
    ("Two-sample t-test", c(r'''
a = np.array([5.1, 4.9, 5.6, 5.8, 6.0, 5.5])
b = np.array([6.2, 6.4, 5.9, 6.8, 7.0, 6.5])
t, p = stats.ttest_ind(a, b)
print(round(t, 3), round(p, 4), 'significant' if p < 0.05 else 'not significant')
''')),
    ("One-sample and paired t-tests", "print(round(stats.ttest_1samp(a, 5.0).pvalue, 4))\nprint(round(stats.ttest_rel(a, b).pvalue, 5))"),
    ("Correlation: Pearson and Spearman", c(r'''
x = np.arange(1, 9)
y = np.array([2.1, 3.9, 6.2, 7.8, 10.1, 12.2, 13.8, 16.1])
r, p = stats.pearsonr(x, y)
rho, _ = stats.spearmanr(x, y)
print(round(r, 4), round(rho, 4))
''')),
    ("Simple linear regression", "res = stats.linregress(x, y)\nprint(round(res.slope, 3), round(res.intercept, 3), round(res.rvalue ** 2, 4))"),
    ("Chi-square test of independence", "table = np.array([[30, 10], [20, 40]])\nchi2, p, dof, expected = stats.chi2_contingency(table)\nprint(round(chi2, 2), round(p, 5), dof)"),
    ("Minimise a function", "res = optimize.minimize(lambda v: (v[0] - 3) ** 2 + (v[1] + 1) ** 2, x0=[0, 0])\nprint(res.x.round(3), res.success)"),
    ("Find a root", "root = optimize.root_scalar(lambda x: x ** 3 - 2 * x - 5, bracket=[2, 3])\nprint(round(root.root, 4))"),
    ("Fit a curve", c(r'''
def model(x, a, b):
    return a * np.exp(b * x)

xs = np.linspace(0, 2, 20)
ys = 2.0 * np.exp(0.8 * xs)
popt, _ = optimize.curve_fit(model, xs, ys)
print(popt.round(3))
''')),
    ("Numerical integration", "area, err = integrate.quad(lambda x: x ** 2, 0, 3)\nprint(round(area, 4))"),
    ("Interpolation", "f_lin = interpolate.interp1d([0, 1, 2], [0, 10, 40])\nf_quad = interpolate.interp1d([0, 1, 2], [0, 10, 40], kind='quadratic')\nprint(f_lin(1.5), f_quad(1.5))"),
    ("Linear algebra: solve, det, inverse, eigenvalues", c(r'''
A = np.array([[3, 1], [1, 2]])
rhs = np.array([9, 8])
print(linalg.solve(A, rhs), round(linalg.det(A), 2), linalg.inv(A).round(2).tolist())
vals, vecs = linalg.eig(A)
print(np.sort(vals.real).round(3))
''')),
])

SC_SETUP = c(r'''
from pathlib import Path
Path('page1.html').write_text("""<html><body>
<div class="quote"><span class="text">\u201cStay hungry, stay foolish.\u201d</span><small class="author">Steve Jobs</small>
<div class="tags"><a class="tag" href="/tag/inspirational/">inspirational</a><a class="tag" href="/tag/wisdom/">wisdom</a></div></div>
<div class="quote"><span class="text">\u201cKnowledge is power.\u201d</span><small class="author">Francis Bacon</small>
<div class="tags"><a class="tag" href="/tag/knowledge/">knowledge</a></div></div>
<ul class="pager"><li class="next"><a href="page2.html">Next</a></li></ul></body></html>""", encoding='utf-8')
Path('page2.html').write_text("""<html><body>
<div class="quote"><span class="text">\u201cImagination is more important than knowledge.\u201d</span><small class="author">Albert Einstein</small>
<div class="tags"><a class="tag" href="/tag/imagination/">imagination</a></div></div></body></html>""", encoding='utf-8')
''')
SPIDER = c(r'''
class QuotesSpider(scrapy.Spider):
    name = 'quotes'
    start_urls = ['https://quotes.toscrape.com/']
    custom_settings = {
        'LOG_LEVEL': 'ERROR',
        'ROBOTSTXT_OBEY': True,
        'DOWNLOAD_DELAY': 1,
        'FEEDS': {'quotes.json': {'format': 'json', 'overwrite': True, 'encoding': 'utf8'}},
        'ITEM_PIPELINES': {'__main__.CleanPipeline': 300},
    }

    def parse(self, response):
        for q in response.css('div.quote'):
            item = Quote()
            item['text'] = q.css('span.text::text').get()
            item['author'] = q.css('small.author::text').get()
            item['tags'] = q.css('a.tag::text').getall()
            yield item
        next_page = response.css('li.next a::attr(href)').get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)
''')
group("2.6", "Scrapy: a spider with items, a pipeline and pagination", "Module 2: Data Mining - Scrapy", "sc", [
    ("Load packages", "import json\nimport scrapy\nfrom scrapy.crawler import CrawlerProcess"),
    ("Item: the fields to collect", c(r'''
class Quote(scrapy.Item):
    text = scrapy.Field()
    author = scrapy.Field()
    tags = scrapy.Field()
''')),
    ("Item pipeline: clean every item", c(r'''
class CleanPipeline:
    def process_item(self, item, spider):
        item['text'] = item['text'].strip('\u201c\u201d')
        return item
''')),
    ("Spider: start URL, CSS selectors, next page, settings", SPIDER, "", SPIDER.replace("start_urls = ['https://quotes.toscrape.com/']", "start_urls = [Path('page1.html').resolve().as_uri()]")),
    ("Selectors on their own: CSS and XPath", c(r'''
from scrapy import Selector
sel = Selector(text='<div class="quote"><span class="text">Hi</span><a href="/x">link</a></div>')
print(sel.css('span.text::text').get(), sel.xpath('//span[@class="text"]/text()').get(), sel.css('a::attr(href)').get())
''')),
    ("Run the crawl", "process = CrawlerProcess()\nprocess.crawl(QuotesSpider)\nprocess.start()"),
    ("Read the scraped file", "with open('quotes.json', encoding='utf-8') as f:\n    items = json.load(f)\nprint(len(items), [i['author'] for i in items])"),
    ("Terminal commands for a full project", "# scrapy startproject quotes_project\n# scrapy genspider quotes quotes.toscrape.com\n# scrapy crawl quotes -o quotes.csv\n# scrapy shell 'https://quotes.toscrape.com'", "skip"),
], note="Scrapy is a framework (scheduler, downloader, pipelines) for crawling many pages, Beautiful Soup only parses one HTML string. "
        "The page is fetched with response.follow, so relative links work. Verified on two local pages that have the same HTML structure as quotes.toscrape.com (the live site was not contacted).",
      setup=SC_SETUP)
SKIP_REASON["Terminal commands for a full project"] = "not run: shell commands"

group("2.7", "scikit-learn: the supervised learning workflow", "Module 2: Scikit-Learn", "main", [
    ("Load packages", c(r'''
import numpy as np
from sklearn.datasets import load_iris, load_diabetes
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.tree import DecisionTreeClassifier, export_text
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report, r2_score, mean_squared_error
''')),
    ("Features, labels and a train / test split", "X, y = load_iris(return_X_y=True)\nX_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42, stratify=y)\nprint(X_train.shape, X_test.shape)"),
    ("Scale: learn the mean and std on the training set only", "scaler = StandardScaler().fit(X_train)\nXs_train, Xs_test = scaler.transform(X_train), scaler.transform(X_test)"),
    ("Logistic regression: fit, predict, accuracy", "clf = LogisticRegression(max_iter=200).fit(Xs_train, y_train)\npred = clf.predict(Xs_test)\nprint(round(accuracy_score(y_test, pred), 3))"),
    ("Confusion matrix and classification report", "print(confusion_matrix(y_test, pred))\nprint(classification_report(y_test, pred, target_names=load_iris().target_names))"),
    ("Decision tree and its rules", "tree = DecisionTreeClassifier(max_depth=2, random_state=0).fit(X_train, y_train)\nprint(export_text(tree, feature_names=load_iris().feature_names))\nprint(round(tree.score(X_test, y_test), 3))"),
    ("Random forest and feature importance", "rf = RandomForestClassifier(n_estimators=100, random_state=0).fit(X_train, y_train)\nprint(round(rf.score(X_test, y_test), 3), rf.feature_importances_.round(2))"),
    ("k-nearest neighbours: effect of k", "for k in (1, 5, 15):\n    knn = KNeighborsClassifier(n_neighbors=k).fit(Xs_train, y_train)\n    print(k, round(knn.score(Xs_test, y_test), 3))"),
    ("Linear regression: R-squared and RMSE", c(r'''
Xd, yd = load_diabetes(return_X_y=True)
Xd_tr, Xd_te, yd_tr, yd_te = train_test_split(Xd, yd, test_size=0.2, random_state=0)
lin = LinearRegression().fit(Xd_tr, yd_tr)
pred_d = lin.predict(Xd_te)
print(round(r2_score(yd_te, pred_d), 3), round(mean_squared_error(yd_te, pred_d) ** 0.5, 1))
print(lin.coef_.shape, round(lin.intercept_, 1))
''')),
    ("Cross-validation", "scores = cross_val_score(LogisticRegression(max_iter=200), Xs_train, y_train, cv=5)\nprint(scores.round(3), round(scores.mean(), 3))"),
    ("Pipeline: scaler and model in one object", "pipe = Pipeline([('scale', StandardScaler()), ('model', LogisticRegression(max_iter=200))])\npipe.fit(X_train, y_train)\nprint(round(pipe.score(X_test, y_test), 3))"),
    ("Grid search over a hyper-parameter", c(r'''
knn_pipe = Pipeline([('scale', StandardScaler()), ('model', KNeighborsClassifier())])
grid = GridSearchCV(knn_pipe, {'model__n_neighbors': [1, 3, 5, 9]}, cv=5)
grid.fit(X_train, y_train)
print(grid.best_params_, round(grid.best_score_, 3))
''')),
    ("Class probabilities", "print(pipe.predict_proba([[6.0, 3.0, 4.8, 1.8]]).round(3))"),
    ("Save and load the trained model", "import joblib\njoblib.dump(pipe, 'iris_model.joblib')\nmodel = joblib.load('iris_model.joblib')\nprint(model.predict([[5.1, 3.5, 1.4, 0.2]]))"),
], note="Fit the scaler on the training data only, otherwise information from the test set leaks into the model. Classification metrics: accuracy, precision, recall, F1. Regression metrics: R-squared, MSE / RMSE.")

group("2.8", "XGBoost: gradient-boosted trees", "Module 2: XGBoost", "dl", [
    ("Load packages and split the data", c(r'''
import numpy as np
import xgboost as xgb
from sklearn.datasets import load_breast_cancer, load_diabetes
from sklearn.model_selection import train_test_split
data = load_breast_cancer()
X_train, X_test, y_train, y_test = train_test_split(data.data, data.target, test_size=0.3, random_state=0, stratify=data.target)
''')),
    ("Classifier: fit and score", "clf = xgb.XGBClassifier(n_estimators=100, max_depth=3, learning_rate=0.1, random_state=0)\nclf.fit(X_train, y_train)\nprint(round(clf.score(X_test, y_test), 3))"),
    ("Probabilities and the most important features", "print(clf.predict_proba(X_test[:2]).round(3))\ntop = np.argsort(clf.feature_importances_)[::-1][:3]\nprint([str(data.feature_names[i]) for i in top])"),
    ("Early stopping on a validation set", c(r'''
X_tr, X_val, y_tr, y_val = train_test_split(X_train, y_train, test_size=0.25, random_state=0, stratify=y_train)
early = xgb.XGBClassifier(n_estimators=500, learning_rate=0.1, early_stopping_rounds=10, eval_metric='logloss', random_state=0)
early.fit(X_tr, y_tr, eval_set=[(X_val, y_val)], verbose=False)
print(early.best_iteration < 500)
''')),
    ("Regressor on a regression data set", c(r'''
Xd, yd = load_diabetes(return_X_y=True)
Xd_tr, Xd_te, yd_tr, yd_te = train_test_split(Xd, yd, test_size=0.2, random_state=0)
reg = xgb.XGBRegressor(n_estimators=200, max_depth=3, learning_rate=0.05, random_state=0).fit(Xd_tr, yd_tr)
rmse = float(np.sqrt(np.mean((reg.predict(Xd_te) - yd_te) ** 2)))
print(round(rmse, 1))
''')),
    ("The native API: DMatrix and train()", c(r'''
dtrain = xgb.DMatrix(X_train, label=y_train)
params = {'objective': 'binary:logistic', 'max_depth': 3, 'eta': 0.1}
booster = xgb.train(params, dtrain, num_boost_round=50)
print(booster.predict(xgb.DMatrix(X_test))[:3].round(3))
''')),
    ("Save and load a model", "clf.save_model('model.json')\nclf2 = xgb.XGBClassifier()\nclf2.load_model('model.json')\nprint(clf2.score(X_test, y_test) == clf.score(X_test, y_test))"),
], note="Boosting builds trees one after another and each new tree fits the errors of the previous ones. Lower learning_rate needs more trees. Never use the test set for early stopping.")

group("2.9", "Keras: a neural network with the Sequential API", "Module 2: Keras", "dl", [
    ("Load packages, fix the random seed", c(r'''
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import numpy as np
import keras
from keras import layers
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
keras.utils.set_random_seed(0)
''')),
    ("Prepare the data", c(r'''
X, y = load_iris(return_X_y=True)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0, stratify=y)
scaler = StandardScaler().fit(X_train)
X_train, X_test = scaler.transform(X_train), scaler.transform(X_test)
''')),
    ("Define the layers", "model = keras.Sequential([\n    layers.Input(shape=(4,)),\n    layers.Dense(16, activation='relu'),\n    layers.Dense(8, activation='relu'),\n    layers.Dense(3, activation='softmax'),\n])"),
    ("Show the architecture and parameter count", "model.summary()\nprint(model.count_params())"),
    ("Compile: optimiser, loss, metric", "model.compile(optimizer=keras.optimizers.Adam(0.01), loss='sparse_categorical_crossentropy', metrics=['accuracy'])"),
    ("Train", "history = model.fit(X_train, y_train, epochs=40, batch_size=16, validation_split=0.2, verbose=0)\nprint(round(history.history['loss'][0], 3), '->', round(history.history['loss'][-1], 3))"),
    ("Evaluate on the test set", "loss, acc = model.evaluate(X_test, y_test, verbose=0)\nprint(round(acc, 3))"),
    ("Predict", "probs = model.predict(X_test[:3], verbose=0)\nprint(probs.shape, probs.argmax(axis=1), y_test[:3])"),
    ("Stop early when validation loss stops improving", "stop = keras.callbacks.EarlyStopping(monitor='val_loss', patience=5, restore_best_weights=True)\nh2 = model.fit(X_train, y_train, epochs=100, validation_split=0.2, callbacks=[stop], verbose=0)\nprint(len(h2.history['loss']) <= 100)"),
    ("The functional API", "inp = layers.Input(shape=(4,))\nhidden = layers.Dense(8, activation='relu')(inp)\nout = layers.Dense(3, activation='softmax')(hidden)\nfunc = keras.Model(inp, out)\nprint(func.count_params())"),
    ("Save and reload the model", "model.save('iris.keras')\nreloaded = keras.models.load_model('iris.keras')\nprint(np.allclose(model.predict(X_test[:2], verbose=0), reloaded.predict(X_test[:2], verbose=0)))"),
], note="Parameters of a Dense layer = inputs x units + units (4 x 16 + 16 = 80). softmax for several classes, sigmoid for two, linear output for regression. "
        "sparse_categorical_crossentropy takes integer labels, categorical_crossentropy takes one-hot vectors.")

group("2.10", "TensorFlow: tensors, gradients, tf.function, tf.data", "Module 2: TensorFlow", "dl", [
    ("Load packages", "import os\nos.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'\nimport numpy as np\nimport tensorflow as tf"),
    ("Tensors and operations", "a = tf.constant([[1.0, 2.0], [3.0, 4.0]])\nb = tf.ones((2, 2))\nprint(a.shape, a.dtype.name, (a + b).numpy().tolist(), tf.matmul(a, a).numpy().tolist())"),
    ("Variables and reductions", "w = tf.Variable([1.0, 2.0])\nw.assign_add([0.5, 0.5])\nprint(w.numpy(), tf.reduce_sum(w).numpy(), tf.reduce_mean(a, axis=0).numpy())"),
    ("Automatic differentiation with GradientTape", "x = tf.constant(3.0)\nwith tf.GradientTape() as tape:\n    tape.watch(x)\n    y = x ** 2\nprint(tape.gradient(y, x).numpy())"),
    ("Gradient descent by hand: fit y = 2x + 1", c(r'''
w, b = tf.Variable(0.0), tf.Variable(0.0)
xs = tf.constant([1.0, 2.0, 3.0, 4.0])
ys = 2.0 * xs + 1.0
opt = tf.keras.optimizers.SGD(learning_rate=0.05)
for _ in range(300):
    with tf.GradientTape() as tape:
        loss = tf.reduce_mean((w * xs + b - ys) ** 2)
    grads = tape.gradient(loss, [w, b])
    opt.apply_gradients(zip(grads, [w, b]))
print(round(float(w.numpy()), 1), round(float(b.numpy()), 1))
''')),
    ("tf.function: compile a Python function into a graph", "@tf.function\ndef square_sum(v):\n    return tf.reduce_sum(v * v)\n\nprint(square_sum(tf.constant([1.0, 2.0, 3.0])).numpy())"),
    ("tf.data: build an input pipeline", "ds = tf.data.Dataset.from_tensor_slices((np.arange(6, dtype='float32'), np.arange(6) % 2)).shuffle(6, seed=0).batch(3)\nfor xb, yb in ds:\n    print(xb.shape, yb.shape)"),
    ("A tf.keras model trained from the pipeline", c(r'''
xs_np = np.linspace(-1, 1, 64).astype('float32')
ds = tf.data.Dataset.from_tensor_slices((xs_np, 3 * xs_np + 2)).batch(16)
net = tf.keras.Sequential([tf.keras.layers.Input(shape=(1,)), tf.keras.layers.Dense(1)])
net.compile(optimizer=tf.keras.optimizers.Adam(0.1), loss='mse')
hist = net.fit(ds.map(lambda a, b: (tf.expand_dims(a, -1), b)), epochs=30, verbose=0)
print(hist.history['loss'][-1] < hist.history['loss'][0])
''')),
])

group("2.11", "PyTorch: tensors, autograd, nn.Module, training loop", "Module 2: PyTorch", "dl", [
    ("Load packages", "import torch\nfrom torch import nn\nfrom torch.utils.data import TensorDataset, DataLoader\nfrom sklearn.datasets import load_iris\nfrom sklearn.preprocessing import StandardScaler"),
    ("Tensors", "t = torch.tensor([[1.0, 2.0], [3.0, 4.0]])\nprint(t.shape, t.dtype, (t @ t).tolist(), t.mean().item(), t.view(4).tolist(), torch.zeros(2, 3).shape)"),
    ("NumPy interoperability", "arr = t.numpy()\nback = torch.from_numpy(arr)\nprint(type(arr).__name__, back.dtype)"),
    ("Autograd: gradient of y = x^2 + 2x at x = 3", "x = torch.tensor(3.0, requires_grad=True)\ny = x ** 2 + 2 * x\ny.backward()\nprint(x.grad.item())"),
    ("Data as tensors and a DataLoader", c(r'''
Xn, yn = load_iris(return_X_y=True)
X = torch.tensor(StandardScaler().fit_transform(Xn), dtype=torch.float32)
y = torch.tensor(yn, dtype=torch.long)
loader = DataLoader(TensorDataset(X, y), batch_size=16, shuffle=True)
print(len(loader))
''')),
    ("The model as an nn.Module", c(r'''
class Net(nn.Module):
    def __init__(self):
        super().__init__()
        self.layers = nn.Sequential(nn.Linear(4, 16), nn.ReLU(), nn.Linear(16, 3))

    def forward(self, x):
        return self.layers(x)

torch.manual_seed(0)
net = Net()
''')),
    ("Loss function and optimiser", "loss_fn = nn.CrossEntropyLoss()\noptimizer = torch.optim.Adam(net.parameters(), lr=0.01)"),
    ("Training loop: zero_grad, forward, loss, backward, step", c(r'''
for epoch in range(30):
    for xb, yb in loader:
        optimizer.zero_grad()
        loss = loss_fn(net(xb), yb)
        loss.backward()
        optimizer.step()
print(round(loss.item(), 3))
''')),
    ("Evaluate without tracking gradients", "net.eval()\nwith torch.no_grad():\n    acc = (net(X).argmax(dim=1) == y).float().mean().item()\nprint(acc > 0.9)"),
    ("Save and load the weights", "torch.save(net.state_dict(), 'net.pt')\nnet2 = Net()\nnet2.load_state_dict(torch.load('net.pt'))\nprint(torch.equal(net(X), net2(X)))"),
    ("Count the parameters", "print(sum(p.numel() for p in net.parameters()))"),
], note="PyTorch adds gradients up: call optimizer.zero_grad() every step. CrossEntropyLoss expects raw scores (logits) and int64 class labels.")

group("2.12", "Folium: interactive maps", "Module 2: Data Visualization - Folium", "main", [
    ("Load packages", "import folium\nfrom folium.plugins import MarkerCluster, HeatMap\nfrom pathlib import Path"),
    ("Base map: centre, zoom, tiles", "m = folium.Map(location=[12.9692, 79.1559], zoom_start=7, tiles='OpenStreetMap')"),
    ("Marker with popup, tooltip, icon", "folium.Marker([12.9692, 79.1559], popup='VIT Vellore', tooltip='Click me', icon=folium.Icon(color='blue', icon='info-sign')).add_to(m)"),
    ("Markers from a dictionary of cities", c(r'''
cities = {'Vellore': (12.9165, 79.1325), 'Chennai': (13.0827, 80.2707), 'Bengaluru': (12.9716, 77.5946)}
for name, (lat, lon) in cities.items():
    folium.Marker([lat, lon], popup=name).add_to(m)
''')),
    ("CircleMarker (pixels) and Circle (metres)", "folium.CircleMarker([13.0827, 80.2707], radius=12, color='red', fill=True, fill_opacity=0.6).add_to(m)\nfolium.Circle([12.9165, 79.1325], radius=20000, color='green').add_to(m)"),
    ("A route with PolyLine", "folium.PolyLine(list(cities.values()), color='purple', weight=3, tooltip='route').add_to(m)"),
    ("Layers with FeatureGroup and LayerControl", c(r'''
fg = folium.FeatureGroup(name='Landmarks')
folium.Marker([12.9716, 77.5946], tooltip='Cubbon Park').add_to(fg)
fg.add_to(m)
folium.LayerControl().add_to(m)
''')),
    ("Cluster many markers", "cluster = MarkerCluster().add_to(m)\nfor i in range(10):\n    folium.Marker([12.9 + i * 0.01, 79.1 + i * 0.01]).add_to(cluster)"),
    ("Heat map from [lat, lon, weight]", "HeatMap([[12.97, 79.15, 0.9], [13.08, 80.27, 0.6], [12.97, 77.59, 0.8]]).add_to(m)"),
    ("Draw a region with GeoJson", c(r'''
zone = {'type': 'FeatureCollection', 'features': [
    {'type': 'Feature', 'properties': {'name': 'Zone A'},
     'geometry': {'type': 'Polygon', 'coordinates': [[[79.0, 12.8], [79.3, 12.8], [79.3, 13.1], [79.0, 13.1], [79.0, 12.8]]]}}]}
folium.GeoJson(zone, name='zone', tooltip=folium.GeoJsonTooltip(fields=['name'])).add_to(m)
''')),
    ("Choropleth: colour regions by a value", c(r'''
import pandas as pd
geo = {'type': 'FeatureCollection', 'features': [
    {'type': 'Feature', 'id': 'A', 'properties': {}, 'geometry': {'type': 'Polygon', 'coordinates': [[[78, 12], [79, 12], [79, 13], [78, 13], [78, 12]]]}},
    {'type': 'Feature', 'id': 'B', 'properties': {}, 'geometry': {'type': 'Polygon', 'coordinates': [[[79, 12], [80, 12], [80, 13], [79, 13], [79, 12]]]}}]}
values = pd.DataFrame({'zone': ['A', 'B'], 'population': [120, 340]})
folium.Choropleth(geo_data=geo, data=values, columns=['zone', 'population'], key_on='feature.id', fill_color='YlGn', legend_name='Population').add_to(m)
''')),
    ("Save as an HTML file", "m.save('map.html')\nhtml = Path('map.html').read_text(encoding='utf-8')\nprint(len(html) > 1000, 'leaflet' in html.lower())"),
], note="Folium builds a Leaflet web page: the map tiles are fetched by the browser, so creating and saving the map needs no internet. Coordinates are [latitude, longitude].")

group("2.13", "More Matplotlib and seaborn plots", "Module 2: Data Visualization - Matplotlib, Seaborn", "main", [
    ("Load packages and data", c(r'''
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
rng = np.random.default_rng(0)
days = np.arange(1, 8)
temp = np.array([29, 31, 30, 33, 32, 28, 27])
df = pd.DataFrame({'group': rng.choice(['A', 'B', 'C'], 90), 'x': rng.normal(50, 10, 90)})
df['y'] = df['x'] * 0.8 + rng.normal(0, 5, 90)
''')),
    ("Line plot with markers, labels, grid", "plt.figure(figsize=(6, 3.5))\nplt.plot(days, temp, marker='o', color='tab:red', label='temperature')\nplt.xlabel('Day')\nplt.ylabel('Temperature (C)')\nplt.title('Daily temperature')\nplt.grid(True, alpha=0.3)\nplt.legend()\nplt.savefig('line.png', dpi=100)"),
    ("Several lines and an annotation", "plt.figure()\nplt.plot(days, temp, label='city A')\nplt.plot(days, temp - 3, '--', label='city B')\nplt.annotate('peak', xy=(4, 33), xytext=(5, 33.5), arrowprops=dict(arrowstyle='->'))\nplt.legend()\nplt.savefig('two_lines.png')"),
    ("Bar and horizontal bar with value labels", "fig, ax = plt.subplots()\nbars = ax.bar(['Q1', 'Q2', 'Q3'], [120, 150, 90], color=['#4c72b0', '#55a868', '#c44e52'])\nax.bar_label(bars)\nfig.savefig('bar.png')\nplt.figure()\nplt.barh(['x', 'y'], [3, 5])\nplt.savefig('barh.png')"),
    ("Pie chart", "plt.figure()\nplt.pie([45, 30, 25], labels=['IT', 'HR', 'Sales'], autopct='%1.1f%%', explode=(0.05, 0, 0), startangle=90)\nplt.axis('equal')\nplt.savefig('pie.png')"),
    ("Histogram with a density curve", "plt.figure()\nsns.histplot(df['x'], bins=12, kde=True)\nplt.savefig('hist.png')"),
    ("A grid of subplots", "fig, axes = plt.subplots(2, 2, figsize=(8, 6), sharex=False)\naxes[0, 0].hist(df['x'])\naxes[0, 1].scatter(df['x'], df['y'], s=10)\naxes[1, 0].boxplot([df[df['group'] == g]['y'] for g in 'ABC'])\naxes[1, 1].plot(days, temp)\nfig.suptitle('Dashboard')\nfig.tight_layout()\nfig.savefig('grid.png')"),
    ("Box plot and violin plot by group", "plt.figure()\nsns.boxplot(data=df, x='group', y='y')\nplt.figure()\nsns.violinplot(data=df, x='group', y='y')\nplt.savefig('violin.png')"),
    ("Counts, regression line, pair plot", "plt.figure()\nsns.countplot(data=df, x='group')\nplt.figure()\nsns.regplot(data=df, x='x', y='y')\ng = sns.pairplot(df, hue='group')\ng.savefig('pair.png')"),
    ("Two y axes", "fig, ax1 = plt.subplots()\nax1.plot(days, temp, color='tab:red')\nax2 = ax1.twinx()\nax2.bar(days, [5, 2, 0, 1, 8, 12, 3], alpha=0.3)\nfig.savefig('twin.png')"),
    ("Style, size and cleaning up", "plt.style.use('ggplot')\nplt.rcParams['figure.figsize'] = (6, 4)\nplt.close('all')"),
], note="plt.* draws on the current figure (quick scripts); fig, ax = plt.subplots() gives explicit objects (several panels). Call savefig before show().")

group("5.1", "Language selection: a weighted decision matrix", "Module 5: Programming language selection criteria", "main", [
    ("Load packages", "import pandas as pd\nimport matplotlib.pyplot as plt"),
    ("The criteria of the syllabus with importance weights (1 to 5)", c(r'''
weights = pd.Series({
    'Size of deployment (data, resource, load)': 5, 'Security': 4, 'Skill set': 4, 'Targeted platform': 3,
    'Elasticity of the language': 3, 'Time to production': 4, 'Performance': 5, 'Support and community': 3,
    'Purpose': 5, 'Programmer experience': 3, 'Ease of development and maintenance': 4, 'Efficiency': 4,
    'Availability of an IDE': 2, 'Error checking and diagnosis': 3})
''')),
    ("Score each language per criterion (1 to 5; example opinions)", c(r'''
scores = pd.DataFrame({
    'Python': [3, 3, 5, 4, 4, 5, 3, 5, 5, 5, 4, 3, 5, 3],
    'Scala':  [5, 4, 2, 4, 4, 3, 5, 3, 5, 3, 3, 4, 4, 5],
    'Java':   [5, 5, 4, 5, 4, 3, 5, 5, 4, 3, 4, 4, 5, 4],
    'R':      [2, 2, 3, 3, 3, 4, 2, 4, 3, 4, 3, 2, 4, 3]}, index=weights.index)
''')),
    ("Weighted total of every language", "totals = scores.mul(weights, axis=0).sum().sort_values(ascending=False)\nprint(totals)"),
    ("Percentage of the best possible score and the winner", "percent = (totals / (weights.sum() * 5) * 100).round(1)\nprint(percent.to_dict())\nprint('Best choice:', totals.idxmax())"),
    ("Sensitivity: what if performance matters twice as much?", "w2 = weights.copy()\nw2['Performance'] = 10\nprint(scores.mul(w2, axis=0).sum().sort_values(ascending=False).index.tolist())"),
    ("Show the result as a bar chart", "plt.figure(figsize=(5, 3))\nplt.bar(totals.index, totals.values, color='steelblue')\nplt.ylabel('Weighted score')\nplt.title('Language selection matrix')\nplt.tight_layout()\nplt.savefig('matrix.png')"),
], note="Module 5 has no programming content in the syllabus; this is a way to turn the criteria list into a calculation. The scores are example opinions, change them to fit the scenario in the question.")
