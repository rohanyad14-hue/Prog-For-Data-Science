"""Build MACSE502_OOP_Python_vs_Scala.pdf: eleven OOP concepts, each shown in Python and in Scala with real output.
Run with the venv python:  python build_oops.py
The programs code/oops_py.py and code/oops_scala.scala (and the oops_err_* files that are meant to fail) must have been run first
(run_and_capture.py, run_sa_extras.py errors ...). The listings in the PDF are cut out of those very files.
"""
import re
import shutil
import tempfile
from pathlib import Path

from reportlab.platypus import CondPageBreak, PageBreak, Paragraph, Spacer

from dsl import B, CODE, H4, KEY, NOTE, OUT, P, T, TIP, WARN
from render import Doc, Heading, S, render_blocks
from reportlab.lib.units import cm

ROOT = Path(__file__).parent
CODE_DIR, OUT_DIR = ROOT / "code", ROOT / "outputs"
PDF = ROOT / "MACSE502_OOP_Python_vs_Scala.pdf"
FOOTER = "MACSE502 Programming for Data Science  |  OOP in Python and Scala"


# ----------------------------------------------------------------------------- cut the listings out of the real files
def py_code():
    secs, cur = {}, None
    for line in (CODE_DIR / "oops_py.py").read_text(encoding="utf-8").splitlines():
        m = re.match(r'^section\((\d+), "(.*)"\)\s*$', line)
        if m:
            cur = int(m.group(1))
            secs[cur] = []
        elif cur is not None:
            secs[cur].append(line)
    return {k: re.sub(r"\n{3,}", "\n\n", "\n".join(v).strip("\n")) for k, v in secs.items()}   # one blank line is enough in print


def scala_code():
    secs, cur = {}, None
    for line in (CODE_DIR / "oops_scala.scala").read_text(encoding="utf-8").splitlines():
        m = re.match(r"^  def s(\d+)\(\): Unit = \{$", line)
        if m:
            cur = int(m.group(1))
            secs[cur] = []
        elif cur is not None and line == "  }":
            cur = None
        elif cur is not None and "section(" not in line:
            secs[cur].append(line[4:] if line.startswith("    ") else line.strip())
    return {k: "\n".join(v).strip("\n") for k, v in secs.items()}


def split_output(path):
    secs, cur = {}, None
    for line in (OUT_DIR / path).read_text(encoding="utf-8").splitlines():
        m = re.match(r"^## (\d+) ", line)
        if m:
            cur = int(m.group(1))
            secs[cur] = []
        elif cur is not None:
            secs[cur].append(line)
    return {k: "\n".join(v).strip("\n") for k, v in secs.items()}


# ----------------------------------------------------------------------------- the text of each concept
ERR = {  # file -> caption of its compiler output
    "oops_err_private": "oops_err_private.scala (meant to fail): access to a private and a protected member",
    "oops_err_override": "oops_err_override.scala (meant to fail): overriding without the word override",
    "oops_err_abstract_new": "oops_err_abstract_new.scala (meant to fail): creating an object of an abstract class",
    "oops_err_abstract_missing": "oops_err_abstract_missing.scala (meant to fail): a subclass that leaves an abstract member out",
    "oops_err_final_method": "oops_err_final_method.scala (meant to fail): overriding a final method",
    "oops_err_final_class": "oops_err_final_class.scala (meant to fail): extending a final class",
}

CONCEPTS = [
    dict(n=1, title="Class, object, constructor, self and this",
         intro="A <b>class</b> is the blueprint and an <b>object</b> is one thing built from it. The <b>constructor</b> is the code that runs when the object "
               "is created and gives its fields their first values.",
         points=["<b>Python</b> has one constructor, `__init__`, and every method names the object as its first parameter, `self`. The way to get a second "
                 "form is a default argument: `Student(\"Ravi\")` starts with 0 marks.",
                 "<b>Scala</b> writes the primary constructor in the class header: `class Student(val name: String, var marks: Int)`. `val` or `var` in front of a "
                 "parameter turns it into a field. More constructors are written `def this(...)` and must start by calling another constructor.",
                 "`this` is implicit in Scala and is written only when needed. Here `setMarks` returns `this`, so `b.setMarks(30).setMarks(55)` chains.",
                 "A class attribute (`college`) belongs to the class and is shared: after `Student.college = \"VIT Bhopal\"` both objects show the new value. "
                 "Scala has no `static`; shared members go into a companion object (concept 9)."],
         exam="Constructor = the special method that runs at object creation. Python: `__init__`. Scala: the class header and body, plus `def this` for extra ones."),
    dict(n=2, title="Encapsulation and access control",
         intro="<b>Encapsulation</b> keeps the data of an object hidden and lets other code reach it only through methods, so that rules (here: a deposit must be "
               "positive) cannot be bypassed.",
         points=["<b>Python</b> has no access keywords. One underscore (`_bank`) is only a request to other programmers. Two underscores (`__balance`) make Python store "
                 "the field as `_Account__balance`: `acc.__balance` fails, but `acc._Account__balance` still returns 1500 in the output. A `@property` without a "
                 "setter makes an attribute read-only.",
                 "<b>Scala</b> has `private` (this class only), `protected` (this class and its subclasses) and public as the default, with no keyword. The compiler "
                 "enforces them, so a wrong access is rejected before the program runs (compiler output below).",
                 "The guard is `require(amount > 0, ...)` in Scala, which throws IllegalArgumentException; in Python it is an `if` and `raise ValueError`."],
         errors=["oops_err_private"],
         exam="Python: privacy by convention and name mangling. Scala: privacy enforced by the compiler."),
    dict(n=3, title="Inheritance and super",
         intro="<b>Inheritance</b> lets a subclass reuse a parent class, add members of its own, and replace (<b>override</b>) an inherited method.",
         points=["<b>Python</b>: `class Employee(Person)`. The child constructor calls `super().__init__(name)`. `Manager.__mro__` lists the lookup order "
                 "Manager, Employee, Person, object (output).",
                 "<b>Scala</b>: `class Employee(name: String, val salary: Int) extends Person(name)`. The arguments for the parent constructor go in the `extends` clause. "
                 "Replacing a concrete method needs the word `override`; leaving it out is a compile error (below). The printed chain is Manager -> Employee -> Person -> Object.",
                 "`Manager extends Employee extends Person` is <b>multilevel</b> inheritance in both languages. In both, `super` reaches the parent's version of a method."],
         errors=["oops_err_override"],
         exam="A Scala class has exactly one superclass. Extra behaviour comes from traits (concept 7). Python allows several parent classes."),
    dict(n=4, title="Method overloading and overriding, field overriding",
         intro="<b>Overloading</b>: the same method name with different parameters in one class, chosen at compile time. <b>Overriding</b>: a subclass supplies its own "
               "body for an inherited member, chosen at run time.",
         points=["<b>Python has no overloading.</b> The second `def add` replaces the first, so `Calc().add(1, 2)` fails with the TypeError in the output. The usual "
                 "substitutes are default arguments (`b=0, c=0`) and `*nums`.",
                 "<b>Scala has real overloading</b>: the compiler picks the method by the number and types of the arguments (`add(1, 2)`, `add(1, 2, 3)`, `add(1.5, 2.5)` "
                 "give 3, 6 and 4.0).",
                 "Scala can override a field as well: `override val sound = \"woof\"`.",
                 "<b>Trap.</b> The parent constructor runs first. If it uses the overridden val while it is being built (`val size = label.length`), that val is still null "
                 "and the program throws NullPointerException (output). Declaring the parent's member as `lazy val` delays the calculation to its first use, and the answer is "
                 "then 7, the length of \"derived\"."],
         exam="Overloading: same class, different parameter list. Overriding: subclass, same signature. Python has only overriding."),
    dict(n=5, title="Polymorphism and operator overloading",
         intro="<b>Polymorphism</b> means one call with many behaviours: the method that runs depends on the object, not on the variable that holds it.",
         points=["In both languages the loop calls `area` on a Circle, a Rect and a base object, and each answers in its own way.",
                 "<b>Python</b> uses <b>duck typing</b>: `Tile` is not a Shape but has `area()`, so it works. <b>Scala</b> is statically typed: the list is `List[Shape]`, "
                 "so every element must be a Shape.",
                 "<b>Operator overloading</b>: Python defines `__add__` for `+`. In Scala an operator is only a method named `+`. Both print Vec(4, 6).",
                 "Small difference visible in the output: Rect(3, 4) prints 12 in Python (ints stay ints) and 12.0 in Scala (the parameters are Double)."],
         exam="Overriding plus a parent-typed variable gives run-time (dynamic) polymorphism. Overloading is compile-time polymorphism."),
    dict(n=6, title="Abstract class",
         intro="An <b>abstract class</b> declares members without a body that every concrete subclass must supply. It may also contain finished methods, and no object "
               "can be created from it.",
         points=["<b>Python</b>: inherit from `ABC` and mark the method `@abstractmethod`. The mistake is caught only when an object is created, at run time: both "
                 "`Vehicle(\"x\")` and `Incomplete(\"x\")` raise TypeError (output).",
                 "<b>Scala</b>: `abstract class`. A member without a body is abstract automatically. The compiler rejects both mistakes before the program runs. Each mistake "
                 "has its own file below, because the compiler stops after the first stage that finds an error.",
                 "`override` is optional when implementing an abstract member (`def wheels: Int = 4`). An anonymous subclass can complete the class on the spot: "
                 "`new Vehicle(\"Hero\") { def wheels: Int = 2 }`."],
         errors=["oops_err_abstract_new", "oops_err_abstract_missing"],
         exam="Abstract class = a partly finished class. Python reports misuse at run time, Scala at compile time."),
    dict(n=7, title="Multiple inheritance, traits and mixins",
         intro="A class can get behaviour from several sources. <b>Python</b> allows <b>multiple inheritance</b>. <b>Scala</b> allows one superclass plus any number of "
               "<b>traits</b>: interface-like units that may also contain finished methods, added by <b>mixin composition</b>.",
         points=["Scala: `class Duck(val name: String) extends Flyer with Swimmer`. A trait can also be mixed into one object at creation: `new Service with Logger`.",
                 "Python: `class Duck(Flyer, Swimmer)`. `Duck.__mro__` shows the order in which Python looks for a method.",
                 "<b>Same diamond, opposite order.</b> B and C both extend A. Python's `D(B, C)` prints `B>C>A`, while Scala's `D extends B with C` prints `C>B>A`. "
                 "Scala's <b>linearization</b> runs the last mixin first; Python's MRO goes from left to right.",
                 "In Scala 2.13 (used here) a trait cannot take constructor parameters; a class can. A trait can declare an abstract member (`def name: String`) "
                 "that the class mixing it in fills."],
         exam="Trait = interface plus optional concrete methods. `extends` for the first parent, `with` for the others. Linearization: right to left."),
    dict(n=8, title="final",
         intro="<b>final</b> stops change: a final method cannot be overridden and a final class cannot be extended.",
         points=["<b>Scala</b> enforces it. The program in the output uses `final def pay` and `final class Leaf` normally; the two files below show the compiler "
                 "refusing an override and a subclass.",
                 "<b>Python</b> has only `typing.final`, a hint for tools such as mypy. At run time nothing is stopped: `Child().pay()` returns \"changed pay\" in the output."],
         errors=["oops_err_final_method", "oops_err_final_class"],
         exam="final = no overriding (method) and no subclassing (class). Enforced in Scala, advisory in Python."),
    dict(n=9, title="Singleton, companion object and class-level members",
         intro="A <b>singleton</b> is a class with exactly one instance. In Scala a <b>companion object</b> is the object that has the same name as a class and sits in the "
               "same scope; it holds what other languages call static members.",
         points=["<b>Scala</b>: `object Registry` is a singleton by definition (no `new`; `Registry.next()` returns 1, then 2). `object Temp` is the companion of `class Temp`: "
                 "its `apply` lets you write `Temp(21.5)`, and because the class constructor is `private`, the companion is the only way to make a Temp. "
                 "Scala has no `static` keyword.",
                 "<b>Python</b>: a singleton can be built with `__new__` returning the same object (`x is y` is True and both see one dictionary). Class-level members: "
                 "`@classmethod` receives the class (`Temp.from_f(212)` is an alternative constructor, 100.0), `@staticmethod` receives nothing, "
                 "and a class attribute (`Temp.count`) is shared."],
         exam="Scala: `object` = singleton. Companion = same name as the class, same file. `apply` allows `Name(args)` without `new`."),
    dict(n=10, title="Case classes and data classes",
         intro="A <b>case class</b> (Scala) and a <b>dataclass</b> (Python) are classes made to hold data. The language writes the constructor, the text form, equality and a "
               "copy method for you.",
         points=["<b>Scala</b>: `case class Point(x: Int, y: Int = 0)` gives `Point(1, 2)` without `new`, immutable fields, `toString` (prints Point(1,2)), "
                 "`==` and `hashCode` based on the fields, `copy(y = 9)`, and pattern matching.",
                 "<b>Python</b>: `@dataclass(frozen=True)`. Without `frozen=True` the fields can be changed; with it, assigning raises FrozenInstanceError (output). "
                 "`dataclasses.replace` is the counterpart of `copy`, and `match` / `case` (Python 3.10 or newer) takes the object apart. It prints as Point(x=1, y=2)."],
         exam="A case class is a class with `apply`, `toString`, `equals`, `hashCode`, `copy` and `unapply` (pattern matching) generated for you."),
    dict(n=11, title="Anonymous objects and classes",
         intro="An <b>anonymous class</b> is created without giving the class a name, for one-time use.",
         points=["<b>Scala</b>: `new Greeter { def greet(name: String) = ... }` makes an object of a nameless subclass of the trait. `new Runnable { ... }` is the common use. "
                 "The output shows that the class has no name (`getSimpleName` is empty).",
                 "<b>Python</b>: `SimpleNamespace(name=\"temp\", size=3)` is an object with attributes and no class of your own. `type(name, bases, dict)` builds a class on "
                 "the fly (here a subclass of Greeter, so `isinstance` is True). A `lambda` is an anonymous function."],
         exam="Anonymous class: create an object of a trait or abstract class by writing its body in braces right after `new`, with no class name."),
]

SEEN = {  # where the concept appeared in the sample questions of this course (see MACSE502_Sample_Questions_Answers.pdf)
    1: "M3-Q1, M1-Q3", 2: "M3-Q4", 3: "M3-Q1", 4: "M3-Q1, M3-Q2", 5: "M3-Q2", 6: "M3-Q2", 7: "M3-Q5", 8: "M3-Q2", 9: "M3-Q4", 10: "M3-Q4", 11: "syllabus only",
}
OVERVIEW = {
    1: ("`class`, `__init__`, `self`", "class header is the primary constructor, `def this`, `this`"),
    2: ("`_x`, `__x`, `@property` (convention)", "`private`, `protected`, public default (enforced)"),
    3: ("`class B(A)`, `super()`", "`extends`, `override` required, `super`"),
    4: ("no overloading; default args, `*args`", "real overloading; `override val`"),
    5: ("duck typing, `__add__`", "subtyping, method named `+`"),
    6: ("`ABC` + `@abstractmethod` (run-time error)", "`abstract class` (compile-time error)"),
    7: ("multiple inheritance, MRO", "traits, `with`, linearization"),
    8: ("`typing.final` (hint only)", "`final` (enforced)"),
    9: ("`__new__`, `@classmethod`, `@staticmethod`", "`object`, companion object, `apply`"),
    10: ("`@dataclass`", "`case class`"),
    11: ("`SimpleNamespace`, `type(...)`", "`new Trait { ... }`"),
}


def front():
    fl = [Spacer(1, 6), Paragraph("MACSE502 Programming for Data Science", S["subtitle"]),
          Paragraph("Object-Oriented Programming in Python and Scala", S["title"]),
          Paragraph("Eleven OOP concepts of the syllabus (Module 1: Object-Oriented Concepts; Module 3: classes, constructors, overloading, inheritance, "
                    "abstract classes, traits, companion objects and more), each shown in both languages with code that was run and its real output.", S["subtitle"])]
    rows = [[str(c["n"]), c["title"], OVERVIEW[c["n"]][0], OVERVIEW[c["n"]][1], SEEN[c["n"]]] for c in CONCEPTS]
    fl += render_blocks([T(["No.", "Concept", "Python", "Scala", "Seen in sample questions"], rows, [0.05, 0.25, 0.25, 0.28, 0.17])], CODE_DIR, OUT_DIR)
    fl += render_blocks([
        NOTE("The last column lists where the concept appeared among the sample questions of this course (`MACSE502_Sample_Questions_Answers.pdf`). "
             "It shows what has been asked so far; it is not a prediction of the FAT paper."),
        TIP("How to use this file: read the one-line idea, compare the two listings, then learn the boxed \"Remember\" line for each concept. "
            "Python ran on version 3.10 and Scala on 2.13.12 with Java 17. The wording of some Python error messages differs in newer Python versions."),
    ], CODE_DIR, OUT_DIR)
    return fl


def concept(c, tmp, py, sc, py_out, sc_out):
    n = c["n"]
    (tmp / f"py{n}.py").write_text(py[n] + "\n", encoding="utf-8")
    (tmp / f"sc{n}.scala").write_text(sc[n] + "\n", encoding="utf-8")
    (tmp / f"py{n}.out.txt").write_text(py_out[n] + "\n", encoding="utf-8")
    (tmp / f"sc{n}.out.txt").write_text(sc_out[n] + "\n", encoding="utf-8")
    blocks = [P(c["intro"]), B(c["points"]),
              H4("Python"), CODE(f"py{n}.py", f"Python (code/oops_py.py, section {n})"), OUT(f"py{n}.out.txt", "Output"),
              H4("Scala"), CODE(f"sc{n}.scala", f"Scala (code/oops_scala.scala, section {n})"), OUT(f"sc{n}.out.txt", "Output")]
    for e in c.get("errors", []):
        shutil.copy(CODE_DIR / f"{e}.scala", tmp / f"{e}.scala")
        shutil.copy(OUT_DIR / f"{e}.out.txt", tmp / f"{e}.out.txt")
        blocks += [CODE(f"{e}.scala", f"Code: {ERR[e].split(' (')[0]} (a file that is meant to fail)"), OUT(f"{e}.out.txt", "Compiler output: " + ERR[e])]
    blocks.append(KEY(c["exam"]))
    return [CondPageBreak(7 * cm), Heading(f"{n}. {c['title']}", S["h2"], 0, toc=False)] + render_blocks(blocks, tmp, tmp)


def closing():
    blocks = [
        T(["Pillar", "Idea", "Python", "Scala"], [
            ["Encapsulation", "hide the data, expose methods", "`_x`, `__x`, `@property`", "`private`, `protected`, getter methods"],
            ["Abstraction", "say what, hide how", "`ABC`, `@abstractmethod`", "`abstract class`, `trait`"],
            ["Inheritance", "reuse a parent class", "`class B(A)`, `super()`", "`extends`, `override`, `super`"],
            ["Polymorphism", "one call, many behaviours", "overriding, duck typing, `__add__`", "overriding, overloading, operators as methods"]],
          [0.16, 0.26, 0.28, 0.30]),
        WARN("Common mistakes: (1) expecting method overloading in Python, where the last `def` wins; (2) calling `__x` truly private, it is only renamed; "
             "(3) expecting `typing.final` to stop anything at run time; (4) forgetting `override` in Scala; (5) using an overridden `val` inside the parent's "
             "constructor (NullPointerException); (6) looking for `static` in Scala, which uses a companion object instead; (7) mixing up the order of `B with C` "
             "(the last mixin runs first) with Python's left-to-right MRO; (8) writing an auxiliary constructor that does not start with a call to another constructor."),
        NOTE("Everything in this file was run on this computer and the outputs are the captured outputs. The files `oops_err_*.scala` are meant to fail: they were only "
             "compiled, to capture the compiler messages. No marking scheme is known, so no marks are suggested."),
    ]
    return [CondPageBreak(9 * cm), Heading("The four pillars at a glance, and common mistakes", S["h2"], 0, toc=False)] + render_blocks(blocks, CODE_DIR, OUT_DIR)


def build():
    py, sc = py_code(), scala_code()
    py_out, sc_out = split_output("oops_py.out.txt"), split_output("oops_scala.out.txt")
    ns = [c["n"] for c in CONCEPTS]
    for d, name in ((py, "python code"), (sc, "scala code"), (py_out, "python output"), (sc_out, "scala output")):
        missing = [n for n in ns if n not in d]
        assert not missing, f"missing {name} for sections {missing}"
    with tempfile.TemporaryDirectory() as t:
        tmp = Path(t)
        story = front()
        for c in CONCEPTS:
            story += concept(c, tmp, py, sc, py_out, sc_out)
        story += closing()
        doc = Doc(str(PDF), title="MACSE502 Programming for Data Science: OOP in Python and Scala", footer=FOOTER)
        doc.multiBuild(story)
    return doc.page


if __name__ == "__main__":
    print(f"built {PDF.name}: {build()} pages")
