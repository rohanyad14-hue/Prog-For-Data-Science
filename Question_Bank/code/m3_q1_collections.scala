// M3-Q1  Collections and functional combinators (Lab experiments 13-16)
import scala.collection.mutable

object M3Q1 extends App {
  // ---- Arrays (mutable, fixed size, index with parentheses) ----
  val nums = Array(2, 5, 9, 14, 20)
  def sum(a: Array[Int]): Int = a.sum
  val fruits = Array("apple", "banana", "cherry", "mango", "orange")
  def join(a: Array[String]): String = a.mkString(",")
  nums(0) = 99                                   // arrays are mutable even when declared with val
  println(s"sum = ${sum(nums)}, joined = ${join(fruits)}")

  // ---- List (immutable linked list), Set, Tuple ----
  val primes = List(2, 3, 5, 7, 11)
  println("squares : " + primes.map(p => p * p))
  println("cons    : " + (0 :: primes))                    // O(1) prepend creates a new list
  val s1 = "hello world".filter(_ != ' ').toSet            // unique characters
  val s2 = "world".toSet
  println("set and : " + (s1 intersect s2).toList.sorted)
  val t = (42, "scala", true)
  println(s"tuple   : ${t._1}, ${t._2}, ${t._3}")

  // ---- Map: duplicate key overwrites; merge with conflict rule; chaining ----
  val grades = mutable.HashMap("Alice" -> 85, "Bob" -> 78)
  grades.put("Alice", 95)                                  // same key -> old value replaced
  println("grades  : " + grades.toList.sorted)

  def mergeMax(a: Map[String, Int], b: Map[String, Int]): Map[String, Int] =
    (a.keySet ++ b.keySet).map(k => k -> math.max(a.getOrElse(k, 0), b.getOrElse(k, 0))).toMap
  println("merge   : " + mergeMax(Map("Alice" -> 85, "Bob" -> 90), Map("Alice" -> 92, "Emma" -> 88)).toList.sorted)

  val attempts = Seq("Alice" -> 85, "Bob" -> 78, "Alice" -> 95)
  val chained = attempts.foldLeft(Map.empty[String, List[Int]]) { case (acc, (k, v)) =>
    acc + (k -> (acc.getOrElse(k, Nil) :+ v))              // separate chaining with a List per key
  }
  println("chained : " + chained.toList.sortBy(_._1))

  // ---- Functional combinators ----
  val xs = (1 to 10).toList
  println("filter  : " + xs.filter(_ % 2 == 0))
  println("map     : " + xs.map(_ * 3))
  println("flatMap : " + xs.take(4).flatMap(n => List((n, n * n))))
  println("foldLeft: " + xs.foldLeft(1L)(_ * _))           // 10! = 3628800
  println("reduce  : " + xs.reduce(_ + _))
  println("flatMap on strings: " + List("hi", "yo").flatMap(_.toList))
}
