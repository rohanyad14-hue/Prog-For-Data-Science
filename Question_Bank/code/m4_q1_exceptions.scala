// M4-Q1  Exception handling in Scala: try/catch/finally, custom exceptions, Option, Try, Either
import scala.util.{Try, Success, Failure}

class InsufficientFundsException(msg: String) extends Exception(msg)    // custom (checked-style) exception

object M4Q1 extends App {
  // ---- 1. try / catch / finally: catch is a pattern match, try is an expression ----
  def divide(a: Int, b: Int): Int =
    try {
      a / b
    } catch {
      case _: ArithmeticException => println("  caught ArithmeticException"); 0
      case e: Exception           => println("  other: " + e.getMessage); -1
    } finally {
      println(s"  finally runs for divide($a, $b)")
    }
  println("divide(10, 2) = " + divide(10, 2))
  println("divide(10, 0) = " + divide(10, 0))

  // ---- 2. throwing a custom exception ----
  def withdraw(balance: Double, amount: Double): Double = {
    if (amount > balance) throw new InsufficientFundsException(s"balance $balance < $amount")
    balance - amount
  }
  try withdraw(100, 250) catch { case e: InsufficientFundsException => println("custom: " + e.getMessage) }

  // ---- 3. Option: absence of a value without null ----
  val phone = Map("asha" -> "98400", "ravi" -> "98410")
  println("Option  : " + phone.get("asha") + " | " + phone.get("zed") + " | " + phone.get("zed").getOrElse("n/a"))

  // ---- 4. Try: wrap code that may throw, then map / recover ----
  def parse(s: String): Try[Int] = Try(s.trim.toInt)
  for (s <- List("42", "4x2")) parse(s) match {
    case Success(v) => println(s"Try     : '$s' -> Success($v)")
    case Failure(e) => println(s"Try     : '$s' -> Failure(${e.getClass.getSimpleName})")
  }
  println("recover : " + parse("oops").recover { case _: NumberFormatException => -1 }.get)
  println("chain   : " + parse("20").map(_ * 2).filter(_ > 30).toOption)

  // ---- 5. Either: an error value that carries information (Left = error, Right = success) ----
  def safeSqrt(x: Double): Either[String, Double] =
    if (x < 0) Left(s"cannot take sqrt of $x") else Right(math.sqrt(x))
  println("Either  : " + safeSqrt(16) + " | " + safeSqrt(-4))
  println("compose : " + (for { a <- safeSqrt(16); b <- safeSqrt(a) } yield b))
}
