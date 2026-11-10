//> using scala 2.13.12
//> using dep org.scalanlp::breeze:2.1.0
// Notes M4: functional error handling in depth, resource management, and Breeze (also PCA with Breeze)
import breeze.linalg._
import breeze.stats.mean
import scala.util.control.NonFatal
import scala.util.{Failure, Success, Try, Using}

object N4 extends App {
  println("--- try/catch/finally as an expression ---")
  def f(x: Int): Int = try { 10 / x } catch { case _: ArithmeticException => -1 } finally println("  finally ran")
  println("f(2) = " + f(2) + " | f(0) = " + f(0))
  def g(): String = try { return "from try" } finally { println("  finally before the value is returned") }
  println(g())

  println("\n--- catch order and NonFatal ---")
  def risky(i: Int): String = try {
    i match { case 0 => throw new IllegalArgumentException("bad arg"); case 1 => Integer.parseInt("x").toString; case 2 => throw new java.io.IOException("disk"); case _ => "fine" }
  } catch {
    case e: IllegalArgumentException => s"IllegalArgument: ${e.getMessage}"
    case NonFatal(e)                 => s"NonFatal: ${e.getClass.getSimpleName}"
  }
  println("  " + (0 to 2).map(risky).mkString(" | ") + "    (case 1: NumberFormatException is a subclass of IllegalArgumentException, so the FIRST handler wins)")
  println("  NonFatal(IOException) = " + NonFatal(new java.io.IOException()) + " | NonFatal(StackOverflowError) = " + NonFatal(new StackOverflowError()) + " | NonFatal(OutOfMemoryError) = " + NonFatal(new OutOfMemoryError()) + "  (never swallow fatal errors; Try does not catch them)")

  println("\n--- Try: map/flatMap/recover/recoverWith/toOption/fold ---")
  def parse(s: String): Try[Int] = Try(s.trim.toInt)
  def reciprocal(n: Int): Try[Double] = if (n == 0) Failure(new ArithmeticException("zero")) else Success(1.0 / n)
  for (s <- List("4", "0", "x")) {
    val r = parse(s).flatMap(reciprocal)
    println(s"  '$s' -> $r | getOrElse(-1.0) = ${r.getOrElse(-1.0)} | recover = ${r.recover { case _: ArithmeticException => Double.PositiveInfinity; case _: NumberFormatException => Double.NaN }}")
  }
  println("  for-comprehension stops at the first failure: " + (for { a <- parse("2"); b <- parse("oops"); c <- parse("5") } yield a + b + c))
  println("  fold: " + parse("5").fold(e => "failed " + e.getMessage, v => s"got $v"))
  println("  a Failure is only a value; calling .get on it re-throws the stored exception: " + Try(parse("x").get).failed.get.getClass.getSimpleName)

  println("\n--- Either: errors with information ---")
  def age(s: String): Either[String, Int] =
    Try(s.toInt).toEither.left.map(_ => s"'$s' is not a number").flatMap(n => if (n < 0) Left("negative age") else Right(n))
  println("  " + List("21", "-3", "abc").map(age))
  println("  fold: " + age("-3").fold(err => "error: " + err, v => "ok " + v) + " | partitionMap: " + List("21", "-3", "abc", "40").partitionMap(age))
  println("  sequence-like: all valid? " + List("1", "2").map(age).forall(_.isRight) + " | first error: " + List("1", "x", "y").map(age).collectFirst { case Left(e) => e })

  println("\n--- Using: automatic resource closing ---")
  class Res(n: String) extends AutoCloseable { def close(): Unit = println(s"  closing $n"); def read = s"data from $n" }
  println("  " + Using(new Res("file1"))(_.read))
  println("  with a failure inside, the resource still closes and the result is: " + Using(new Res("file2"))(_ => throw new RuntimeException("boom")))
  println("  two resources close in reverse order: " + Using.Manager { use => val a = use(new Res("A")); val b = use(new Res("B")); a.read + "+" + b.read })

  println("\n--- Breeze: vectors, matrices, slicing, broadcasting ---")
  val v = DenseVector(1.0, 2.0, 3.0); val w = DenseVector(4.0, 5.0, 6.0)
  println("  v + w = " + (v + w) + " | v *:* w = " + (v *:* w) + " | v dot w = " + (v dot w) + " | v * 2.0 = " + (v * 2.0) + " | sum(v) = " + sum(v))
  val m = DenseMatrix((1.0, 2.0), (3.0, 4.0))
  println("  m * m (matrix product) = " + (m * m).toString.replace("\n", " ; ") + " | m *:* m (element-wise) = " + (m *:* m).toString.replace("\n", " ; "))
  println("  m.t = " + m.t.toString.replace("\n", " ; ") + " | det = " + det(m) + " | inv = " + inv(m).toString.replace("\n", " ; "))
  println("  slicing: v(0 to 1) = " + v(0 to 1) + " | m(::, 0) = " + m(::, 0) + " | m(1, ::) = " + m(1, ::).t + " | m(0, 1) = " + m(0, 1))
  val cols = DenseMatrix((1.0, 10.0), (2.0, 20.0), (3.0, 30.0))
  println("  broadcasting: subtract column means = " + (cols(*, ::) - mean(cols(::, *)).t).toString.replace("\n", " ; "))
  println("  indexing is 0-based and uses (), like Scala arrays; v(5) throws " + Try(v(5)).failed.get.getClass.getSimpleName)

  println("\n--- PCA in Breeze: eigen-decomposition of the covariance matrix (same 5 points as the Python notes) ---")
  val X = DenseMatrix((2.0, 1.0), (3.0, 5.0), (4.0, 3.0), (5.0, 6.0), (6.0, 5.0))
  val mu = mean(X(::, *)).t
  val Xc = X(*, ::) - mu
  val C = (Xc.t * Xc) / (X.rows - 1.0)
  val es = eigSym(C)
  println("  covariance = " + C.toString.replace("\n", " ; "))
  println("  eigenvalues (ascending) = " + es.eigenvalues + " | explained ratio of the largest = " + f"${es.eigenvalues(1) / sum(es.eigenvalues)}%.4f")
  println("  eigenvectors (columns) = " + es.eigenvectors.toString.replace("\n", " ; "))
}
