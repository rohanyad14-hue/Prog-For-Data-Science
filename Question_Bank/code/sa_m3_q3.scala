//> using scala 2.13.12
// Sample answer M3-Q3: Map and functional combinators (map, filter, reduce) compared with an imperative loop
import scala.collection.mutable

object Cart {
  def main(args: Array[String]): Unit = {
    val prices = Map("Laptop" -> 65000, "Mobile" -> 25000, "Tablet" -> 18000, "Headphone" -> 3000)
    val show = (m: Map[String, Double]) => m.toList.sortBy(_._1).map { case (k, v) => f"$k -> $v%.1f" }.mkString(", ")

    println("--- functional version: no variable is ever changed ---")
    val discounted = prices.map { case (item, p) => item -> p * 0.9 }          // 10% discount on every product
    val expensive = prices.filter { case (_, p) => p > 20000 }                  // products above Rs. 20,000
    val totalValue = prices.values.reduce(_ + _)                                // total inventory value (one unit of each)
    println("discounted : " + show(discounted))
    println("expensive  : " + expensive.keys.toList.sorted)
    println("total      : " + totalValue + " (after discount " + discounted.values.sum + ")")

    println("--- imperative version of the same three tasks ---")
    val discounted2 = mutable.Map[String, Double]()
    var expensive2 = List[String]()
    var total2 = 0
    for ((item, p) <- prices) {
      discounted2(item) = p * 0.9
      if (p > 20000) expensive2 = item :: expensive2
      total2 += p
    }
    println("discounted : " + show(discounted2.toMap))
    println("expensive  : " + expensive2.sorted)
    println("total      : " + total2)
    println("same answers: " + (discounted == discounted2.toMap && expensive.keySet == expensive2.toSet && totalValue == total2))

    println("--- a chained pipeline reads like the requirement ---")
    val report = prices.filter(_._2 > 20000).map { case (i, p) => i -> p * 0.9 }.values.sum
    println("discounted value of the expensive products: " + report)

    println("--- reduce fails on an empty collection, foldLeft does not ---")
    try Map.empty[String, Int].values.reduce(_ + _)
    catch { case e: UnsupportedOperationException => println("reduce: " + e.getMessage) }
    println("foldLeft: " + Map.empty[String, Int].values.foldLeft(0)(_ + _))
  }
}
