r"""Task tables (Task | Code) for the SCALA syllabus topics that the lab-based cheat sheet does not cover.
Row flags (same meaning as cheat_scala.py):  ""  statement inside main()      "import"  placed at the top of the file
  "top"  declaration placed before the object (classes, traits, objects)      "wrapper"  shown only      "skip"  shown, not run
  "repl" a Scala REPL transcript: lines starting with "scala> " are typed, the other lines are the REPL's replies
A 4th element, when present, is what is compiled instead of the displayed code (used for the Spark session builder).
verify_gap_scala.py assembles each group into one program, compiles it with scala-cli (Scala 2.13.12) and runs it.
"""

SGROUPS = []
SKIP_REASON = {"Structured Streaming: a rate source into a memory table":
               "not run: Spark writes a checkpoint, which needs winutils.exe on Windows (standard code on Linux / Colab)"}

SPARK_OPTS = ("--add-opens=java.base/java.lang=ALL-UNNAMED --add-opens=java.base/java.lang.invoke=ALL-UNNAMED --add-opens=java.base/java.lang.reflect=ALL-UNNAMED "
              "--add-opens=java.base/java.io=ALL-UNNAMED --add-opens=java.base/java.net=ALL-UNNAMED --add-opens=java.base/java.nio=ALL-UNNAMED "
              "--add-opens=java.base/java.util=ALL-UNNAMED --add-opens=java.base/java.util.concurrent=ALL-UNNAMED "
              "--add-opens=java.base/java.util.concurrent.atomic=ALL-UNNAMED --add-opens=java.base/sun.nio.ch=ALL-UNNAMED "
              "--add-opens=java.base/sun.nio.cs=ALL-UNNAMED --add-opens=java.base/sun.security.action=ALL-UNNAMED --add-opens=java.base/sun.util.calendar=ALL-UNNAMED")


def c(s):
    return s.strip("\n")


def sgroup(gid, title, topics, rows, note="", deps=(), directives=(), stdin=""):
    SGROUPS.append(dict(id=gid, title=title, topics=topics, deps=list(deps), directives=list(directives), rows=rows, note=note, stdin=stdin))


ENTRY = ("Entry point: statements below go inside main", "object Experiment {\n  def main(args: Array[String]): Unit = {\n    // statements go here\n  }\n}", "wrapper")

# ------------------------------------------------------------------------------------------------ 3.1
sgroup("3.1", "Functions: the expanded function format", "Module 3: Expanded Function Format", [
    ENTRY,
    ("Full form: parameters, result type, block body", c(r'''
def add(a: Int, b: Int): Int = {
  a + b
}
println(add(2, 3))
''')),
    ("Short form: one expression, inferred result type", "def square(x: Int) = x * x\nprintln(square(7))"),
    ("A function with no useful result (Unit)", c(r'''
def greet(name: String): Unit = println(s"Hello, $name")
greet("VIT")
''')),
    ("Default and named arguments", c(r'''
def area(w: Double = 1.0, h: Double = 1.0): Double = w * h
println(area())
println(area(h = 5, w = 2))
''')),
    ("Variable number of arguments", "def total(nums: Int*): Int = nums.sum\nprintln(total(1, 2, 3))\nprintln(total(List(4, 5, 6): _*))"),
    ("Function values (literals) and their types", "val double: Int => Int = x => x * 2\nval add3 = (a: Int, b: Int, c: Int) => a + b + c\nprintln(double(21))\nprintln(add3(1, 2, 3))"),
    ("Placeholder syntax", "val nums = List(1, 2, 3, 4)\nprintln(nums.map(_ * 10))\nprintln(nums.filter(_ % 2 == 0))\nprintln(nums.reduce(_ + _))"),
    ("Higher-order function: takes a function", "def applyTwice(f: Int => Int, x: Int): Int = f(f(x))\nprintln(applyTwice(_ + 3, 10))\nprintln(applyTwice(double, 5))"),
    ("A function that returns a function (closure)", "def multiplier(factor: Int): Int => Int = x => x * factor\nval triple = multiplier(3)\nprintln(triple(14))"),
    ("Currying: several parameter lists", "def addC(a: Int)(b: Int): Int = a + b\nval add10 = addC(10) _\nprintln(addC(1)(2))\nprintln(add10(5))"),
    ("Tail recursion", "import scala.annotation.tailrec", "import"),
    ("Recursive factorial that cannot overflow the stack", c(r'''
@tailrec
def factorial(n: Int, acc: BigInt = 1): BigInt =
  if (n <= 1) acc else factorial(n - 1, acc * n)
println(factorial(20))
''')),
    ("By-name parameter: evaluated every time it is used", "def twice(block: => Unit): Unit = { block; block }\ntwice(println(\"run\"))"),
    ("Generic function", "def firstOf[T](items: List[T]): Option[T] = items.headOption\nprintln(firstOf(List(\"a\", \"b\")))\nprintln(firstOf(List.empty[Int]))"),
    ("Nested function and a tuple result", c(r'''
def stats(xs: List[Double]): (Double, Double) = {
  def mean(v: List[Double]) = v.sum / v.size
  val m = mean(xs)
  (m, math.sqrt(xs.map(x => math.pow(x - m, 2)).sum / xs.size))
}
val (mu, sd) = stats(List(2.0, 4.0, 4.0, 4.0, 5.0, 5.0, 7.0, 9.0))
println(s"mean=$mu sd=$sd")
''')),
    ("Turn a method into a function value", "def inc(x: Int) = x + 1\nval f = inc _\nprintln(List(1, 2, 3).map(inc))\nprintln(f(9))"),
], note="def name(parameters): ResultType = { body }. The last expression is the result, no return keyword is needed. Recursive functions must state their result type.")

# ------------------------------------------------------------------------------------------------ 3.2
sgroup("3.2", "Variables, strings, numbers and types", "Module 3: Variables and Strings, Numbers, Variable types", [
    ENTRY,
    ("val, var and lazy val", c(r'''
val pi = 3.14159
var counter = 0
counter += 1
lazy val heavy = { println("computing..."); 42 }
println(counter)
println(heavy)
println(heavy)
''')),
    ("Type inference and explicit types", "val a = 10\nval b: Double = 10\nval c = \"text\"\nval d = 3.5f\nval e: Long = 1L << 40\nprintln((a.getClass.getSimpleName, b.getClass.getSimpleName, c.getClass.getSimpleName, d, e))"),
    ("Strings: length, index, case, substring", c(r'''
val s = "  Data Science  "
val t = s.trim
println(t.length)
println(t(0))
println(t.toUpperCase)
println(t.toLowerCase)
println(t.substring(0, 4))
println(t.charAt(5))
println(t.reverse)
''')),
    ("Search, replace, split, count", "println(t.contains(\"Sci\"))\nprintln(t.indexOf(\"Science\"))\nprintln(t.startsWith(\"Data\"))\nprintln(t.replace(\"Data\", \"Big\"))\nprintln(t.split(\" \").toList)\nprintln(t.count(_ == 'a'))"),
    ("String interpolation: s, f, raw", c(r'''
val name = "Asha"
val marks = 91.456
println(s"$name scored ${marks + 1}")
println(f"$name scored $marks%.1f")
println(raw"no\tescape")
''')),
    ("Multi-line strings", c(r'''
val text = """first line
   |second line""".stripMargin
println(text)
''')),
    ("Compare and join strings", c(r'''
println("abc" == "abc")
println("apple" < "banana")
println("a" + "b" * 3)
println(List("x", "y", "z").mkString("-"))
println("b".compareTo("a"))
''')),
    ("Numeric types and their limits", "println((Byte.MaxValue, Short.MaxValue, Int.MaxValue, Long.MaxValue))\nprintln(Int.MaxValue + 1)\nprintln(Double.MaxValue > 1e300)"),
    ("Integer and floating-point arithmetic", "println(7 / 2)\nprintln(7 % 2)\nprintln(7 / 2.0)\nprintln(7.toDouble / 2)\nprintln(-7 / 2)\nprintln(-7 % 3)\nprintln(math.floorMod(-7, 3))"),
    ("Conversions", c(r'''
println("42".toInt + 1)
println(3.99.toInt)
println(65.toChar)
println('A'.toInt)
println(10.toString + "!")
println("3.5".toDouble * 2)
println("abc".toIntOption)
''')),
    ("Math functions and rounding", "println(math.sqrt(16))\nprintln(math.pow(2, 10))\nprintln(math.abs(-5))\nprintln(math.max(3, 9))\nprintln(math.round(2.5))\nprintln(math.ceil(2.1))\nprintln(math.floor(2.9))\nprintln(f\"${math.Pi}%.4f\")"),
    ("Big numbers and exact decimals", "val big = BigInt(\"123456789012345678901234567890\")\nprintln(big * 2)\nprintln(BigDecimal(\"0.1\") + BigDecimal(\"0.2\"))\nprintln(0.1 + 0.2)"),
    ("Characters", "val ch = 'q'\nprintln(ch.isLetter)\nprintln(ch.toUpper)\nprintln(ch + 1)\nprintln((ch + 1).toChar)"),
    ("The type hierarchy: Any, AnyVal, AnyRef", c(r'''
val things: List[Any] = List(1, "two", 3.0, true, 'c')
things.foreach(t => println(t.getClass.getSimpleName))
println(things(1).isInstanceOf[String])
println(things(0).asInstanceOf[Int] + 1)
''')),
    ("Option instead of null", "val maybe: Option[Int] = Some(5)\nval none: Option[Int] = None\nprintln(maybe.getOrElse(0))\nprintln(none.getOrElse(0))\nprintln(maybe.map(_ * 2))"),
    ("Type alias and tuples", "type Point = (Double, Double)\nval p: Point = (1.5, 2.5)\nprintln(p._1 + p._2)"),
], note="val cannot be reassigned, var can. Int / Int is integer division. Int.MaxValue + 1 silently wraps around to a negative number. Use BigInt / BigDecimal when exactness matters.")

# ------------------------------------------------------------------------------------------------ 3.3
sgroup("3.3", "Operators, booleans, control flow and user input", "Module 3: Getting user input, Operators, Booleans", [
    ENTRY,
    ("Input reading and loop control imports", "import scala.io.StdIn\nimport scala.util.control.Breaks._", "import"),
    ("Arithmetic operators", "val a = 17\nval b = 5\nprintln(a + b)\nprintln(a - b)\nprintln(a * b)\nprintln(a / b)\nprintln(a % b)"),
    ("Relational operators", "println((a > b, a < b, a >= 17, a <= 5, a == b, a != b))"),
    ("Logical operators and short-circuit evaluation", c(r'''
val t = true
val f = false
println((t && f, t || f, !t, t ^ f))
def boom(): Boolean = { println("evaluated"); true }
println(f && boom())
println(t || boom())
''')),
    ("Bitwise operators", "println((12 & 10, 12 | 10, 12 ^ 10, ~12, 1 << 4, -16 >> 2, -16 >>> 28))"),
    ("Compound assignment", "var x = 10\nx += 5\nx -= 3\nx *= 2\nx /= 4\nx %= 4\nprintln(x)"),
    ("Operators are methods", "println(5.+(3))\nprintln(5 max 9)\nprintln(List(1, 2) ++ List(3))\nprintln(1 to 3)"),
    ("Precedence", "println(2 + 3 * 4)\nprintln((2 + 3) * 4)\nprintln(10 - 4 - 3)\nprintln(2 + 3 > 4 && 1 < 2)"),
    ("Boolean values in collections", "val isEven = (n: Int) => n % 2 == 0\nprintln(isEven(4))\nval nums = List(1, 2, 3, 4)\nprintln((nums.count(isEven), nums.exists(_ > 3), nums.forall(_ > 0)))"),
    ("if / else is an expression", "val n = 15\nval size = if (n < 10) \"small\" else if (n < 20) \"medium\" else \"large\"\nprintln(size)"),
    ("match with guards and types", c(r'''
def describe(x: Any): String = x match {
  case 0 => "zero"
  case i: Int if i < 0 => "negative int"
  case _: Int => "positive int"
  case s: String => s"text of length ${s.length}"
  case (p, q) => s"pair $p,$q"
  case _ => "something else"
}
List(0, -4, 8, "hey", (1, 2), 2.5).foreach(v => println(describe(v)))
''')),
    ("for loops: ranges, until, by, nested", c(r'''
for (i <- 1 to 3) print(s"$i ")
println()
for (i <- 1 until 10 by 3) print(s"$i ")
println()
for (i <- 1 to 3; j <- 1 to 2) print(s"($i,$j) ")
println()
''')),
    ("for with a guard and yield", "val squares = for (i <- 1 to 10 if i % 2 == 0) yield i * i\nprintln(squares)"),
    ("while and do-while", "var k = 3\nwhile (k > 0) { print(k + \" \"); k -= 1 }\nprintln()\nvar m = 0\ndo { m += 1 } while (m < 5)\nprintln(m)"),
    ("break out of a loop", c(r'''
breakable {
  for (i <- 1 to 10) {
    if (i == 4) break()
    print(s"$i ")
  }
}
println()
''')),
    ("Read from the keyboard", c(r'''
print("Enter your name: ")
val name = StdIn.readLine()
print("Enter marks: ")
val marks = StdIn.readInt()
println(s"Hello $name, your marks are $marks")
''')),
    ("Read several numbers from one line", "val numbers = StdIn.readLine().split(\" \").map(_.toInt)\nprintln(numbers.sum)"),
], note="Scala has no break or continue keyword: use breakable { ... break() } or filter the loop with a guard. A user typing something that is not a number makes readInt throw NumberFormatException.",
    stdin="Rohan\n85\n3 4 5\n")

# ------------------------------------------------------------------------------------------------ 3.4
REPL_ARRAY = c(r'''
scala> val a = Array(1, 2, 3)
val a: Array[Int] = Array(1, 2, 3)

scala> a.map(_ * 2)
val res0: Array[Int] = Array(2, 4, 6)

scala> a(0) = 9

scala> a
val res2: Array[Int] = Array(9, 2, 3)

scala> a.length
val res3: Int = 3

scala> a :+ 4
val res4: Array[Int] = Array(9, 2, 3, 4)

scala> val m = Array.ofDim[Int](2, 2)
val m: Array[Array[Int]] = Array(Array(0, 0), Array(0, 0))

scala> m(1)(1) = 5

scala> m
val res6: Array[Array[Int]] = Array(Array(0, 0), Array(0, 5))

scala> a.sum
val res7: Int = 14
''')
sgroup("3.4", "Arrays, HashSet and the other mutable collections; the REPL", "Module 3: Arrays, Hash set, Scala Array-REPL", [
    ENTRY,
    ("Imports", "import scala.collection.mutable\nimport scala.collection.immutable.{HashSet, TreeMap, TreeSet}", "import"),
    ("Mutable HashSet: unique elements, fast lookup", "val hs = mutable.HashSet(3, 1, 4, 1, 5)\nhs += 9\nhs -= 1\nprintln(hs.contains(4))\nprintln(hs.size)\nprintln(hs.toList.sorted)"),
    ("Set algebra on HashSets", "val s1 = mutable.HashSet(1, 2, 3)\nval s2 = mutable.HashSet(3, 4)\nprintln((s1 union s2).toList.sorted)\nprintln((s1 intersect s2).toList)\nprintln((s1 diff s2).toList.sorted)\nprintln(s1.subsetOf(s1 union s2))"),
    ("Immutable HashSet returns a new set", "val frozen = HashSet(\"a\", \"b\")\nval more = frozen + \"c\"\nprintln((frozen.size, more.size))"),
    ("ArrayBuffer: a growable array", "val buf = mutable.ArrayBuffer(1, 2, 3)\nbuf += 4\nbuf ++= List(5, 6)\nbuf.insert(0, 0)\nbuf.remove(1)\nprintln(buf)"),
    ("ListBuffer", "val lb = mutable.ListBuffer[String]()\nlb += \"x\"\nlb += \"y\"\nprintln(lb.toList)"),
    ("Mutable queue and stack", "val q = mutable.Queue(1, 2, 3)\nq.enqueue(4)\nprintln(q.dequeue())\nval st = mutable.Stack(1, 2, 3)\nst.push(9)\nprintln(st.pop())\nprintln(q)\nprintln(st)"),
    ("Mutable Map", "val stock = mutable.Map(\"apple\" -> 10)\nstock(\"pear\") = 5\nstock += (\"fig\" -> 2)\nstock.getOrElseUpdate(\"kiwi\", 7)\nstock -= \"fig\"\nprintln(stock.toList.sortBy(_._1))"),
    ("Sorted collections", "val tm = TreeMap(\"b\" -> 2, \"a\" -> 1)\nval ts = TreeSet(5, 1, 3)\nprintln(tm)\nprintln(ts)"),
    ("Array: create, update, sort", c(r'''
val arr = Array(5, 3, 8, 1)
arr(0) = 50
println(arr.mkString(", "))
println(arr.length)
println(arr.sorted.mkString(","))
println(arr.sortWith(_ > _).mkString(","))
println(arr.reverse.toList)
''')),
    ("More array operations", c(r'''
println(arr.indexOf(8))
println(arr.slice(1, 3).toList)
println(arr.max)
println(arr.contains(3))
println(arr.zip(Array("a", "b", "c", "d")).toList)
println(Array.fill(3)(0).toList)
println(Array.tabulate(4)(i => i * i).toList)
println(Array.range(0, 10, 3).toList)
''')),
    ("Two-dimensional arrays", c(r'''
val grid = Array.ofDim[Int](2, 3)
grid(1)(2) = 7
grid.foreach(row => println(row.mkString(" ")))
val table = Array(Array(1, 2), Array(3, 4))
println(table.map(_.sum).toList)
println(table.flatten.toList)
''')),
    ("Arrays compare by reference", "val x = Array(1, 2)\nval y = Array(1, 2)\nprintln(x == y)\nprintln(x.sameElements(y))\nprintln(x.toList == y.toList)"),
    ("The Scala REPL: type an expression, read the answer", REPL_ARRAY, "repl"),
], note="Start the REPL by typing `scala` (or `scala-cli repl`) in a terminal; `:quit` leaves it. The REPL names unnamed results res0, res1, ... and an assignment such as a(0) = 9 also uses up a number even though it prints nothing. "
        "The transcript was produced by running exactly those lines in the Scala 2.13 REPL engine.")

# ------------------------------------------------------------------------------------------------ 3.5
sgroup("3.5", "Classes and objects: constructors, overloading, this, singleton, companion, case classes, access modifiers", 
       "Module 3: Scala Object and Class, Anonymous object, Singleton, Companion Object, Case Classes, Constructors, Method Overloading, This Keyword, Access Modifiers", [
    ENTRY,
    ("A class with constructor parameters, fields and methods", c(r'''
class Student(val name: String, var marks: Int) {
  private val college = "VIT"
  def grade: String = if (marks >= 90) "S" else if (marks >= 75) "A" else "B"
  def curve(extra: Int): Unit = { marks += extra }
  override def toString: String = s"$name ($marks, $grade) of $college"
}
''') , "top"),
    ("Create objects and use them", "val s = new Student(\"Asha\", 80)\nprintln(s)\ns.curve(12)\nprintln(s.grade)\ns.marks = 70\nprintln(s.marks)\nprintln(s.name)"),
    ("An anonymous object: created and used once", "println(new Student(\"Anon\", 60).grade)"),
    ("Parameters without val / var stay private", c(r'''
class Counter(start: Int) {
  private var count = start
  def next(): Int = { count += 1; count }
}
''') , "top"),
    ("Use it", "val counter = new Counter(10)\nprintln(counter.next())\nprintln(counter.next())"),
    ("Auxiliary constructors and the this keyword", c(r'''
class Rectangle(val width: Double, val height: Double) {
  def this(side: Double) = this(side, side)
  def this() = this(1.0)
  def area: Double = width * height
  def scale(k: Double): Rectangle = new Rectangle(width * k, height * k)
  def biggerThan(other: Rectangle): Boolean = this.area > other.area
}
''') , "top"),
    ("Call the three constructors", "println(new Rectangle(2, 3).area)\nprintln(new Rectangle(4).area)\nprintln(new Rectangle().area)\nprintln(new Rectangle(2, 3).scale(2).area)\nprintln(new Rectangle(5).biggerThan(new Rectangle(2, 3)))"),
    ("Return this to chain method calls", c(r'''
class Builder {
  private val parts = scala.collection.mutable.ListBuffer[String]()
  def add(p: String): this.type = { parts += p; this }
  def build: String = parts.mkString(" ")
}
''') , "top"),
    ("Chain the calls", "println(new Builder().add(\"data\").add(\"science\").build)"),
    ("Method overloading: same name, different parameters", c(r'''
class Printer {
  def show(x: Int): String = s"int $x"
  def show(x: String): String = s"string $x"
  def show(x: Int, y: Int): String = s"two ints ${x + y}"
}
''') , "top"),
    ("Call the overloaded methods", "val p = new Printer\nprintln(p.show(5))\nprintln(p.show(\"hi\"))\nprintln(p.show(2, 3))"),
    ("Singleton object: exactly one instance, no new", c(r'''
object AppConfig {
  val appName = "PDS"
  private var visits = 0
  def visit(): Int = { visits += 1; visits }
}
''') , "top"),
    ("Use the singleton", "println(AppConfig.appName)\nAppConfig.visit()\nprintln(AppConfig.visit())"),
    ("Companion object: factory apply, shared constants, private constructor", c(r'''
class Account private (val id: Int, var balance: Double)

object Account {
  private var nextId = 1000
  val MinBalance = 100.0
  def apply(initial: Double): Account = {
    require(initial >= MinBalance, s"opening balance must be at least $MinBalance")
    nextId += 1
    new Account(nextId, initial)
  }
}
''') , "top"),
    ("Use the companion", "val acc = Account(500)\nprintln((acc.id, acc.balance))\nprintln(Account.MinBalance)\ntry Account(5) catch { case e: IllegalArgumentException => println(e.getMessage) }"),
    ("unapply: make an object usable in pattern matching", c(r'''
object Email {
  def unapply(s: String): Option[(String, String)] = s.split("@") match {
    case Array(user, domain) => Some((user, domain))
    case _ => None
  }
}
''') , "top"),
    ("Match with the extractor", "\"asha@vit.ac.in\" match {\n  case Email(u, d) => println(s\"user=$u domain=$d\")\n  case _ => println(\"not an email\")\n}"),
    ("A trait implemented by an anonymous class", "trait Greeter { def greet(name: String): String }", "top"),
    ("Anonymous classes and the shorter lambda form", c(r'''
val formal = new Greeter { def greet(name: String) = s"Good day, $name" }
val shout: Greeter = name => name.toUpperCase + "!"
println(formal.greet("Rao"))
println(shout.greet("hey"))
''')),
    ("Case class: equality, copy, pattern matching come for free", "case class Employee(name: String, dept: String, salary: Double)", "top"),
    ("Use the case class", c(r'''
val e1 = Employee("Asha", "IT", 50000)
val e2 = e1.copy(salary = 55000)
println(e1)
println(e1 == Employee("Asha", "IT", 50000))
println(e2.salary)
e1 match {
  case Employee(n, "IT", s) if s > 40000 => println(s"$n is a well-paid IT employee")
  case _ => println("other")
}
''')),
    ("Case class with its own companion method", c(r'''
case class Temperature(celsius: Double) {
  def fahrenheit: Double = celsius * 9 / 5 + 32
}

object Temperature {
  def fromFahrenheit(f: Double): Temperature = Temperature((f - 32) * 5 / 9)
}
''') , "top"),
    ("Use it", "println(Temperature.fromFahrenheit(212))\nprintln(Temperature(100).fahrenheit)"),
    ("Access modifiers: private, protected, public", c(r'''
class Vault {
  private val secret = 42                  // inside Vault only (other Vault objects included)
  protected val hint = "starts with 4"     // Vault and its subclasses
  val label = "public"                     // everywhere (the default)
  def reveal(other: Vault): Int = other.secret
}

class SubVault extends Vault {
  def showHint: String = hint
}
''') , "top"),
    ("Use them", "val v = new Vault\nprintln(v.label)\nprintln(v.reveal(new Vault))\nprintln(new SubVault().showHint)"),
    ("Write equals and hashCode yourself for an ordinary class", c(r'''
class Point2(val x: Int, val y: Int) {
  override def equals(o: Any): Boolean = o match {
    case p: Point2 => p.x == x && p.y == y
    case _ => false
  }
  override def hashCode: Int = (x, y).hashCode
}
''') , "top"),
    ("Compare them", "println(new Point2(1, 2) == new Point2(1, 2))\nprintln(Set(new Point2(1, 2), new Point2(1, 2)).size)"),
], note="A class parameter marked val / var becomes a public field, an unmarked one stays private. Only a case class gets apply, copy, equals, hashCode, toString and unapply automatically; a plain class needs `new`. "
        "Trying to read a private member from outside does not compile (value secret in class Vault cannot be accessed).")

# ------------------------------------------------------------------------------------------------ 3.6
sgroup("3.6", "Inheritance, overriding, final, abstract classes, traits and mixins", "Module 3: Inheritance, Field Overriding, Final, Abstract Class, Trait, Trait Mixins", [
    ENTRY,
    ("extends and override; super calls the parent version", c(r'''
class Animal(val name: String) {
  def sound: String = "..."
  def describe: String = s"$name says $sound"
}

class Dog(name: String) extends Animal(name) {
  override def sound: String = "Woof"
}

class Puppy(name: String) extends Dog(name) {
  override def sound: String = super.sound + " (squeaky)"
}
''') , "top"),
    ("Polymorphism: the subclass method runs", "val animals: List[Animal] = List(new Animal(\"Generic\"), new Dog(\"Rex\"), new Puppy(\"Bit\"))\nanimals.foreach(a => println(a.describe))"),
    ("Type tests and pattern matching on classes", c(r'''
animals.foreach {
  case d: Dog => println(s"${d.name} is a Dog")
  case a => println(s"${a.name} is some Animal")
}
println(animals(1).isInstanceOf[Dog])
println(animals.map(_.getClass.getSimpleName))
''')),
    ("Field overriding: override a val", c(r'''
class Vehicle {
  val wheels: Int = 4
  def info: String = s"$wheels wheels"
}

class Bike extends Vehicle {
  override val wheels: Int = 2
}
''') , "top"),
    ("See the overridden field", "println(new Vehicle().info)\nprintln(new Bike().info)"),
    ("Trap: a parent constructor reads the field before the child sets it", c(r'''
class Base {
  val size: Int = 10
  val doubled: Int = size * 2
}

class Derived extends Base {
  override val size: Int = 100
}
''') , "top"),
    ("The surprising result", "val d = new Derived\nprintln((d.size, d.doubled))"),
    ("final: no overriding and no further subclasses", c(r'''
class Parent {
  final def id: Int = 1
}

final class Leaf extends Parent
''') , "top"),
    ("Use the final members", "println(new Leaf().id)"),
    ("Abstract class: abstract members plus concrete ones", c(r'''
abstract class Shape {
  def area: Double                 // abstract: no body
  val sides: Int                   // abstract value
  def describe: String = f"$sides sides, area $area%.2f"
}

class Square(side: Double) extends Shape {
  val sides = 4
  def area: Double = side * side
}

class Circle(r: Double) extends Shape {
  val sides = 0
  def area: Double = math.Pi * r * r
}
''') , "top"),
    ("Use the abstract class", "List(new Square(3), new Circle(1)).foreach(s => println(s.describe))"),
    ("Traits: reusable behaviour, with abstract and concrete members", c(r'''
trait Logger {
  def log(msg: String): Unit = println(s"[LOG] $msg")
}

trait Auditable {
  def auditId: String
}

class Service(val auditId: String) extends Logger with Auditable {
  def run(): Unit = log(s"service $auditId started")
}
''') , "top"),
    ("Use the mixed-in trait", "new Service(\"S-1\").run()"),
    ("Mix traits in when the object is created", c(r'''
class Basic
trait Walks { def move = "walks" }
trait Swims { def swim = "swims" }
''') , "top"),
    ("Create a mixed object", "val duck = new Basic with Walks with Swims\nprintln(duck.move + \" and \" + duck.swim)"),
    ("Stackable traits: the order of mixing changes the result", c(r'''
abstract class Text {
  def render: String
}

class Plain extends Text {
  def render = "hello"
}

trait Reverse extends Text {
  abstract override def render: String = super.render.reverse
}

trait Exclaim extends Text {
  abstract override def render: String = super.render + "!"
}
''') , "top"),
    ("Compare the two orders", "println((new Plain with Reverse with Exclaim).render)\nprintln((new Plain with Exclaim with Reverse).render)"),
    ("Sealed trait with case classes: the compiler checks the match is complete", c(r'''
sealed trait Figure
case class Circ(r: Double) extends Figure
case class Rect(w: Double, h: Double) extends Figure
case object Dot extends Figure
''') , "top"),
    ("Match on the sealed hierarchy", c(r'''
def areaOf(f: Figure): Double = f match {
  case Circ(r)    => math.Pi * r * r
  case Rect(w, h) => w * h
  case Dot        => 0.0
}
println(List(Circ(1), Rect(2, 3), Dot).map(areaOf).map(a => f"$a%.2f"))
''')),
    ("Constructors run from the top of the hierarchy down", c(r'''
class A { println("A constructor") }
class B extends A { println("B constructor") }
class C extends B { println("C constructor") }
''') , "top"),
    ("Create a C", "new C"),
    ("Ordered: compare your own objects", c(r'''
class Version(val major: Int, val minor: Int) extends Ordered[Version] {
  def compare(that: Version): Int = if (major != that.major) major - that.major else minor - that.minor
  override def toString = s"$major.$minor"
}
''') , "top"),
    ("Sort and compare versions", "println(List(new Version(2, 1), new Version(1, 9), new Version(2, 0)).sorted)\nprintln(new Version(1, 0) < new Version(1, 1))"),
], note="Abstract class: can have constructor parameters, one parent only. Trait: no constructor parameters, many can be mixed in (linearisation decides the order). "
        "Trying to override a final member or to extend a final class does not compile (`cannot override final member`, `illegal inheritance from final class`).")

# ------------------------------------------------------------------------------------------------ 3.7 / 4.1
sgroup("4.1", "Exception handling in Scala", "Module 4: Exception Handling", [
    ENTRY,
    ("Imports", "import scala.util.{Try, Success, Failure, Using}\nimport scala.util.control.NonFatal", "import"),
    ("try / catch / finally", c(r'''
try {
  val n = "abc".toInt
  println(n)
} catch {
  case e: NumberFormatException => println(s"bad number: ${e.getMessage}")
} finally {
  println("cleanup always runs")
}
''')),
    ("Several kinds of exception in one catch", c(r'''
def risky(i: Int): String =
  try {
    i match {
      case 0 => throw new IllegalArgumentException("zero not allowed")
      case 1 =>
        val a = Array(1)
        a(5).toString
      case 2 => (10 / (i - 2)).toString
      case _ => "ok"
    }
  } catch {
    case e: IllegalArgumentException => s"IAE: ${e.getMessage}"
    case _: ArrayIndexOutOfBoundsException => "index out of range"
    case _: ArithmeticException => "division by zero"
  }
println(List(0, 1, 2, 3).map(risky))
''')),
    ("try is an expression: it has a value", "val parsed = try \"42\".toInt catch { case _: NumberFormatException => -1 }\nprintln(parsed)"),
    ("A custom exception class", "class InsufficientFundsException(val needed: Double, msg: String) extends Exception(msg)", "top"),
    ("throw it and catch it", c(r'''
def withdraw(balance: Double, amt: Double): Double = {
  if (amt > balance) throw new InsufficientFundsException(amt - balance, s"short by ${amt - balance}")
  balance - amt
}
try withdraw(100, 250) catch {
  case e: InsufficientFundsException => println(s"${e.getMessage} (needed ${e.needed})")
}
''')),
    ("require and assert", c(r'''
try { require(1 > 2, "one is not greater than two") } catch { case e: IllegalArgumentException => println(e.getMessage) }
try { assert(1 + 1 == 3, "math") } catch { case e: AssertionError => println(e.getMessage) }
''')),
    ("Option: a value that may be missing", c(r'''
def find(id: Int): Option[String] = Map(1 -> "Asha", 2 -> "Ravi").get(id)
println(find(1))
println(find(9))
println(find(9).getOrElse("unknown"))
find(2) match {
  case Some(n) => println(n)
  case None => println("none")
}
''')),
    ("Try: an exception as a value", c(r'''
val ok = Try("12".toInt)
val bad = Try("x".toInt)
println(ok)
println(bad.isFailure)
println(bad.getOrElse(0))
bad match {
  case Success(v) => println(v)
  case Failure(e) => println(s"failed: ${e.getClass.getSimpleName}")
}
println(Try(10 / 0).recover { case _: ArithmeticException => Int.MaxValue })
''')),
    ("Chain Try values with a for expression", c(r'''
def parse(s: String) = Try(s.toInt)
val sum = for { a <- parse("4"); b <- parse("5") } yield a + b
val broken = for { a <- parse("4"); b <- parse("x") } yield a + b
println(sum)
println(broken.isFailure)
''')),
    ("Either: Left carries the error, Right the result", c(r'''
def safeDiv(a: Int, b: Int): Either[String, Int] = if (b == 0) Left("divide by zero") else Right(a / b)
println(safeDiv(10, 2))
println(safeDiv(1, 0))
println(safeDiv(10, 2).map(_ + 1))
safeDiv(1, 0) match {
  case Left(err) => println(s"error: $err")
  case Right(v) => println(v)
}
''')),
    ("NonFatal: catch ordinary errors, not JVM-fatal ones", "try { sys.error(\"boom\") } catch { case NonFatal(e) => println(s\"handled: ${e.getMessage}\") }"),
    ("Using: close a resource automatically", "val first = Using(new java.io.StringReader(\"data\")) { r => r.read().toChar }\nprintln(first)"),
    ("Wrap an exception and keep its cause", c(r'''
try {
  try { "x".toInt } catch { case e: NumberFormatException => throw new RuntimeException("config invalid", e) }
} catch {
  case e: RuntimeException => println(s"${e.getMessage} <- ${e.getCause.getClass.getSimpleName}")
}
''')),
    ("Inspect an exception", "try { 1 / 0 } catch { case e: Exception => println(e); println(e.getStackTrace.nonEmpty) }"),
], note="Scala has no checked exceptions: nothing forces you to catch. Prefer Option, Try or Either for expected failures and keep try / catch for unexpected ones. "
        "The catch block is a partial function made of case clauses, so put specific exceptions before general ones.")

# ------------------------------------------------------------------------------------------------ 4.2 Spark
SPARK_SESSION_SHOWN = c(r'''
val spark = SparkSession.builder().appName("pds").master("local[*]").getOrCreate()
val sc = spark.sparkContext
sc.setLogLevel("ERROR")
import spark.implicits._
println(spark.version)
''')
SPARK_SESSION_RUN = c(r'''
val spark = SparkSession.builder().appName("pds").master("local[2]")
  .config("spark.ui.enabled", "false").config("spark.driver.bindAddress", "127.0.0.1").config("spark.driver.host", "127.0.0.1").getOrCreate()
val sc = spark.sparkContext
sc.setLogLevel("ERROR")
import spark.implicits._
println(spark.version)
''')
sgroup("4.2", "Apache Spark: architecture, RDDs, DataFrames, SQL, MLlib, streaming, GraphX", "Module 4: Apache Spark Architecture, Spark Big Data, Apache Spark Components", [
    ENTRY,
    ("Imports", "import org.apache.spark.sql.SparkSession\nimport org.apache.spark.sql.functions._\nimport org.apache.spark.sql.expressions.Window\nimport java.nio.file.{Files, Paths}", "import"),
    ("The data type used for DataFrames and Datasets", "case class Emp(name: String, dept: String, salary: Double, age: Int)", "top"),
    ("Start Spark in local mode: this program is the driver", SPARK_SESSION_SHOWN, "", SPARK_SESSION_RUN),
    ("Architecture facts: master, parallelism, partitions", "println(sc.master)\nprintln(sc.defaultParallelism > 0)\nprintln(sc.parallelize(1 to 100, 4).getNumPartitions)"),
    ("RDD: transformations are lazy, actions run the job", "val nums = sc.parallelize(1 to 10)\nval evensSquared = nums.filter(_ % 2 == 0).map(x => x * x)\nprintln(evensSquared.collect().toList)\nprintln(evensSquared.count())\nprintln(nums.reduce(_ + _))"),
    ("Word count with reduceByKey", c(r'''
val lines = sc.parallelize(Seq("spark is fast", "spark is lazy", "scala runs spark"))
val counts = lines.flatMap(_.split(" ")).map(w => (w, 1)).reduceByKey(_ + _)
println(counts.collect().sortBy(r => (-r._2, r._1)).toList)
''')),
    ("The lineage (DAG) behind an RDD", "println(counts.toDebugString)"),
    ("Pair RDD join and caching", "val names = sc.parallelize(Seq((1, \"Asha\"), (2, \"Ravi\")))\nval marks = sc.parallelize(Seq((1, 90), (2, 75), (3, 60)))\nprintln(names.join(marks).collect().sortBy(_._1).toList)\nval cached = nums.map(_ * 2).cache()\nprintln(cached.sum())"),
    ("Shared variables: broadcast and accumulator", c(r'''
val lookup = sc.broadcast(Map(1 -> "IT", 2 -> "HR"))
val acc = sc.longAccumulator("evens")
sc.parallelize(1 to 10).foreach(x => if (x % 2 == 0) acc.add(1))
println(acc.value)
println(sc.parallelize(Seq(1, 2, 1)).map(lookup.value).collect().toList)
''')),
    ("DataFrame from case classes", c(r'''
val emp = Seq(Emp("Asha", "IT", 90000, 28), Emp("Ravi", "HR", 60000, 35),
              Emp("Meena", "IT", 110000, 41), Emp("Kabir", "HR", 65000, 30)).toDF()
emp.printSchema()
emp.show()
''')),
    ("select, filter, withColumn, orderBy", c(r'''
emp.select($"name", $"salary")
  .filter($"salary" > 62000)
  .withColumn("bonus", $"salary" * 0.1)
  .orderBy($"salary".desc)
  .show()
''')),
    ("groupBy and aggregations", "emp.groupBy(\"dept\")\n  .agg(count(\"*\").as(\"people\"), avg(\"salary\").as(\"avg_salary\"), max(\"age\").as(\"oldest\"))\n  .orderBy(\"dept\").show()"),
    ("Spark SQL on a temporary view", c(r'''
emp.createOrReplaceTempView("employees")
spark.sql("SELECT dept, ROUND(AVG(salary), 1) AS avg_salary FROM employees WHERE age > 29 GROUP BY dept ORDER BY dept").show()
''')),
    ("Join two DataFrames", c(r'''
val depts = Seq(("IT", "Bengaluru"), ("HR", "Pune")).toDF("dept", "city")
emp.join(depts, Seq("dept"), "inner").select("name", "dept", "city").orderBy("name").show()
''')),
    ("Window function: rank inside each department", c(r'''
val w = Window.partitionBy("dept").orderBy($"salary".desc)
emp.withColumn("rank", rank().over(w)).select("name", "dept", "rank").orderBy("dept", "rank").show()
''')),
    ("Typed Dataset", "val ds = emp.as[Emp]\nprintln(ds.filter(_.age > 29).map(_.name).collect().toList)"),
    ("User-defined function", "val level = udf((s: Double) => if (s >= 100000) \"high\" else \"normal\")\nemp.withColumn(\"level\", level($\"salary\")).select(\"name\", \"level\").show()"),
    ("Read a CSV file", c(r'''
Files.write(Paths.get("people.csv"), "name,age\nAsha,28\nRavi,35\n".getBytes)
val people = spark.read.option("header", "true").option("inferSchema", "true").csv("people.csv")
people.show()
people.printSchema()
''')),
    ("The execution plan Spark will run", "emp.filter($\"age\" > 29).groupBy(\"dept\").count().explain()"),
    ("MLlib: K-means clustering", c(r'''
import org.apache.spark.ml.feature.VectorAssembler
import org.apache.spark.ml.clustering.KMeans
val pts = Seq((1.0, 1.0), (1.2, 0.8), (0.9, 1.1), (8.0, 8.0), (8.2, 7.9), (7.8, 8.1)).toDF("x", "y")
val feats = new VectorAssembler().setInputCols(Array("x", "y")).setOutputCol("features").transform(pts)
val model = new KMeans().setK(2).setSeed(1L).fit(feats)
println(model.clusterCenters.map(c => c.toArray.map(v => math.round(v)).toList).sortBy(_.head).toList)
''')),
    ("MLlib: linear regression", c(r'''
import org.apache.spark.ml.regression.LinearRegression
val train = Seq((1.0, 3.0), (2.0, 5.0), (3.0, 7.0), (4.0, 9.0)).toDF("x", "label")
val data = new VectorAssembler().setInputCols(Array("x")).setOutputCol("features").transform(train)
val lr = new LinearRegression().fit(data)
println((math.round(lr.coefficients(0)), math.round(lr.intercept)))
''')),
    ("Structured Streaming: a rate source into a memory table", c(r'''
val stream = spark.readStream.format("rate").option("rowsPerSecond", 5).load()
val query = stream.writeStream.format("memory").queryName("ticks").outputMode("append").start()
Thread.sleep(3000)
query.stop()
println(spark.sql("SELECT COUNT(*) FROM ticks").first().getLong(0) > 0)
'''), "skip"),
    ("GraphX: a small graph, degrees and PageRank", c(r'''
import org.apache.spark.graphx.{Edge, Graph}
val users = sc.parallelize(Seq((1L, "Asha"), (2L, "Ravi"), (3L, "Meena")))
val follows = sc.parallelize(Seq(Edge(1L, 2L, "follows"), Edge(2L, 3L, "follows"), Edge(3L, 2L, "follows")))
val graph = Graph(users, follows)
println(graph.inDegrees.collect().sortBy(_._1).toList)
println(graph.pageRank(0.001).vertices.collect().sortBy(-_._2).head._1)
''')),
    ("Stop the session", "spark.stop()"),
], note="Architecture: the driver (your program, holds the SparkSession) builds a DAG of transformations; the cluster manager gives it executors; executors run tasks on partitions. Nothing runs until an action (collect, count, show, write). "
        "Components: Spark Core (RDDs), Spark SQL / DataFrames, Structured Streaming, MLlib, GraphX. Run in local mode on one machine.",
    deps=["org.apache.spark::spark-sql:3.5.1", "org.apache.spark::spark-mllib:3.5.1", "org.apache.spark::spark-graphx:3.5.1"],
    directives=["//> using javaOpt " + SPARK_OPTS])
