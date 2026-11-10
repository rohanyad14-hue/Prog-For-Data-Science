// M3-Q4  Scala fundamentals: function formats, variables, strings, input, numbers, operators, booleans
import java.io.StringReader

object M3Q4 extends App {
  // ---- function formats: full (expanded) form, short form, function literal, higher-order ----
  def addExpanded(a: Int, b: Int): Int = {          // expanded: braces, explicit return type
    return a + b                                    // `return` is legal but unidiomatic
  }
  def add(a: Int, b: Int) = a + b                   // last expression is the result, type inferred
  val addLit: (Int, Int) => Int = (a, b) => a + b   // anonymous function stored in a val
  def twice(f: Int => Int, x: Int): Int = f(f(x))   // higher-order function
  println(s"functions : ${addExpanded(2, 3)} ${add(2, 3)} ${addLit(2, 3)} ${twice(_ * 3, 2)}")

  // ---- val / var, type inference, lazy val ----
  val fixed = 10                                    // immutable reference
  var counter = 0                                   // mutable reference
  counter += 1
  lazy val expensive = { println("  (computing lazy val once)"); 42 }
  println(s"val/var    : $fixed $counter, types ${fixed.getClass.getSimpleName}")
  println("lazy       : " + expensive + " " + expensive)

  // ---- strings and interpolation ----
  val name = "Rohan"; val gpa = 8.4567
  println(s"s-string   : Hello $name, next year ${2026 + 1}")
  println(f"f-string   : GPA = $gpa%.2f, padded = ${42}%05d")
  println(raw"raw-string : no escape \n here")
  println("methods    : " + "scala".toUpperCase + " " + "scala".reverse + " " + "a,b,c".split(",").toList)

  // ---- getting user input (simulated here with a StringReader instead of the keyboard) ----
  Console.withIn(new StringReader("25\nScala\n")) {
    val age = scala.io.StdIn.readInt()
    val lang = scala.io.StdIn.readLine()
    println(s"input      : age=$age, language=$lang")
  }

  // ---- numbers and operators (operators are just methods) ----
  println(s"numbers    : ${7 / 2} ${7 % 2} ${7 / 2.0} ${1 + 2 * 3} ${(1).+(2)}")
  println(s"types      : ${Int.MaxValue} ${Long.MaxValue} ${5.toDouble} ${3.9.toInt} ${'a'.toInt}")
  println(s"overflow   : ${Int.MaxValue + 1}")
  println(s"bitwise    : ${6 & 3} ${6 | 3} ${6 ^ 3} ${1 << 3}")

  // ---- booleans, short-circuit evaluation, == versus eq ----
  def noisy(b: Boolean): Boolean = { println("  evaluated"); b }
  println("short-circuit: " + (false && noisy(true)))      // right side never evaluated
  println("or          : " + (true || noisy(false)))
  println(s"equality   : ${"ab" == "a" + "b"} ${List(1, 2) == List(1, 2)} ${new String("x") eq new String("x")}")
}
