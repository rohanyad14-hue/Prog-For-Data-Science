"""OOP in Python, one section per concept (the Scala twin is oops_scala.scala). Run: python oops_py.py
build_oops.py cuts this file at the section(...) lines, so the PDF shows exactly the code that was run."""


def section(n, title):
    print(f"## {n} {title}")


section(1, "Class, object, constructor, self")
class Student:
    college = "VIT"                          # class attribute: one copy shared by all objects

    def __init__(self, name, marks=0):       # constructor: runs on Student(...)
        self.name = name                     # instance attributes: one copy per object
        self.marks = marks

    def grade(self):                         # self is the object the method was called on
        return "pass" if self.marks >= 40 else "fail"

    def __str__(self):                       # what print(obj) shows
        return f"{self.name} ({self.marks})"


a = Student("Asha", 72)
b = Student("Ravi")                          # default argument: the only 'second constructor' Python has
print(a, a.grade(), "|", b, b.grade())
Student.college = "VIT Bhopal"              # change the class attribute once ...
print(a.college, "|", b.college)             # ... and every object sees it

section(2, "Encapsulation and access control")
class Account:
    def __init__(self, owner, balance):
        self.owner = owner                   # public
        self._bank = "VITB"                  # one underscore: 'protected' by convention only
        self.__balance = balance             # two underscores: stored as _Account__balance (name mangling)

    @property
    def balance(self):                       # read-only attribute
        return self.__balance

    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("amount must be positive")
        self.__balance += amount


acc = Account("Asha", 1000)
acc.deposit(500)
print(acc.balance)
try:
    print(acc.__balance)
except AttributeError as e:
    print("AttributeError:", e)
print(acc._Account__balance)                 # still reachable: Python hides the name, it does not forbid access
try:
    acc.balance = 5
except AttributeError as e:
    print("AttributeError:", e)

section(3, "Inheritance and super()")
class Person:
    def __init__(self, name):
        self.name = name

    def describe(self):
        return f"{self.name} is a person"


class Employee(Person):
    def __init__(self, name, salary):
        super().__init__(name)               # run the parent constructor first
        self.salary = salary

    def describe(self):                      # overriding: same name, new body
        return super().describe() + f" earning {self.salary}"


class Manager(Employee):                     # multilevel inheritance
    pass


m = Manager("Meena", 90000)
print(m.describe())
print(isinstance(m, Person), [c.__name__ for c in Manager.__mro__])

section(4, "Method overloading (there is none)")
class Calc:
    def add(self, a, b):
        return a + b

    def add(self, a, b, c):                  # replaces the first add: only the last def with a name survives
        return a + b + c


try:
    Calc().add(1, 2)
except TypeError as e:
    print("TypeError:", e)


class Calc2:
    def add(self, a, b=0, c=0):              # emulation 1: default arguments
        return a + b + c

    def total(self, *nums):                  # emulation 2: any number of arguments
        return sum(nums)


k = Calc2()
print(k.add(1), k.add(1, 2), k.add(1, 2, 3), k.total(1, 2, 3, 4))

section(5, "Polymorphism and operator overloading")
class Shape:
    def area(self):
        raise NotImplementedError


class Circle(Shape):
    def __init__(self, r):
        self.r = r

    def area(self):
        return round(3.14159 * self.r ** 2, 2)


class Rect(Shape):
    def __init__(self, w, h):
        self.w, self.h = w, h

    def area(self):
        return self.w * self.h


class Tile:                                  # not a Shape, but it has area(): duck typing
    def area(self):
        return 1


for s in [Circle(2), Rect(3, 4), Tile()]:    # the method that runs depends on the object, not on the variable
    print(type(s).__name__, s.area())


class Vec:
    def __init__(self, x, y):
        self.x, self.y = x, y

    def __add__(self, other):                # operator overloading: + calls __add__
        return Vec(self.x + other.x, self.y + other.y)

    def __repr__(self):
        return f"Vec({self.x}, {self.y})"


print(Vec(1, 2) + Vec(3, 4))

section(6, "Abstract class")
from abc import ABC, abstractmethod


class Vehicle(ABC):
    def __init__(self, name):
        self.name = name

    @abstractmethod
    def wheels(self):                        # abstract: subclasses must provide it
        ...

    def info(self):                          # concrete method, inherited as it is
        return f"{self.name} has {self.wheels()} wheels"


class Car(Vehicle):
    def wheels(self):
        return 4


class Incomplete(Vehicle):                   # forgot to implement wheels()
    pass


print(Car("Swift").info())
for cls in (Vehicle, Incomplete):
    try:
        cls("x")
    except TypeError as e:
        print("TypeError:", e)

section(7, "Multiple inheritance and mixins")
class Flyer:
    def fly(self):
        return f"{self.name} flies"


class Swimmer:
    def swim(self):
        return f"{self.name} swims"


class Duck(Flyer, Swimmer):                  # several parents: a class can inherit from more than one
    def __init__(self, name):
        self.name = name


d = Duck("Donald")
print(d.fly(), "|", d.swim())
print([c.__name__ for c in Duck.__mro__])    # method resolution order: left to right


class A:
    def hi(self):
        return "A"


class B(A):
    def hi(self):
        return "B>" + super().hi()


class C(A):
    def hi(self):
        return "C>" + super().hi()


class D(B, C):                               # diamond: super() follows the MRO D, B, C, A
    pass


print(D().hi())

section(8, "final (not enforced at run time)")
from typing import final


class Base:
    @final                                   # a hint for type checkers such as mypy; Python itself ignores it
    def pay(self):
        return "base pay"


class Child(Base):
    def pay(self):                           # allowed at run time
        return "changed pay"


print(Child().pay())

section(9, "Singleton and class-level members")
class Config:
    _instance = None

    def __new__(cls):                        # called before __init__: return the one existing object
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.values = {}
        return cls._instance


x, y = Config(), Config()
x.values["mode"] = "exam"
print(x is y, y.values)


class Temp:
    count = 0                                # class attribute

    def __init__(self, c):
        self.c = c
        Temp.count += 1

    @classmethod
    def from_f(cls, f):                      # alternative constructor: gets the class, not an object
        return cls(round((f - 32) * 5 / 9, 1))

    @staticmethod
    def is_valid(c):                         # needs neither object nor class
        return c >= -273.15


t = Temp.from_f(212)
print(t.c, Temp.is_valid(-300), Temp.count)

section(10, "Data classes (the counterpart of case classes)")
from dataclasses import dataclass, replace


@dataclass(frozen=True)                      # generates __init__, __repr__, __eq__; frozen makes it immutable
class Point:
    x: int
    y: int = 0


p = Point(1, 2)
print(p, p == Point(1, 2), replace(p, y=9))
try:
    p.x = 5
except Exception as e:
    print(type(e).__name__)
match p:                                     # structural pattern matching (Python 3.10+)
    case Point(x=1, y=yy):
        print("x is 1, y is", yy)
    case _:
        print("other")

section(11, "Anonymous objects")
from types import SimpleNamespace

o = SimpleNamespace(name="temp", size=3)     # an object without a class of its own
print(o.name, o.size, o)


class Greeter:
    def greet(self, name):
        raise NotImplementedError


g = type("AnonymousGreeter", (Greeter,), {"greet": lambda self, name: f"Hello, {name}"})()   # a class made on the fly
print(g.greet("Asha"), isinstance(g, Greeter))
