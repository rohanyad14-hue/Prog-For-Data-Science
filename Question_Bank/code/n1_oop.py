"""Notes M1: object-oriented Python and its traps."""
from abc import ABC, abstractmethod
from dataclasses import dataclass


print("--- class attribute vs instance attribute ---")
class Bad:
    items = []                      # shared by every instance
    def __init__(self, n):
        self.n = n
    def add(self, x):
        self.items.append(x)
class Good:
    def __init__(self, n):
        self.n = n
        self.items = []             # one list per object
    def add(self, x):
        self.items.append(x)
b1, b2 = Bad(1), Bad(2)
b1.add("x")
g1, g2 = Good(1), Good(2)
g1.add("x")
print("Bad  :", b2.items, "<- b2 sees b1's item")
print("Good :", g2.items)

print("\n--- encapsulation, name mangling, property ---")
class Account:
    def __init__(self, owner, balance):
        self.owner = owner            # public
        self._audit = []              # protected by convention
        self.__balance = balance      # name-mangled
    @property
    def balance(self):
        return self.__balance
    @balance.setter
    def balance(self, v):
        if v < 0:
            raise ValueError("negative balance")
        self.__balance = v
acc = Account("Asha", 100)
print("vars:", sorted(vars(acc)))
print("acc._Account__balance =", acc._Account__balance, "| acc.balance =", acc.balance)
try:
    acc.__balance
except AttributeError as err:
    print("acc.__balance ->", err)
try:
    acc.balance = -5
except ValueError as err:
    print("setter validation:", err)

print("\n--- inheritance, super(), polymorphism, abstract class ---")
class Shape(ABC):
    @abstractmethod
    def area(self): ...
    def describe(self):
        return f"{type(self).__name__} area={self.area():.2f}"
class Circle(Shape):
    def __init__(self, r): self.r = r
    def area(self): return 3.14159 * self.r ** 2
class Rect(Shape):
    def __init__(self, w, h): self.w, self.h = w, h
    def area(self): return self.w * self.h
try:
    Shape()
except TypeError as err:
    print("abstract:", err)
for s in (Circle(1), Rect(2, 3)):
    print(s.describe())

class Person:
    def __init__(self, name): self.name = name
class Student(Person):
    def __init__(self, name, reg):
        super().__init__(name)
        self.reg = reg
st = Student("Asha", "VL1")
print("isinstance Student/Person:", isinstance(st, Student), isinstance(st, Person), "| issubclass:", issubclass(Student, Person))

print("\n--- multiple inheritance and MRO (C3 linearization) ---")
class A:
    def who(self): return "A"
class B(A):
    def who(self): return "B>" + super().who()
class C(A):
    def who(self): return "C>" + super().who()
class D(B, C):
    def who(self): return "D>" + super().who()
print("D().who() =", D().who())
print("MRO:", [k.__name__ for k in D.__mro__])

print("\n--- classmethod, staticmethod, dunder methods ---")
class Temp:
    def __init__(self, c): self.c = c
    @classmethod
    def from_f(cls, f): return cls((f - 32) * 5 / 9)
    @staticmethod
    def is_valid(c): return c >= -273.15
    def __repr__(self): return f"Temp({self.c:.1f})"
    def __str__(self): return f"{self.c:.1f} C"
    def __eq__(self, o): return isinstance(o, Temp) and self.c == o.c
    def __hash__(self): return hash(self.c)
    def __lt__(self, o): return self.c < o.c
    def __add__(self, o): return Temp(self.c + o.c)
t = Temp.from_f(212)
print(repr(t), "|", str(t), "|", Temp.is_valid(-300), "|", Temp(1) + Temp(2), "|", Temp(1) == Temp(1.0),
      "| sorted:", sorted([Temp(5), Temp(1)]), "| in set:", len({Temp(1), Temp(1)}))

@dataclass
class Point:
    x: int
    y: int = 0
print("dataclass:", Point(1, 2), Point(1, 2) == Point(1, 2))

print("\n--- duck typing ---")
class Duck:
    def speak(self): return "quack"
class Robot:
    def speak(self): return "beep"
print([o.speak() for o in (Duck(), Robot())], "(no common base class needed)")
