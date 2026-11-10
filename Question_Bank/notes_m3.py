from dsl import *
from notes_util import between, pick

# =====================================================================================================
sub_3_1 = SUB("3.1", "Functions: expanded format, short forms, higher-order functions", [
    B(["Expanded format: `def name(p1: T1, p2: T2): R = { body }`. The <b>last expression is the result</b>; `return` is legal but unidiomatic. Parameter types are mandatory; the result type may be inferred (annotate public methods anyway).",
       "Short form: `def add(a: Int, b: Int) = a + b`. Function literal (anonymous function): `(a: Int, b: Int) => a + b`; placeholder form `_ + _`. A function is a value: `val f: Int => Int = _ * 2`.",
       "Higher-order: takes or returns functions (`map`, `filter`). Default and named arguments, varargs (`xs: Int*`, pass a list with `: _*`), currying (`def add(a: Int)(b: Int)`), partial application (`add(5) _`).",
       "<b>Call-by-value</b> (default): the argument is evaluated once before the call. <b>Call-by-name</b> (`x: => Int`): evaluated at every use inside the function.",
       "A closure captures the <i>variable</i>, not a copy of its value."]),
    OUT("m3_q4_basics.out.txt", "Verified output (first lines: function forms)", transform=lambda t: "\n".join(t.split("\n")[:5])),
    OUT("n3_scala_traps.out.txt", "Verified output", transform=pick("val, var, def", "functions:")),
    QA("What do `v twice`, `d twice` and `l twice` print for `val v = next()`, `def d = next()`, `lazy val l = next()`?", [
        P("`v twice: 1 1 | d twice: 2 3 | l twice: 4 4`. The `val` ran once at definition; the `def` runs on every use (2 then 3); the `lazy val` ran once at its first use (4) and is then cached. "
          "At the end `calls = 4`.")], "tricky"),
    QA("Explain call-by-value and call-by-name using `byValue(next())` and `byName(next())`.", [
        P("With call-by-value `next()` ran once (calls = 1) before the body started and the result 1 + 1 = 2. With call-by-name (`x: => Int`) the expression is re-evaluated at each use of `x`, so it ran twice (1 + 2 = 3, calls = 2). "
          "Use by-name for lazy defaults, logging and custom control structures.")], "tricky"),
    QA("Write `add` in expanded form, short form and as a function value, and show a higher-order function.", [
        SNIP("def addExpanded(a: Int, b: Int): Int = {\n  a + b\n}\ndef add(a: Int, b: Int) = a + b\nval addLit: (Int, Int) => Int = (a, b) => a + b\n"
             "def twice(f: Int => Int, x: Int) = f(f(x))\ntwice(_ * 3, 2)        // 18", lang="scala", caption="Tested in the question bank (M3-C5): all four give 5 or 18")], "3 marks"),
    QA("A closure `val times = (x: Int) => x * factor` is defined with `var factor = 2`, then `factor = 10`. What is `times(3)`?", [
        P("30. The closure captures the variable `factor`, not the value 2 (output: `times(3) = 30`).")], "tricky"),
    QA("What is currying and what is partial application?", [
        P("Currying splits a multi-argument function into a chain of single-argument lists: `def add(a: Int)(b: Int)`. Supplying only the first list gives a new function: `val add5 = add(5) _`, so `add5(10) = 15` (output).")], "3 marks"),
])

sub_3_2 = SUB("3.2", "Variables, strings and user input", [
    B(["`val` = immutable reference (cannot be reassigned); `var` = mutable; `lazy val` = evaluated at first use. Prefer `val`. Types are inferred: `val n = 10` is an `Int`.",
       "Strings are Java strings (immutable). Interpolation: `s\"Hello $name, ${1 + 2}\"`, `f\"$gpa%.2f\"` (printf style, type checked), `raw\"no \\\\n escape\"`. Triple quotes `\"\"\"...\"\"\"` give multi-line text; `.stripMargin` removes the `|` margin.",
       "Useful methods: `length, toUpperCase, reverse, split, mkString, substring, contains, replace, trim, toInt, toDouble, format`.",
       "Input: `scala.io.StdIn.readLine()`, `readInt()`, `readDouble()`; `args` in `main` hold command-line arguments."]),
    OUT("m3_q4_basics.out.txt", "Verified output", transform=lambda t: "\n".join(t.split("\n")[1:9])),
    QA("Difference between `val`, `var` and `lazy val`.", [P("`val` can be assigned once; `var` can be reassigned; `lazy val` is computed only when first used and then cached. For a `val` holding a mutable object, the object can still change, only the reference is fixed.")], "3 marks"),
    QA("What do `s`, `f` and `raw` interpolators do?", [P("`s` substitutes `$name` and `${expr}`; `f` adds printf formats and checks types at compile time (`f\"$gpa%.2f\"` gives 8.46 for 8.4567); `raw` leaves backslash sequences unprocessed.")], "2 marks"),
    QA("How do you read an integer and a line from the keyboard?", [SNIP("val age  = scala.io.StdIn.readInt()\nval lang = scala.io.StdIn.readLine()", lang="scala", caption="The tested program feeds these from a StringReader via Console.withIn")], "2 marks"),
    QA("What is the difference between `\"5\".toInt` and `'5'.toInt`?", [P("`\"5\".toInt` parses the text and gives 5. `'5'.toInt` converts the <i>character</i> to its code, 53. Use `'5'.asDigit` or `'5' - '0'` for the digit (output below). `\"abc\".toIntOption` returns `None` instead of throwing.")], "tricky"),
    OUT("n3_scala_traps.out.txt", "Verified output", transform=pick("Char vs String")),
])

sub_3_3 = SUB("3.3", "Numbers, variable types, operators and booleans", [
    T(["Type", "Size", "Note"], [["Byte, Short, Int, Long", "8, 16, 32, 64 bit", "integer literals are `Int`; `10L` is `Long`; Int overflow wraps silently"], ["Float, Double", "32, 64 bit", "`3.14` is `Double`; `0.1 + 0.2 != 0.3`"],
                                  ["Char, String, Boolean", "16 bit, text, true/false", "`'a'` Char, `\"a\"` String"], ["Unit, Null, Nothing, Any", "-", "`Unit` is `()`; `Any` is the root; `Nothing` is the subtype of everything (e.g. `throw`)"]], [0.28, 0.2, 0.52]),
    B(["Operators are <b>methods</b>: `1 + 2` is `1.+(2)`; `xs map f` is `xs.map(f)`. Precedence is decided by the first character of the operator. Operators ending in `:` are right-associative (`1 :: Nil`).",
       "Integer division truncates: `7 / 2 = 3`, `7 % 3 = 1`, `-7 % 3 = -1`. Bitwise `& | ^ << >>`.",
       "Booleans: `&&` and `||` short-circuit; `&` and `|` always evaluate both sides. `==` is value equality (calls `equals`); `eq` is reference equality.",
       "Conversions are explicit: `3.9.toInt = 3`, `5.toDouble`; assigning a `Double` to an `Int` does not compile."]),
    OUT("m3_q4_basics.out.txt", "Verified output", transform=lambda t: "\n".join(t.split("\n")[9:])),
    OUT("n3_scala_traps.out.txt", "Verified output", transform=pick("equality", "Char vs String")),
    QA("What are `7 / 2`, `7 / 2.0`, `-7 % 3` and `Int.MaxValue + 1`?", [P("3, 3.5, -1 and -2147483648 (the sign of `%` follows the dividend, and Int overflow wraps without an error). Use `Long` for large sums: Spark's `reduce(_ + _)` over 1..1,000,000 as `Int` gave 1784293664 instead of 500000500000.")], "tricky"),
    QA("Difference between `==` and `eq`; predict `new String(\"hi\") == new String(\"hi\")` and `... eq ...`.", [P("`true` and `false`. `==` compares contents; `eq` compares object identity. `Array(1,2) == Array(1,2)` is also `false` (arrays use reference equality); compare with `sameElements` or `.toList`.")], "tricky"),
    QA("What does `false && noisy(true)` do?", [P("Nothing on the right-hand side: `&&` short-circuits, so `noisy` is never called. Likewise `true || ...`. The non-short-circuit operators `&` and `|` evaluate both sides.")], "2 marks"),
    QA("Why is `1 + 2` described as a method call?", [P("Every operator is a method of the left operand: `1.+(2)`. This is why you can define `+` on your own class and why `a max b` and `xs map f` work as infix notation.")], "2 marks"),
])

sub_3_4 = SUB("3.4", "Arrays, lists, tuples, sets, hash sets and maps", [
    T(["Type", "Mutable?", "Order / unique", "Key facts"], [
        ["`Array[T]`", "elements yes, size fixed", "ordered, duplicates ok", "JVM array, `a(i)` O(1); equality is by reference"],
        ["`ArrayBuffer`, `ListBuffer`", "yes", "ordered", "growable (`scala.collection.mutable`)"],
        ["`List[T]`", "no", "ordered, duplicates ok", "linked list; `::` prepend O(1); `a(i)` and `:+` O(n); `Nil` is empty"],
        ["`Vector`", "no", "ordered", "fast random access and updates (effectively O(1))"],
        ["`Set[T]` / `HashSet`", "no (mutable version exists)", "unique, no guaranteed order", "hash based; `&`, `|`, `--` (`intersect`, `union`, `diff`)"],
        ["`Map[K, V]` / `HashMap`", "no (mutable version exists)", "unique keys", "`get` returns `Option`; `m(k)` throws if missing; `+ (k -> v)` returns a new map"],
        ["`(A, B, C)`", "no", "fixed size, mixed types", "`t._1`, destructure `val (a, b) = t`"]], [0.2, 0.2, 0.22, 0.38]),
    B(["Immutable collections never change: every \"modification\" returns a new collection, and `var l = List(1)` only rebinds the variable.",
       "A duplicate key in a Map overwrites the old value; hash collisions (different keys, same bucket) are resolved internally. Lab 15's \"chaining\" is a user-level `Map[K, List[V]]`."]),
    OUT("m3_q1_collections.out.txt", "Verified output (Labs 13 to 16)"),
    OUT("n3_scala_traps.out.txt", "Verified output", transform=pick("lists:", "more collection")),
    QA("Compare Array and List.", [
        T(["", "Array", "List"], [["Mutability", "elements can be changed", "immutable"], ["Size", "fixed", "any, but each change makes a new list"], ["Access", "`a(i)` O(1)", "`l(i)` O(n)"],
                                  ["Prepend", "no", "`x :: l` O(1)"], ["Equality", "reference (`Array(1,2) == Array(1,2)` false)", "structural (true)"]], [0.2, 0.4, 0.4])], "5 marks"),
    QA("What is `1 :: 2 :: Nil`? Why is `::` written on the left of the list?", [P("`List(1, 2)`. Operators ending in a colon are right-associative and are methods of the <i>right</i> operand, so it parses as `1 :: (2 :: Nil)`, i.e. `Nil.::(2).::(1)`.")], "tricky"),
    QA("Create the squares of the first five primes, the unique characters of \"hello world\", and the intersection of two sets.", [
        SNIP("List(2, 3, 5, 7, 11).map(p => p * p)                 // List(4, 9, 25, 49, 121)\n\"hello world\".filter(_ != ' ').toSet            // Set of unique characters\n"
             "(\"hello world\".toSet & \"world\".toSet)                  // common characters", lang="scala", caption="The first and third lines are run in the output above (m3_q1)")], "3 marks"),
    QA("A `Map` holds duplicate-key writes. Show overwrite, merge-with-max and chaining.", [
        P("`grades.put(\"Alice\", 95)` replaces 85. Merge: for each key in `a.keySet ++ b.keySet` take `math.max(a.getOrElse(k, 0), b.getOrElse(k, 0))`. Chaining: `foldLeft(Map.empty[String, List[Int]])` appending to `acc.getOrElse(k, Nil)`. "
          "Output above: merge `(Alice,92), (Bob,90), (Emma,88)`, chained `(Alice, List(85, 95))`.")], "5 marks"),
    QA("`m(\"z\")` versus `m.get(\"z\")` on a Map without \"z\".", [P("`m(\"z\")` throws `NoSuchElementException`; `m.get(\"z\")` returns `None`; `m.getOrElse(\"z\", 0)` returns a default.")], "2 marks"),
    QA("`val l = ListBuffer(1, 2); l += 3; l.prepend(0)`: is that allowed with `val`?", [P("Yes. The reference `l` is fixed but the buffer is mutable (output: `ListBuffer(0, 1, 2, 3)`). The same trick with an immutable `List` would not compile.")], "tricky"),
])

sub_3_5 = SUB("3.5", "Functional combinators", [
    B(["`map` transforms each element; `filter` keeps matches; `flatMap` maps then flattens one level; `foldLeft(z)(f)` / `foldRight(z)(f)` accumulate with a start value; `reduce` folds without a start value (fails on empty); `scanLeft` keeps the intermediate results.",
       "Also: `groupBy`, `partition`, `zip`, `zipWithIndex`, `take/drop/takeWhile`, `sortBy/sortWith`, `distinct`, `sliding`, `exists/forall/count/find`.",
       "`for (x <- xs if cond) yield f(x)` is sugar for `filter`/`map`/`flatMap`.",
       "<b>Fold direction matters</b> unless the operation is associative <i>and</i> commutative."]),
    OUT("n3_scala_traps.out.txt", "Verified output", transform=pick("folds")),
    QA("Compute `List(1,2,3,4).foldLeft(0)(_ - _)` and `foldRight(0)(_ - _)`.", [P("foldLeft: ((((0-1)-2)-3)-4) = -10. foldRight: 1-(2-(3-(4-0))) = -2. Subtraction is not associative, so the direction changes the answer (output).")], "tricky"),
    QA("Reverse a list with `foldLeft`; copy it with `foldRight`.", [P("`foldLeft(List.empty[Int])((acc, x) => x :: acc)` gives `List(4,3,2,1)`; `foldRight(List.empty[Int])((x, acc) => x :: acc)` gives `List(1,2,3,4)` (output).")], "3 marks"),
    QA("Difference between `map` and `flatMap` with `List(\"hi\", \"yo\")` and `_.toList`.", [P("`map(_.toList)` gives `List(List(h,i), List(y,o))`; `flatMap(_.toList)` flattens to `List(h, i, y, o)`. `flatMap` also lets you chain `Option`s and generators in a for-comprehension.")], "3 marks"),
    QA("Trace `reduce`, `fold` and `scanLeft` on an empty list.", [P("`List.empty[Int].reduce(_ + _)` throws `UnsupportedOperationException`; `fold(0)(_ + _)` returns 0; use `reduceOption` or `fold` for possibly-empty data.")], "tricky"),
    QA("Create a list of the integers 1 to 10, filter evens, multiply by 3, build (n, n*n) tuples with flatMap, and the product with foldLeft.", [
        P("`xs.filter(_ % 2 == 0)`, `xs.map(_ * 3)`, `xs.flatMap(n => List((n, n * n)))`, `xs.foldLeft(1L)(_ * _)` = 3628800 (use `Long`; 13! already overflows `Int`). Output in 3.4.")], "5 marks"),
    QA("What does `for { i <- 1 to 3; j <- 1 to 2 if i != j } yield (i, j)` produce?", [P("`List((1,2), (2,1), (3,1), (3,2))`: nested generators with a guard (output).")], "predict the output"),
])

sub_3_6 = SUB("3.6", "Option and pattern matching", [
    B(["`Option[A]` is `Some(a)` or `None`; it replaces `null`. `map`, `flatMap`, `filter`, `getOrElse`, `fold`; a for-comprehension over Options gives `None` as soon as one is `None`.",
       "`match` tests patterns top to bottom: constants, variables, types (`case n: Int`), tuples, lists (`head :: tail`, `Nil`), case classes, guards (`if`), alternatives (`|`), binders (`x @ pattern`), wildcard `_`. The first match wins.",
       "On a `sealed` trait the compiler warns when a case is missing (exhaustiveness)."]),
    OUT("n3_scala_traps.out.txt", "Verified output", transform=pick("Option", "pattern matching")),
    QA("Why prefer `Option` to `null`?", [P("The possible absence is in the type, so the compiler makes you handle it; combinators (`map`, `getOrElse`) remove `if (x != null)` checks and `NullPointerException`s.")], "3 marks"),
    QA("Predict `describe` for `0`, `-5`, `\"scala\"`, `(1,2)`, `Nil`, `List(1,2,3)`.", [P("`zero`, `negative int -5`, `string of length 5`, `pair 1,2`, `empty list`, `list head=1 tail=List(2, 3)` (output). Order of cases matters: `case 0` must come before `case n: Int`.")], "predict the output"),
    QA("What does `val whole @ List(first, _*) = List(9, 8, 7)` bind?", [P("`whole = List(9, 8, 7)` and `first = 9`; `@` names the whole matched value and `_*` ignores the rest.")], "tricky"),
    QA("`Some(2)` and `Option.empty[Int]` in a for-comprehension: result?", [P("`None`. With `Some(2)` and `Some(3)` the result is `Some(6)`; a single `None` makes the whole expression `None`.")], "2 marks"),
])

sub_3_7 = SUB("3.7", "Classes, objects, constructors, this and method overloading", [
    B(["`class Point(val x: Int, var y: Int, tag: String)`: the class header is the <b>primary constructor</b>. `val` makes a read-only field, `var` a read/write field, a plain parameter is just a constructor parameter (private to the class if used inside).",
       "<b>Auxiliary constructors</b> are `def this(...)` and their first statement must call another constructor: `def this(x: Int) = this(x, 0, \"aux\")`.",
       "`this` is the current object; return `this` (type `this.type`) to chain calls. Use `this.y = y` when a parameter hides a field.",
       "<b>Overloading</b>: same name, different parameter lists, chosen at compile time. <b>Overriding</b>: a subclass replaces an inherited member (`override`), chosen at run time.",
       "Instances are created with `new`, or without `new` if a companion `apply` exists (case classes)."]),
    OUT("n3_oop_traps.out.txt", "Verified output", transform=pick("constructors", "initialisation")),
    OUT("m3_q2_oop.out.txt", "Verified output (question bank M3-C2)"),
    QA("Primary versus auxiliary constructor; what is the rule for the auxiliary one?", [P("The primary constructor is the class header and defines the fields. An auxiliary constructor (`def this`) must begin with a call to a previously defined constructor. This chains all constructors back to the primary one.")], "3 marks"),
    QA("What is the difference between `class P(x: Int)`, `class P(val x: Int)` and `class P(var x: Int)`?", [P("Plain: no accessor (`p.x` does not compile). `val`: a public read-only field. `var`: a public field with a setter.")], "tricky"),
    QA("What is printed when `Derived` overrides a `val` that `Base`'s constructor uses?", [
        P("`Base constructor sees name = null` and `name.length` throws `NullPointerException`. The superclass constructor runs before the subclass field is initialised, so the overriding `val` is still `null` (0 for numbers). "
          "Fixes: make the member a `def`, a `lazy val`, or avoid using it in the constructor (output shows `SafeBase` seeing \"derived\").")], "tricky"),
    QA("Show method overloading and say how it differs from overriding.", [SNIP("def deposit(amount: Double): Unit = { balance += amount }\ndef deposit(amount: Double, note: String): Unit = { balance += amount; println(note) }", lang="scala", caption="Account in m3_q2_oop.scala")], "3 marks"),
    QA("What does returning `this.type` allow?", [P("Method chaining: `p.moveTo(0, 0).moveTo(1, 1)` (output: `Point(1,1,t)`). Each call returns the same object.")], "2 marks"),
])

sub_3_8 = SUB("3.8", "Singleton, anonymous and companion objects", [
    B(["`object Config { ... }` is a <b>singleton</b>: one instance, created lazily on first use, no `new`. `object Main extends App` (or `def main`) is the program entry point.",
       "A <b>companion object</b> has the same name as a class and sits in the same file. Each can access the other's private members. It holds `apply` factories (so `Student(\"A\", 1)` works without `new`) and static-like helpers.",
       "An <b>anonymous class</b> is a one-off subclass created inline: `new Animal { override val sound = \"meow\" }`.",
       "`unapply` (in a companion/extractor object) powers pattern matching; case classes generate both `apply` and `unapply`."]),
    OUT("n3_oop_traps.out.txt", "Verified output", transform=pick("extractors")),
    QA("How does a companion object remove the need for `new`?", [P("The compiler rewrites `Student(\"Rohan\", 101)` to `Student.apply(\"Rohan\", 101)`, defined in the companion. The companion can call a private constructor, validate input, count instances (`created = 2` in the question-bank output) or return a subtype.")], "5 marks"),
    QA("What is the difference between a singleton object and a class?", [P("A class is a blueprint of which many instances can exist; an `object` is a single, ready-made instance, used for utilities, constants and `main`. There is no `static` keyword in Scala; companion objects play that role.")], "3 marks"),
    QA("What is `Secret.peek(Secret(21))` in the sample and why can it be called?", [P("42: the companion `apply` doubles the code and `peek` reads the private constructor's field. A companion may access the class's private members; outside code cannot call `new Secret(1)`.")], "tricky"),
    QA("What is an extractor?", [P("An object with `unapply` that tells `match` how to deconstruct a value. Output: `Even.unapply` made `10` match `case Even(h)` with half 5 while 7 fell through to `odd 7`.")], "2 marks"),
])

sub_3_9 = SUB("3.9", "Case classes", [
    B(["`case class Person(name: String, age: Int, city: String)`: constructor parameters become public `val` fields; the compiler adds `apply` (no `new`), `unapply` (pattern matching), structural `equals` and `hashCode`, readable `toString`, and `copy`.",
       "Meant for immutable data records. Combine with a `sealed trait` and `match` for algebraic data types; `case object` for singletons/enumerations.",
       "`copy` is <b>shallow</b>; an `Array` field is compared by reference, so two otherwise equal case classes holding arrays are not `==`."]),
    OUT("m3_q3_case_traits.out.txt", "Verified output (Lab 17 operations, then pattern matching)", transform=lambda t: "\n".join(t.split("\n")[:13])),
    OUT("n3_oop_traps.out.txt", "Verified output", transform=pick("sealed", "case class:")),
    QA("List four capabilities that distinguish a case class from an ordinary class.", [P("(1) public immutable fields from constructor parameters, (2) companion `apply` so no `new`, (3) structural `equals`/`hashCode`/`toString`, (4) `copy` with changed fields, and `unapply` for pattern matching.")], "5 marks"),
    QA("`Team(\"A\", Array(\"x\",\"y\")) == Team(\"A\", Array(\"x\",\"y\"))`: true or false?", [P("False. The two arrays are different objects and arrays use reference equality. Use a `List` or `Vector` field for structural equality.")], "tricky"),
    QA("What does `p1.copy(city = \"Pune\")` do, and is it a deep copy?", [P("It makes a new object with `city` replaced and the other fields reused; nested mutable objects are shared (output: the copied `Team` shares the same array).")], "3 marks"),
    QA("How does a `sealed trait` help `match`?", [P("All subclasses must be in the same file, so the compiler knows every case. A `match` that forgets `Dot` produces a warning. The `area` function covers `Circle`, `Rect` and `Dot`.")], "3 marks"),
    QA("Write the Lab 17 filter, group, format and sort operations.", [P("`people.filter(_.age > 30)`, `people.groupBy(_.city)`, `people.map(p => s\"${p.name} is ${p.age} years old and lives in ${p.city}\")`, `people.sortBy(_.age)`. Output in the question bank (M3-C3) and above.")], "5 marks"),
])

sub_3_10 = SUB("3.10", "Inheritance, field overriding, final and abstract classes", [
    B(["`class Dog extends Animal`. A subclass inherits members; `override` is <b>required</b> to replace a concrete member; `super.method()` calls the parent version.",
       "Fields can be overridden too: `override val sound = \"woof\"`. A `val` can override a parameterless `def`, but a `def` cannot override a `val`.",
       "`final` on a member forbids overriding; `final class` forbids extending; `sealed` restricts subclasses to the same file.",
       "<b>Abstract class</b>: may have abstract members (no body) and constructor parameters; cannot be instantiated. A concrete subclass implements them (`override` optional).",
       "Dynamic dispatch: the method run is chosen by the object's real class, not the variable's declared type."]),
    OUT("n3_oop_traps.out.txt", "Verified output", transform=pick("overriding")),
    QA("`val a: Animal = new Puppy(\"Bit\"); a.sound`: which version runs?", [P("`Puppy.sound`, giving `woof (squeaky)`. The declared type decides what you may call; the runtime class decides which implementation runs.")], "3 marks"),
    QA("What happens if you override a concrete method without `override`, or override a `final` one?", [P("Both are compile-time errors (\"needs `override` modifier\", \"cannot override final member\").")], "2 marks"),
    QA("Abstract class versus concrete class; can an abstract class have constructor parameters?", [P("Yes. `abstract class Animal(val name: String) { def sound: String }`. It cannot be instantiated with `new` (except as an anonymous subclass); subclasses supply the abstract members.")], "3 marks"),
    QA("Explain field overriding with a short example.", [SNIP("class Animal { val sound: String = \"...\" }\nclass Dog extends Animal { override val sound: String = \"woof\" }", lang="scala", caption="m3_q2_oop.scala")], "3 marks"),
])

sub_3_11 = SUB("3.11", "Traits, mixins and linearization (tricky topic)", [
    B(["A <b>trait</b> is like an interface that may also hold concrete methods and fields. A class can mix in many traits: `class Worker extends Logger with Auditor`; a single instance can too: `new Worker(\"K\") with Notifier`.",
       "Scala 2 traits cannot take constructor parameters (Scala 3 allows them). Abstract classes can, and a class extends only one class.",
       "<b>Linearization</b> solves the diamond problem: the parent chain is flattened to one line, so `super` always means exactly one thing. For `class D extends B with C` (both extend `A`): "
       "L(D) = D, L(C) then L(B) with duplicates removed leaving the later occurrence = <b>D, C, B, A</b>. `super.who` in D runs C first, then B, then A.",
       "<b>The order of `with` matters</b>: the right-most trait is consulted first."]),
    OUT("m3_q3_case_traits.out.txt", "Verified output (question bank M3-C3/C4)", transform=lambda t: "\n".join(t.split("\n")[-6:])),
    OUT("n3_oop_traps.out.txt", "Verified output", transform=pick("trait mixin")),
    QA("What does `(new D).who` print for `trait A {def who=\"A\"}`, `trait B extends A {override def who=\"B > \"+super.who}`, `trait C extends A {... \"C > \"...}`, `class D extends B with C {... \"D > \"...}`?", [
        P("`D > C > B > A`. L(D) = D, C, B, A (output). Each `super.who` moves one step to the right along that line.")], "predict the output"),
    QA("Show that the order of mixins changes the result: `Greeter with Loud with Polite` versus `Greeter with Polite with Loud`.", [
        P("The first gives `HELLO ASHA, please` (Polite is outermost: Loud upper-cases first, then Polite appends); the second gives `HELLO ASHA, PLEASE` (Loud is outermost and upper-cases everything Polite produced). Output above.")], "tricky"),
    QA("Trait versus abstract class.", [
        T(["", "Trait", "Abstract class"], [["Inheritance", "many per class (mixin)", "one per class"], ["Constructor parameters", "Scala 2: no; Scala 3: yes", "yes"], ["Java interop", "compiles to an interface", "abstract class"],
                                             ["Use", "reusable capabilities (logging)", "a base type with state and a constructor"]], [0.25, 0.4, 0.35])], "3 marks"),
    QA("Compare linearization in Scala with Python's MRO.", [P("Both flatten multiple inheritance into one order so `super` is unambiguous. Python (C3) gives `D > B > C > A` for `class D(B, C)` with the leftmost parent first; Scala mixes right to left, so `extends B with C` gives `D, C, B, A`. In both, the shared base `A` appears once, last.")], "tricky"),
    QA("Can a trait have a concrete method and a field?", [P("Yes: `trait Logger { def log(m: String): Unit = println(m) }`, plus abstract members that the class must define. `Worker` in the output uses `log` and `audit` from two traits.")], "2 marks"),
])

sub_3_12 = SUB("3.12", "Access modifiers", [
    T(["Modifier", "Visible in"], [["(none)", "public: everywhere (the default)"], ["`protected`", "the class and its subclasses (not the whole package, unlike Java)"],
                                    ["`private`", "the class itself and its companion object"], ["`private[this]`", "only the same instance"], ["`private[pkg]`", "the named enclosing package or class"]], [0.25, 0.75]),
    OUT("m3_q2_oop.out.txt", "Verified output (Base and Child classes: `protected, public, private` is printed by `c.peek`, `c.open`, `c.reveal`)", transform=lambda t: "\n".join(t.split("\n")[5:6])),
    QA("What is the default access level, and how does `protected` differ from Java?", [P("Public. Scala's `protected` allows subclasses only; Java also allows the same package.")], "2 marks"),
    QA("Can the companion object read a `private` field of its class?", [P("Yes, and vice versa; this is why a companion `apply` can call a `private` constructor.")], "2 marks"),
    QA("A subclass tries `c.secret` where `secret` is `private` in `Base`. Result?", [P("Compile error: value secret in class Base cannot be accessed. Through the public method `reveal` the value is reachable (output `private`).")], "2 marks"),
])

sub_3_13 = SUB("3.13", "Scala arrays and the REPL", [
    B(["Arrays are fixed-size JVM arrays: `val a = Array(2, 5, 9)`, index with <b>parentheses</b> `a(0)`, update `a(0) = 10` (allowed even for a `val`). Iterate with `for (x <- a)` or `a.foreach(println)`; `a.sum`, `a.mkString(\",\")`, `a.map`, `a.filter`. `Array.fill(3)(0)`, `Array.ofDim[Int](2, 3)`.",
       "Equality is by reference; compare with `sameElements`. Use `ArrayBuffer` when the size must change.",
       "<b>REPL</b> (Read-Eval-Print Loop): start with `scala` (or `scala-cli repl`). Each expression is evaluated and printed with a generated name (`res0: Int = 5`). Commands: `:help`, `:paste` (multi-line, finish with Ctrl-D), `:type expr`, `:load file`, `:reset`, `:quit`. "
       "(REPL sessions were not recorded in this document; the array operations below were run as a compiled program.)"]),
    OUT("m3_q1_collections.out.txt", "Verified output", transform=lambda t: "\n".join(t.split("\n")[:1])),
    OUT("n3_scala_traps.out.txt", "Verified output", transform=pick("equality")),
    QA("Create an array 2, 5, 9, 14, 20; write a function returning its sum; join a fruit array with commas; print each element.", [
        P("`val nums = Array(2, 5, 9, 14, 20)`, `def sum(a: Array[Int]) = a.sum`, `fruits.mkString(\",\")`, `for (n <- nums) println(n)`. Output (Lab 13): `sum = 147` after the program changed `nums(0)` to 99, `joined = apple,banana,cherry,mango,orange`.")], "5 marks"),
    QA("Why does `Array(1,2) == Array(1,2)` give false, and what is the fix?", [P("Arrays use Java reference equality. Use `a.sameElements(b)` or compare `a.toList == b.toList` (both true in the output).")], "tricky"),
    QA("What is the REPL used for, and how do you enter a multi-line definition?", [P("Quick experiments with expressions, collections and library calls without a project. Type `:paste`, paste the code, press Ctrl-D.")], "2 marks"),
])

NOTES_3 = NMODULE(
    3, "Scala data structures and object-oriented programming", "12 hours",
    "expanded function format; variables and strings; user input; numbers; variable types; operators; booleans; arrays, lists, tuples, sets, hash set, maps; functional combinators; objects and classes; anonymous object, singleton; companion object, case classes; constructors; method overloading; `this`; inheritance; field overriding; `final`; abstract class; trait and mixins; access modifiers; Scala array and the REPL.",
    [("Expanded function format", "3.1"), ("Variables and strings; getting user input", "3.2"), ("Numbers, variable types, operators, booleans", "3.3"),
     ("Arrays, lists, tuples, sets, hash set, maps", "3.4"), ("Functional combinators (map, flatMap, fold ...)", "3.5"), ("Option and pattern matching", "3.6"),
     ("Objects and classes, constructors, method overloading, `this`", "3.7"), ("Anonymous object, singleton, companion object", "3.8"), ("Case classes", "3.9"),
     ("Inheritance, field overriding, final, abstract class", "3.10"), ("Trait, trait mixins", "3.11"), ("Access modifiers", "3.12"), ("Scala array, REPL", "3.13")],
    [sub_3_1, sub_3_2, sub_3_3, sub_3_4, sub_3_5, sub_3_6, sub_3_7, sub_3_8, sub_3_9, sub_3_10, sub_3_11, sub_3_12, sub_3_13],
)
