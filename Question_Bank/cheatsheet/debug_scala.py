"""Format-2 (debug the program) items for the Scala labs.
kind  "compile"  the buggy code does not compile; `contains` must appear in the compiler message
      "runtime"  compiles, then throws; `contains` must appear in the exception line
      "silent"   compiles and runs, prints a wrong result; `contains` must appear in stdout
`top` / `top_fixed` are declarations placed before the object (classes), `imports` are placed at the top of the file.
verify_debug_scala.py compiles and runs every item with scala-cli and stores the real messages in debug_scala_results.json.
"""

SCALA_BUGS = []


def sbug(topic, buggy, fixed, why, kind, contains, fixed_contains="", top="", top_fixed=None, imports="", deps=()):
    SCALA_BUGS.append(dict(topic=topic, buggy=buggy.strip("\n"), fixed=fixed.strip("\n"), why=why, kind=kind, contains=contains,
                           fixed_contains=fixed_contains, top=top, top_fixed=top if top_fixed is None else top_fixed,
                           imports=imports, deps=list(deps)))


sbug("val / var", "val x = 5\nx = 10", "var x = 5\nx = 10\nprintln(x)",
     "A val is a constant. Declare it with var if it must change (prefer new vals in functional code).", "compile", "reassignment to val", "10")
sbug("arrays", "val arr = Array(1, 2, 3)\nprintln(arr[0])", "val arr = Array(1, 2, 3)\nprintln(arr(0))",
     "Scala indexes with round brackets arr(i). Square brackets are for type parameters, e.g. Array[Int].", "compile", "", "1")
sbug("List", "val l = List(1, 2, 3)\nl(0) = 10", "val l = List(1, 2, 3)\nval l2 = l.updated(0, 10)\nprintln(l2)",
     "List (and the default Map/Set) is immutable, there is no update. updated returns a new list. Use Array or ListBuffer when you really need in-place changes.",
     "compile", "update is not a member", "List(10, 2, 3)")
sbug("Set", "val s = Set(1, 2)\ns += 3", "val s = Set(1, 2)\nval s2 = s + 3\nprintln(s2)",
     "The default Set is immutable, so += would have to reassign the val. Use s + 3 to get a new set, or scala.collection.mutable.Set / a var.",
     "compile", "", "Set(1, 2, 3)")
sbug("Map", "val m = Map(\"a\" -> 1)\nprintln(m(\"b\"))", "val m = Map(\"a\" -> 1)\nprintln(m.getOrElse(\"b\", 0))\nprintln(m.get(\"b\"))",
     "m(key) throws when the key is absent. get returns an Option (None if absent) and getOrElse supplies a default.",
     "runtime", "key not found: b", "None")
sbug("case class", "val p = P(\"Ann\", 20)\np.age = 21", "val p = P(\"Ann\", 20)\nval p2 = p.copy(age = 21)\nprintln(p2)",
     "Case-class parameters are immutable vals. copy(...) builds a new object with the changed field.", "compile", "reassignment to val",
     "P(Ann,21)", top="case class P(name: String, age: Int)")
sbug("tuples", "val t = (1, \"a\")\nprintln(t(0))", "val t = (1, \"a\")\nprintln(t._1)\nval (num, txt) = t",
     "Tuple elements are read with t._1, t._2 (counting from 1), or by destructuring. Tuples cannot be indexed with ( ).", "compile", "", "1")
sbug("types", "val x: Int = \"5\"", "val x: Int = \"5\".toInt\nprintln(x + 1)",
     "Scala is statically typed: a String is not an Int. Convert explicitly with toInt / toDouble.", "compile", "type mismatch", "6")
sbug("integer division", "val nums = List(1, 2, 3, 4)\nprintln(nums.sum / nums.length)", "val nums = List(1, 2, 3, 4)\nprintln(nums.sum.toDouble / nums.length)",
     "Int / Int is integer division (10 / 4 = 2). No error, just a wrong mean. Convert one operand to Double first.", "silent", "2", "2.5")
sbug("arrays", "val a = Array(1, 2, 3)\nprintln(a.length())", "val a = Array(1, 2, 3)\nprintln(a.length)",
     "length is a parameterless member, so it is written without ( ). (size works as well.)", "compile", "does not take parameters", "3")
sbug("string interpolation", "val lst = List(1, 2, 3)\nprintln(s\"Length: $lst.length\")", "val lst = List(1, 2, 3)\nprintln(s\"Length: ${lst.length}\")",
     "$name only takes the identifier. A method call or expression needs braces: ${lst.length}.", "silent", "List(1, 2, 3).length", "Length: 3")
sbug("string interpolation", "val name = \"Rohan\"\nprintln(\"Hello $name\")", "val name = \"Rohan\"\nprintln(s\"Hello $name\")",
     "Without the s prefix the dollar sign is just text. f\"...\" (formatted) and raw\"...\" are the other interpolators.", "silent", "Hello $name", "Hello Rohan")
sbug("Option", "val m = Map(\"a\" -> 1)\nprintln(m.get(\"a\") + 1)", "val m = Map(\"a\" -> 1)\nprintln(m.getOrElse(\"a\", 0) + 1)",
     "get returns Option[Int], not Int, so + 1 is not defined. Unwrap with getOrElse, map or a pattern match.", "compile", "", "2")
sbug("imports", "val g = mutable.HashMap(\"a\" -> 1)", "import scala.collection.mutable\nval g = mutable.HashMap(\"a\" -> 1)\ng(\"b\") = 2\nprintln(g.size)",
     "mutable is not in scope. import scala.collection.mutable (the default collections are the immutable ones).", "compile", "not found: value mutable", "2")
sbug("Breeze", "val v = DenseVector(1.0, 2.0) :* DenseVector(3.0, 4.0)", "val v = DenseVector(1.0, 2.0) *:* DenseVector(3.0, 4.0)\nprintln(v)\nprintln(DenseVector(1.0, 2.0) dot DenseVector(3.0, 4.0))",
     "The old element-wise operator :* is gone in Breeze 2.x. Use *:* (a plain * between two vectors is element-wise too) and dot for the inner product.", "compile", "is not a member", "11.0",
     imports="import breeze.linalg._", deps=["org.scalanlp::breeze:2.1.0"])
sbug("Spire", "println(Rational(1 / 3))", "println(Rational(1, 3))\nprintln(Rational(1, 3) + Rational(1, 6))",
     "1 / 3 is integer division and is 0 before Rational ever sees it. Give the numerator and denominator separately.", "silent", "0", "1/3",
     imports="import spire.math._\nimport spire.implicits._", deps=["org.typelevel::spire:0.18.0"])
sbug("Saddle", "val s = Series(Vec(1.0, 2.0, 3.0), Index(\"a\", \"b\", \"c\"))\nprintln(s.mean)", "val s = Series(Vec(1.0, 2.0, 3.0), Index(\"a\", \"b\", \"c\"))\nprintln(s.values.mean)",
     "A Series has no mean method. Take the underlying Vec with .values (or .toVec) and call the statistic there.", "compile", "mean is not a member",
     "2.0", imports="import org.saddle._", deps=["io.github.pityka::saddle-core:4.0.0-M14"])
sbug("OOP", "val b = new B\nprintln(b.g)", "val b = new B\nprintln(b.g)",
     "Overriding a concrete member needs the override modifier.", "compile", "override", "2",
     top="class A { def g: Int = 1 }\nclass B extends A { def g: Int = 2 }",
     top_fixed="class A { def g: Int = 1 }\nclass B extends A { override def g: Int = 2 }")
sbug("OOP", "val e = new Emp(500)\nprintln(e.salary)", "val e = new Emp(500)\nprintln(e.getSalary)",
     "A private member is visible only inside the class. Expose it through a public method, or drop private.", "compile", "cannot be accessed", "500",
     top="class Emp(private val salary: Int)",
     top_fixed="class Emp(private val salary: Int) { def getSalary: Int = salary }")
sbug("OOP", "val f = Foo(3)\nprintln(f.x)", "val f = new Foo(3)\nprintln(f.x)",
     "Only case classes get an apply method, so a plain class needs new. (Scala 3 relaxes this, Scala 2.13 does not.)", "compile", "not found: value Foo", "3",
     top="class Foo(val x: Int)")
sbug("conversion", "println(\"abc\".toInt)", "println(\"abc\".toIntOption)\nprintln(\"42\".toIntOption.getOrElse(0))",
     "toInt throws on text that is not a number. toIntOption returns None instead, which you can default with getOrElse.", "runtime", "NumberFormatException", "None")
sbug("arrays", "val a = Array(1, 2, 3)\nprintln(a)", "val a = Array(1, 2, 3)\nprintln(a.mkString(\", \"))\nprintln(a.toList)",
     "Arrays are JVM arrays, so println shows the type code and hash ([I@...). Use mkString or toList to see the elements.", "silent", "[I@", "1, 2, 3")
sbug("List", "val l = List(1, 2, 3)\nl :+ 4\nprintln(l)", "val l = List(1, 2, 3)\nval l2 = l :+ 4\nprintln(l2)",
     "Immutable collections never change in place: :+ returns a NEW list, which was thrown away here. Keep the result in a val (or use a var / ListBuffer).",
     "silent", "List(1, 2, 3)", "List(1, 2, 3, 4)")
sbug("ranges", "val a = Array(10, 20, 30)\nfor (i <- 0 to a.length) println(a(i))", "val a = Array(10, 20, 30)\nfor (i <- 0 until a.length) println(a(i))",
     "to includes the end value, until excludes it. Indices are 0 .. length-1, so use until (or a.indices).", "runtime", "ArrayIndexOutOfBoundsException", "30")
sbug("methods", "def square(x: Int) { x * x }\nprintln(square(3))", "def square(x: Int): Int = x * x\nprintln(square(3))",
     "Without = the body is a procedure that returns Unit, so the value is lost and () is printed. Always write = after the parameter list.", "silent", "()", "9")
sbug("List", "println(List(1, 2, 3).get(0))", "println(List(1, 2, 3)(0))\nprintln(List(1, 2, 3).headOption)",
     "List has no get (that is Java, and Map.get). Use list(i), head or headOption.", "compile", "get is not a member", "1")
