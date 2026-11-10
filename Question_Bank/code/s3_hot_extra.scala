// Authored HOT questions, Module 3: order processing with combinators, and a billing calculator (Scala 2.13)
import java.io.StringReader
import scala.util.Try

case class Order(id: Int, item: String, qty: Int, unitPrice: Int, coupon: Option[String])

sealed trait Size
case object Small extends Size
case object Medium extends Size
case object Large extends Size

object S3HotExtra extends App {
  val orders = List(Order(1, "Laptop", 1, 65000, Some("SAVE10")), Order(2, "Mouse", 3, 500, None), Order(3, "Laptop", 2, 64000, None),
                    Order(4, "Monitor", 1, 12000, Some("SAVE5")), Order(5, "Mouse", 2, 450, Some("BOGUS")))
  def value(o: Order): Int = o.qty * o.unitPrice

  println("--- H3-6 step 1: revenue per product with groupBy / map / reduce ---")
  val byItem = orders.groupBy(_.item).map { case (item, os) => item -> os.map(value).sum }
  println("revenue per item   : " + byItem.toList.sortBy(-_._2))
  println("units per item     : " + orders.groupBy(_.item).map { case (i, os) => i -> os.map(_.qty).sum }.toList.sortBy(_._1))
  println("total revenue      : reduce = " + orders.map(value).reduce(_ + _) + ", foldLeft = " + orders.foldLeft(0)((acc, o) => acc + value(o)) + ", sum = " + orders.map(value).sum)
  println("same logic, imperative: " + { var t = 0; for (o <- orders) t += value(o); t })

  println("\n--- H3-6 step 2: folds and the direction trap ---")
  val biggest = orders.foldLeft(orders.head)((best, o) => if (value(o) > value(best)) o else best)
  println("largest order via foldLeft: " + biggest.id + " (" + biggest.item + ", " + value(biggest) + ") | maxBy gives " + orders.maxBy(value).id)
  println("running revenue (scanLeft): " + orders.map(value).scanLeft(0)(_ + _).tail)
  println("foldLeft(0)(_ - _) = " + orders.map(_.qty).foldLeft(0)(_ - _) + " but foldRight(0)(_ - _) = " + orders.map(_.qty).foldRight(0)(_ - _) + " (subtraction is not associative: the direction matters)")

  println("\n--- H3-6 step 3: pattern matching with guards and a sealed hierarchy ---")
  def size(o: Order): Size = value(o) match { case v if v >= 60000 => Large; case v if v >= 5000 => Medium; case _ => Small }
  println("order sizes: " + orders.map(o => o.id + "=" + size(o)))
  def label(s: Size): String = s match { case Small => "ship normally"; case Medium => "check stock"; case Large => "manager approval" }
  println("actions    : " + orders.map(o => label(size(o))))
  println("match on tuples and lists: " + (orders.map(o => (o.item, o.qty)) match { case ("Laptop", 1) :: rest => s"first order is a single laptop, ${rest.size} more orders"; case _ => "other" }))

  println("\n--- H3-6 step 4: Option instead of null for the missing coupon ---")
  val discounts = Map("SAVE10" -> 10, "SAVE5" -> 5)
  def pct(o: Order): Int = o.coupon.flatMap(discounts.get).getOrElse(0)
  println("discount percent per order: " + orders.map(o => o.id + ":" + pct(o)) + " (None and the unknown coupon BOGUS both give 0)")
  println("net revenue after coupons : " + orders.map(o => value(o) * (100 - pct(o)) / 100).sum)
  println("coupon strings used       : " + orders.flatMap(_.coupon) + " | orders with no coupon: " + orders.count(_.coupon.isEmpty))
  println("a for-comprehension over Options: " + (for { o <- orders.find(_.id == 1); c <- o.coupon; d <- discounts.get(c) } yield d) + " versus " + (for { o <- orders.find(_.id == 2); c <- o.coupon; d <- discounts.get(c) } yield d))

  println("\n--- H3-8 billing calculator: functions, strings, numbers, booleans ---")
  val items = List(("Pen", 10, 5), ("Book", 2, 250), ("Bag", 1, 799))
  def lineTotal(qty: Int, price: Int): Int = { qty * price }                   // expanded form
  def gst(amount: Int, percent: Int = 18) = amount * percent / 100             // short form with a default argument
  val subtotal = items.map { case (_, q, p) => lineTotal(q, p) }.sum
  println(f"subtotal $subtotal, GST ${gst(subtotal)}, total ${subtotal + gst(subtotal)}  (integer arithmetic truncates: 1349 * 18 / 100 = ${1349 * 18 / 100}, exact value ${1349 * 0.18})")
  println("per-line output with f-interpolation:")
  items.foreach { case (n, q, p) => println(f"  $n%-6s $q%3d x $p%5d = ${lineTotal(q, p)}%6d") }
  println(s"as a string: ${items.map(_._1).mkString(", ")} | upper: ${items.map(_._1.toUpperCase)} | length of 'Book': ${"Book".length}")
  println("Int vs Double: 7 / 2 = " + 7 / 2 + ", 7 / 2.0 = " + 7 / 2.0 + ", 799 * 0.18 = " + 799 * 0.18 + " (use whole paise or BigDecimal for money)")
  println("BigDecimal exact money: " + (BigDecimal("799") * BigDecimal("0.18")) + " | Double: " + 799 * 0.18)
  def lazyDiscount(eligible: Boolean, calc: => Int): Int = if (eligible) calc else 0       // by-name parameter
  var evaluated = 0
  def expensive(): Int = { evaluated += 1; 100 }
  println("by-name: lazyDiscount(false, expensive()) = " + lazyDiscount(false, expensive()) + ", evaluations = " + evaluated + " | lazyDiscount(true, ...) = " + lazyDiscount(true, expensive()) + ", evaluations = " + evaluated)
  val vip = true; val big = subtotal > 1000
  println(s"booleans: vip && big = ${vip && big}, vip || big = ${vip || big}, !big = ${!big}, 'a' == 'a' is ${'a' == 'a'}, \"ab\" == \"a\" + \"b\" is ${"ab" == "a" + "b"}")
  Console.withIn(new StringReader("3\n250\n")) {
    val q = scala.io.StdIn.readInt(); val p = scala.io.StdIn.readInt()
    println(s"input read from the keyboard stand-in: qty=$q price=$p total=${lineTotal(q, p)}")
  }
  println("safe parse of user text: " + List("12", "x1", " 7 ").map(s => Try(s.trim.toInt).toOption))
}
