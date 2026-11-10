//> using scala 2.13.12
//> using dep org.scalanlp::breeze:2.1.0
//> using dep org.typelevel::spire:0.18.0
// M4-Q2  Breeze (numerical computing, Lab 19) and Spire (exact numerics, Lab 20)
import breeze.linalg._
import breeze.stats.{mean, variance}

object M4Q2 extends App {
  val fruits = Seq("Apple", "Banana", "Cherry", "Mango", "Orange")
  val price = DenseVector(2.50, 1.20, 4.00, 3.50, 2.00)
  val qty = DenseVector(150.0, 300.0, 80.0, 110.0, 200.0)

  val revenue = price *:* qty                               // element-wise (Hadamard) product
  fruits.indices.foreach(i => println(f"${fruits(i)}%-7s ${price(i)}%.2f x ${qty(i)}%.0f = ${revenue(i)}%.2f"))
  println(f"total revenue = ${sum(revenue)}%.2f, mean price = ${mean(price)}%.3f, variance = ${variance(price)}%.4f")

  val A = DenseMatrix((2.0, 1.0), (1.0, 3.0))
  val b = DenseVector(3.0, 5.0)
  val x = A \ b                                             // solve A x = b
  println("A*x = b  ->  x = " + x.map(v => math.round(v * 1000) / 1000.0))
  println("A * A^T  = " + (A * A.t))
  println("dot      = " + (price dot qty))

  // ---- Spire: exact rational arithmetic, no floating-point error ----
  import spire.math.Rational
  val d = 0.1 + 0.2
  val r = Rational(1, 10) + Rational(2, 10)
  println(s"Double 0.1 + 0.2 = $d   | Rational 1/10 + 2/10 = $r  (exactly 3/10: ${r == Rational(3, 10)})")
}
