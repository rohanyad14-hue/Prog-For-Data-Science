from dsl import *

mcqs = [
    MCQ("What happens with `val x = 5; x = 6` in Scala?",
        ["x becomes 6", "compile-time error: reassignment to val", "runtime exception", "x stays 5 silently"], 1,
        "`val` is an immutable reference. Use `var` if the reference must change."),
    MCQ("Which expression creates a new List with 0 added at the front of `List(1, 2)`?",
        ["`List(1, 2) :+ 0`", "`0 :: List(1, 2)`", "`List(1, 2).add(0)`", "`List(1, 2)(0) = 0`"], 1,
        "`::` (cons) prepends in O(1). `:+` appends and costs O(n) on a List. Lists are immutable, so a new list is returned."),
    MCQ("Which of these is NOT generated automatically for a case class?",
        ["`toString`", "`copy`", "structural `equals`", "a `main` method"], 3,
        "The compiler adds `apply`, `unapply`, `copy`, `equals`, `hashCode` and `toString`. A `main` method you write yourself (or extend `App`)."),
    MCQ("`Student(\"Rohan\", 101)` (no `new`) works for a normal class when:",
        ["the class is final", "its companion object defines `apply`", "the class is abstract", "the class has a private field"], 1,
        "The call is rewritten to `Student.apply(\"Rohan\", 101)`. Case classes get this companion `apply` for free."),
    MCQ("In Scala a class can extend:",
        ["any number of classes", "one class and any number of traits", "only one trait", "one abstract class and no traits"], 1,
        "Single class inheritance plus multiple trait mixins (`class A extends B with T1 with T2`)."),
    MCQ("A method declared `final def` in a superclass:",
        ["cannot be overridden in a subclass", "must be overridden", "is abstract", "is private"], 0,
        "`final` forbids overriding (on a class it forbids extending)."),
    MCQ("What does `List(1, 2, 3, 4).foldLeft(0)((acc, x) => acc + x)` return?",
        ["List(1, 3, 6, 10)", "10", "0", "24"], 1, "Accumulator steps: 0+1=1, 1+2=3, 3+3=6, 6+4=10."),
    MCQ("A `private` member of a class is accessible:",
        ["everywhere", "in the class itself (and its companion object)", "in subclasses only", "in the same package only"], 1,
        "`protected` adds subclasses; default (no modifier) is public in Scala."),
    MCQ("`object Config { val name = \"app\" }` defines:",
        ["a class with no constructor", "a singleton: exactly one instance created lazily on first use", "a trait", "a static import"], 1,
        "An `object` is Scala's singleton, used for utilities and as the home of `main` and companion factories."),
    MCQ("What is `List(1, 2, 3).map(_ * 2).filter(_ > 2)`?",
        ["List(2, 4, 6)", "List(4, 6)", "List(1, 2, 3)", "List(6)"], 1, "map gives List(2, 4, 6); filter keeps values greater than 2."),
    MCQ("To redefine a concrete method inherited from a superclass you must write:",
        ["`overload`", "`override`", "`super`", "`final`"], 1, "`override` is mandatory when replacing a concrete member (optional for abstract ones)."),
]

shorts = [
    SHORT("Explain `val`, `var`, `lazy val` and type inference.", 3, [
        B(["`val` : immutable binding, assigned once. `var` : mutable binding. Prefer `val` (functional style, thread-safe).",
           "`lazy val` : evaluated on first use, once, then cached.",
           "Type inference: `val n = 10` is an `Int`, `val s = \"hi\"` a `String`. Annotate public method return types: `def area: Double`."])]),
    SHORT("Show the different ways to write a function in Scala (expanded format, short format, function literal).", 3, [
        SNIP("def addExpanded(a: Int, b: Int): Int = {   // expanded: braces + explicit result type\n    a + b\n}\n"
             "def add(a: Int, b: Int) = a + b             // short: type inferred, no braces\n"
             "val addLit: (Int, Int) => Int = (a, b) => a + b   // function literal stored in a val\n"
             "def twice(f: Int => Int, x: Int) = f(f(x))  // higher-order: takes a function\n"
             "twice(_ * 3, 2)                              // 18, `_` is the placeholder argument", lang="scala"),
        P("The last expression is the result; `return` is legal but not idiomatic.")]),
    SHORT("Differentiate Array, List, Set, Map and Tuple in Scala.", 5, [
        T(["Type", "Mutable?", "Ordered / unique", "Notes"], [
            ["`Array[T]`", "elements yes, size fixed", "ordered, duplicates ok", "index `a(0)`; maps to a JVM array; O(1) access"],
            ["`List[T]`", "no (immutable)", "ordered, duplicates ok", "linked list; `::` prepend O(1); index access O(n)"],
            ["`Set[T]`", "no by default", "unordered, unique", "membership test fast; `union`, `intersect`, `diff`"],
            ["`Map[K,V]`", "no by default", "unique keys", "`get` returns Option; `getOrElse`; `+` adds a pair"],
            ["`(A, B, C)`", "no", "fixed size, mixed types", "access with `._1`, `._2`; destructure `val (a, b) = t`"]],
          [0.15, 0.2, 0.24, 0.41]),
        P("Mutable versions live in `scala.collection.mutable` (`ArrayBuffer`, `mutable.Set`, `mutable.HashMap`).")]),
    SHORT("Explain `map`, `flatMap`, `filter`, `foldLeft` and `reduce` with one example each.", 5, [
        T(["Combinator", "Idea", "Example -> result"], [
            ["`map`", "transform each element", "`List(1,2,3).map(_ * 2)` -> List(2, 4, 6)"],
            ["`filter`", "keep elements passing a test", "`List(1,2,3,4).filter(_ % 2 == 0)` -> List(2, 4)"],
            ["`flatMap`", "map then flatten one level", "`List(\"hi\",\"yo\").flatMap(_.toList)` -> List(h, i, y, o)"],
            ["`foldLeft`", "accumulate from the left with a start value", "`List(1,2,3,4).foldLeft(0)(_ + _)` -> 10"],
            ["`reduce`", "like fold but starts with the first element (fails on an empty list)", "`List(1,2,3).reduce(_ * _)` -> 6"]],
          [0.15, 0.35, 0.5])]),
    SHORT("What are primary and auxiliary constructors? What does `this` do?", 3, [
        B(["The <b>primary constructor</b> is the class header and body: `class Account(val owner: String, var balance: Double)`.",
           "An <b>auxiliary constructor</b> is `def this(...)`; its first statement must call another constructor: `def this(owner: String) = this(owner, 0.0)`.",
           "`this` refers to the current object (`this.balance = balance` when a parameter hides a field) and is also the name used to call another constructor."])]),
    SHORT("Differentiate method overloading and method overriding.", 3, [
        P("<b>Overloading</b>: same method name, different parameter lists, in the same class; resolved at compile time "
          "(`deposit(x)` and `deposit(x, note)`). <b>Overriding</b>: a subclass replaces an inherited method or field with the same signature using `override`; "
          "resolved at run time through dynamic dispatch. `final` blocks overriding.")]),
    SHORT("Explain Scala access modifiers.", 3, [
        T(["Modifier", "Visible in"], [
            ["(none) public", "everywhere (default)"],
            ["`protected`", "the class and its subclasses (not the rest of the package)"],
            ["`private`", "the class itself and its companion object"],
            ["`private[pkg]`", "qualified: visible up to the named package or class"]], [0.3, 0.7])]),
    SHORT("Differentiate a singleton `object`, a companion object and an anonymous class.", 3, [
        B(["<b>Singleton object</b>: `object Config { ... }` is a single instance, no `new`, used for utilities and `main`.",
           "<b>Companion object</b>: an `object` with the same name as a class in the same file; it can read the class's private members and defines "
           "`apply` factories and static-like helpers.",
           "<b>Anonymous class</b>: a one-off subclass created inline: `new Animal { override val sound = \"meow\" }`."])]),
    SHORT("What is the Scala REPL? List two commands.", 2, [
        P("The REPL (Read-Eval-Print Loop) is an interactive shell started with the `scala` command. You type an expression, it compiles and evaluates it, "
          "prints the value and gives it a name (`res0`). `:paste` enters multi-line mode (end with Ctrl+D); `:quit` exits; `:help` lists commands. "
          "It is ideal for trying array and list operations.")]),
    SHORT("Explain string interpolation: `s`, `f` and `raw`.", 2, [
        SNIP('val name = "Rohan"; val gpa = 8.4567\ns"Hello $name, next year ${2026 + 1}"   // s: embed values and expressions\n'
             'f"GPA = $gpa%.2f"                      // f: printf-style formatting -> 8.46\n'
             'raw"no escape \\n here"                // raw: backslashes are not interpreted', lang="scala")]),
]

# ------------------------------------------------------------------------------------------ longs
c1_prompt = [
    P("(Lab experiments 13 to 16) Create an array of integers 2, 5, 9, 14, 20 and a function returning the sum; create an array of five fruit names and a function that joins them with commas; "
      "iterate over the array. Create a list of the first five primes and square each element; build a set of unique characters of \"hello world\" and "
      "intersect two sets; create a tuple (Int, String, Boolean) and print each element. Create a HashMap of names and grades with a duplicate key, "
      "merge two maps keeping the higher grade, and store several values per key using lists (chaining). "
      "Use `filter`, `map`, `flatMap` and `foldLeft` on the list 1 to 10."),
]
c1_answer = [
    H3("Key ideas"),
    B(["Arrays are mutable and fixed size even when the reference is a `val`; Lists, Sets and Maps are immutable by default, so every \"change\" returns a new collection.",
       "A duplicate key in a Map (or `put` into a mutable HashMap) <b>overwrites</b> the old value. This is a key conflict, resolved by a rule such as `math.max`. "
       "A true hash collision (two different keys in one bucket) is resolved internally by the hash table. Storing a `List` of values per key is the user-level \"chaining\" asked in the lab.",
       "Combinator pipeline: `filter` -> `map` -> `flatMap` (flatten) -> `foldLeft`/`reduce` (aggregate). `foldLeft(1L)(_ * _)` over 1 to 10 gives 3628800 (use `Long`, because 13! already overflows `Int`).",
       "`Set` operations: `intersect`, `union`, `diff`; a set built from a String keeps unique characters."]),
    CODE("m3_q1_collections.scala"),
    OUT("m3_q1_collections.out.txt"),
    NOTE("All Scala programs in this bank were compiled and run with Scala 2.13.12 on Java 17 (via scala-cli), the same Scala version as your Colab (Almond) setup."),
]

c2_prompt = [
    P("(FAT high-frequency question 6) Write a Scala program that demonstrates: classes with primary and auxiliary constructors; method overloading; "
      "the `this` keyword; inheritance with field overriding and `final`; an abstract class; access modifiers; a singleton object; a companion object "
      "with an `apply` factory; and an anonymous class. Explain how a companion object removes the need for `new`."),
]
c2_answer = [
    T(["Syllabus concept", "Where it appears in the code"], [
        ["Primary constructor", "`class Account(val owner: String, private var balance: Double)`"],
        ["Auxiliary constructor, `this`", "`def this(owner: String) = this(owner, 0.0)`"],
        ["Method overloading", "`deposit(amount)` and `deposit(amount, note)`"],
        ["Inheritance, field overriding", "`class Dog extends Animal { override val sound = \"woof\" }`"],
        ["`final`", "`final def kind()` cannot be overridden"],
        ["Abstract class", "`abstract class Shape { def area: Double }` implemented by `Circle`, `Rect`"],
        ["Access modifiers", "`private`, `protected`, public in `Base` / `Child`"],
        ["Singleton object", "`object Config`"],
        ["Companion object, `apply`", "`class Student private (...)` + `object Student { def apply(...) }`"],
        ["Anonymous class", "`new Animal { override val sound = \"meow\" }`"]], [0.32, 0.68]),
    H3("How the companion object works"),
    P("The compiler rewrites `Student(\"Rohan\", 101)` to `Student.apply(\"Rohan\", 101)`. The companion shares the class name and file, "
      "so it can call the private constructor and read private members. It is the idiomatic factory: it can validate, count instances (as the demo does: `created = 2`), "
      "cache objects or return a subtype, none of which `new` allows. Case classes get a generated `apply` automatically."),
    WARN("A `def` cannot override a `val`, but a `val` can override a parameterless `def`. When overriding a concrete member you must write `override`."),
    CODE("m3_q2_oop.scala"),
    OUT("m3_q2_oop.out.txt"),
]

c3_prompt = [
    P("(Lab experiment 17, FAT high-frequency question 5) Create `case class Person(name, age, city)` and a list of five people. "
      "Filter out people older than 30, group by city, convert each person to the string \"Name is Age years old and lives in City\", "
      "and sort by age. List four capabilities that distinguish a case class from a normal class and show pattern matching with a guard."),
]
c3_answer = [
    T(["Capability", "Normal class", "Case class"], [
        ["Constructor parameters", "private unless marked `val`", "public `val` fields automatically"],
        ["Instantiation", "`new` required (unless a companion `apply` exists)", "companion `apply` generated: `Person(\"A\", 22, \"X\")`"],
        ["Equality", "reference equality (`eq`) by default", "structural `equals` and `hashCode` on all fields"],
        ["`toString`", "`Person@1b2c3d`", "`Person(Asha,22,Chennai)`"],
        ["Copy with changes", "write your own", "`p.copy(city = \"Pune\")`"],
        ["Pattern matching", "needs a hand-written `unapply`", "generated `unapply`: `case Person(n, a, _) =>`"]], [0.22, 0.38, 0.4]),
    P("Case classes are meant for immutable data records. Combined with `sealed` traits they give exhaustive pattern matching "
      "(the compiler warns if a case is missing)."),
    CODE("m3_q3_case_traits.scala"),
    OUT("m3_q3_case_traits.out.txt"),
]

c4_prompt = [
    P("(FAT high-frequency question 9) Contrast traits with abstract classes. Explain trait mixins and how Scala resolves the diamond problem "
      "through linearization, using `class D extends B with C` where both `B` and `C` extend `A` and override `who` calling `super.who`."),
]
c4_answer = [
    T(["Point", "Abstract class", "Trait"], [
        ["Inheritance", "a class extends exactly one", "a class mixes in many: `extends Base with T1 with T2`"],
        ["Constructor parameters", "yes", "not in Scala 2 (Scala 3 allows them)"],
        ["State and behaviour", "fields, concrete and abstract methods", "also; commonly small reusable behaviours"],
        ["Java interop", "behaves like an abstract Java class", "compiles to an interface (plus helper code)"],
        ["Use when", "a strong \"is-a\" base type with constructor arguments", "adding orthogonal capabilities (logging, auditing)"]],
      [0.2, 0.38, 0.42]),
    H3("Mixins"),
    P("`class Worker(name) extends Logger with Auditor` inherits the concrete methods of both traits. A trait can also be mixed in for a single object: "
      "`new Worker(\"Kabir\") with Notifier`."),
    H3("Linearization of `D extends B with C`"),
    P("Scala orders the whole parent chain into one line, so `super` always has exactly one meaning. The rule: "
      "<b>L(D) = D, followed by L(C) then L(B), where a type already seen later in the line replaces its earlier occurrence</b>."),
    N(["L(A) = A", "L(B) = B, A", "L(C) = C, A",
       "L(D) = D, L(C) +> L(B) = D, {C, A} +> {B, A} = <b>D, C, B, A</b>",
       "`A` appears once, at the end, so the diamond is resolved. `super.who` in D calls C, which calls B, which calls A."]),
    P("The program printed `D > C > B > A`, confirming the order. The class mixed in <i>last</i> (C) is consulted first."),
    SNIP("trait A { def who: String = \"A\" }\ntrait B extends A { override def who = \"B > \" + super.who }\n"
         "trait C extends A { override def who = \"C > \" + super.who }\nclass D extends B with C { override def who = \"D > \" + super.who }\n"
         "println((new D).who)", lang="scala", caption="Excerpt from m3_q3_case_traits.scala"),
    OUT("m3_q3_case_traits.out.txt", "Output of the whole program (the last lines show the trait mixins and `D > C > B > A`)",
        transform=lambda t: "\n".join(t.split("\n")[-6:])),
]

c5_prompt = [
    P("Demonstrate Scala fundamentals: the expanded function format and shorter forms, variables and strings, reading user input, numbers and "
      "variable types, operators and booleans. Explain what is special about operators and about `==` versus `eq` in Scala."),
]
c5_answer = [
    B(["<b>Types</b>: `Byte` (8-bit), `Short` (16), `Int` (32), `Long` (64), `Float` (32), `Double` (64), `Char` (16), `Boolean`, `String`. "
       "`Int` arithmetic overflows silently: `Int.MaxValue + 1` is `-2147483648`.",
       "<b>Operators are methods</b>: `1 + 2` is `1.+(2)`; `a max b` is `a.max(b)`. Precedence follows the first character of the operator.",
       "`==` calls `equals` (value equality); `eq` compares references. `&&` and `||` short-circuit, so the right side may never run.",
       "<b>Input</b>: `scala.io.StdIn.readLine()` and `readInt()` read from the keyboard. The demo feeds them from a `StringReader` so the program is repeatable."]),
    CODE("m3_q4_basics.scala"),
    OUT("m3_q4_basics.out.txt"),
]

longs = [
    LONG("Scala collections and functional combinators", 10, c1_prompt, c1_answer,
         "arrays 2, list/set/tuple 2, map conflicts and chaining 3, combinators 3."),
    LONG("Classes, constructors, inheritance and companion objects", 10, c2_prompt, c2_answer,
         "constructors and overloading 3, inheritance and abstract 3, access modifiers 1, singleton/companion 3."),
    LONG("Case classes and pattern matching", 10, c3_prompt, c3_answer,
         "four capabilities 4, list operations 3, pattern matching with guard 3."),
    LONG("Traits, mixins and linearization", 10, c4_prompt, c4_answer,
         "trait vs abstract class 3, mixins 2, linearization steps 4, code 1."),
    LONG("Scala fundamentals", 10, c5_prompt, c5_answer,
         "functions 2, variables and strings 2, input 1, numbers and operators 3, booleans and equality 2."),
]

MODULE_3 = MODULE(
    3, "Scala data structures and object-oriented programming", "12 hours",
    "expanded function format; variables and strings; user input; numbers; variable types; operators; booleans; arrays, lists, tuples, sets, hash set, maps; "
    "functional combinators (map); objects and classes; anonymous object, singleton; companion object, case classes; constructors; method overloading; "
    "`this`; inheritance; field overriding; `final`; abstract class; trait and mixins; access modifiers; Scala array and the REPL.",
    [H3("Revision: Scala in ten lines"),
     B(["Statically typed, runs on the JVM, mixes object-oriented and functional styles; everything is an object, every expression has a value.",
        "Prefer `val`, immutable collections and expressions over statements.",
        "Labs 13 to 17 of your list of experiments map to the five long questions below."])],
    mcqs, shorts, longs,
    exam_notes=[TIP("For code questions, write the result of each `println` as a comment next to it. It shows you can predict output without a compiler."),
                WARN("Do not call `List` \"mutable\" because you wrote `var l = List(1)`; the variable changes, the list does not.")],
)
