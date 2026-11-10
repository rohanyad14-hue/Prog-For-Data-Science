package lab.exercises

/**
 * Exercise 14: Understanding Lists, Sets, and Tuples in Scala
 * 
 * Objectives:
 * 1. Create a list of the first five prime numbers.
 * 2. Function to return a new list with each element squared.
 * 3. Create a set of unique characters from "hello world".
 * 4. Function that takes two sets and returns their intersection.
 * 5. Create a tuple with 3 elements (Int, String, Boolean) and access/print each element.
 */
object Exercise14_Lists_Sets_Tuples {

  // Function to square all elements of a list
  def squareList(lst: List[Int]): List[Int] = {
    lst.map(x => x * x)
  }

  // Generic function to calculate intersection of two sets
  def setIntersection[T](s1: Set[T], s2: Set[T]): Set[T] = {
    s1.intersect(s2)
  }

  def main(args: Array[String]): Unit = {
    println("==================================================")
    println("    EXERCISE 14: LISTS, SETS, AND TUPLES")
    println("==================================================")

    // 1 & 2. Primes list and squaring
    val primes: List[Int] = List(2, 3, 5, 7, 11)
    val squaredPrimes = squareList(primes)
    println(s"1. Original Primes: $primes")
    println(s"2. Squared Primes:  $squaredPrimes")

    // 3 & 4. Unique character set and intersection
    val text = "hello world"
    val charSet: Set[Char] = text.toSet
    val comparisonSet: Set[Char] = Set('e', 'l', 'o', 'z', 'k')
    val intersection = setIntersection(charSet, comparisonSet)
    
    println(s"\n3. Unique characters in '$text': $charSet")
    println(s"   Comparison set: $comparisonSet")
    println(s"4. Intersection result: $intersection")

    // 5. Tuple creation and positional access
    val record: (Int, String, Boolean) = (2024, "Computer Science", true)
    println(s"\n5. Created Tuple: $record")
    println(s"   -> Element 1 (_1) [Integer]: ${record._1}")
    println(s"   -> Element 2 (_2) [String]:  ${record._2}")
    println(s"   -> Element 3 (_3) [Boolean]: ${record._3}")

    println("==================================================")
  }
}
